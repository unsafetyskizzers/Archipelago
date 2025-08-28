import asyncio
import Utils
import websockets
import functools
from copy import deepcopy
from typing import List, Any, Iterable
from NetUtils import decode, encode, JSONtoTextParser, JSONMessagePart, NetworkItem, NetworkPlayer
from MultiServer import Endpoint
from CommonClient import CommonContext, gui_enabled, ClientCommandProcessor, logger, get_base_parser

DEBUG = False

# THIS CODE IS LARGELY TAKEN FROM THE HAT IN TIME APWORLD! THANKS COOKIECAT FOR THE POINTERS! -whimsiemi

# to-do list: handle printjsons via the proxy (to make datapackages redundant), clean up things a bit and find a way to properly disconnect proxy client to stop weird shenanigans across different worlds/slots
class PTCommandProcessor(ClientCommandProcessor):
    def _cmd_pt(self):
        """Check PT Connection State"""
        if isinstance(self.ctx, PTContext):
            logger.info(f"PT Status: {self.ctx.get_pt_status()}")


class PTContext(CommonContext):
    command_processor = PTCommandProcessor
    game = "Pizza Tower"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.proxy = None
        self.proxy_task = None
        self.autoreconnect_task = None
        self.endpoint = None
        self.items_handling = 0b111
        self.room_info = None
        self.connected_msg = None
        self.game_connected = False
        self.awaiting_info = False
        self.just_collected = None
        self.full_inventory: List[Any] = []
        self.server_msgs: List[Any] = []
        self.connected = False
        self.authenticated = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(PTContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def get_pt_status(self) -> str:
        if not self.is_proxy_connected():
            return "Not connected to Pizza Tower"

        return "Connected to Pizza Tower"

    async def send_msgs_proxy(self, msgs: Iterable[dict]) -> bool:
        """ `msgs` JSON serializable """
        if not self.endpoint or not self.endpoint.socket.open or self.endpoint.socket.closed:
            return False

        if DEBUG:
            logger.info(f"Outgoing message: {msgs}")

        await self.endpoint.socket.send(msgs)
        return True

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def disconnect_proxy(self):
        if self.endpoint and not self.endpoint.socket.closed:
            await self.endpoint.socket.close()
        if self.proxy_task is not None:
            await self.proxy_task

    def is_connected(self) -> bool:
        return self.server and self.server.socket.open

    def is_proxy_connected(self) -> bool:
        return self.endpoint and self.endpoint.socket.open

    def update_items(self):
        # just to be safe - we might still have an inventory from a different room
        if not self.is_connected():
            return

        self.server_msgs.append(encode([{"cmd": "ReceivedItems", "index": 0, "items": self.full_inventory}]))

    def on_package(self, cmd: str, args: dict):
        if cmd == "RoomInfo":
            #prepare roominfo packet to send to game client when it connects to our proxy
            self.seed_name = args["seed_name"]
            self.room_info = encode([args])
        elif cmd == "Connected":
            #same as roominfo except with the connected packet
            self.connected_msg = encode([args])
            if self.awaiting_info:
                self.server_msgs.append(self.room_info)
                self.update_items()
                self.awaiting_info = False
            self.connected = True
            self.authenticated = True
        elif cmd == "ReceivedItems":
            #if index is 0 its the receiveditems packet sent on connect which contains all collected items thus far
            if args["index"] == 0:
                self.full_inventory.clear()
            for item in args["items"]:
                self.full_inventory.append(item)
            self.server_msgs.append(encode([args]))
        #adjusted printjson packet, only sends over assembled text message and the type
        elif cmd == "PrintJSON":
            txtmsg = ""
            if args.get("type") == "Collect":
                txtmsg = f"{self.player_names[args["slot"]]} collected all of their items!"
                self.just_collected = args["slot"]
            if (args.get("type") == "ItemSend" and self.slot_concerns_self(args["item"].player) 
                and args["item"].player != self.just_collected and not self.slot_concerns_self(args["receiving"])):
                item_name = self.item_names.lookup_in_game(args["item"].item, self.slot_info[args["receiving"]].game)
                txtmsg = f"Found {self.player_names[args["receiving"]]}'s {item_name}!"
            if args.get("type") == "Goal":
                txtmsg = f"{self.player_names[args["slot"]]} reached their goal!"
            if txtmsg:
                self.server_msgs.append(encode([{
                    "cmd": cmd,
                    "type": args.get("type"),
                    "text": txtmsg
                }]))
        #send over all other received data from the server in full
        else:
            self.server_msgs.append(encode([args]))

    def run_gui(self):
        from kvui import GameManager

        class PTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Pizza Tower Client"

        self.ui = PTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def proxy(websocket, path: str = "/", ctx: PTContext = None):
    ctx.endpoint = Endpoint(websocket)
    try:
        await on_client_connected(ctx)
        if ctx.is_proxy_connected():
            async for data in websocket:
                if DEBUG:
                    logger.info(f"Incoming message: {data}")
                if not ctx.is_connected() and ctx.authenticated:
                    text = encode([{"cmd": "ProxyDisconnect"}])
                    await ctx.send_msgs_proxy(text)
                    ctx.authenticated = False
                await parse_game_packets(ctx, data)
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logger.exception(e)
    finally:
        await ctx.disconnect_proxy()

async def parse_game_packets(ctx: PTContext, data):
    for msg in decode(data):
        if msg["cmd"] == "ClientPing":
            # Ensure that the client is still connected to the text client using a special packet
            text = encode([{"cmd": "ClientPong"}])
            await ctx.send_msgs_proxy(text)
        #dont send further packets if not connected with server yet
        #connected is only set to true if we've actually received the initial connection data from the server
        elif not ctx.connected:
            break
        #connection with server is handled by proxy client already, just send back the important data
        elif msg["cmd"] == "Connect":
            # Proxy is connecting, make sure it is valid
            if msg["game"] != "Pizza Tower":
                logger.info("Aborting proxy connection: game is not Pizza Tower")
                await ctx.disconnect_proxy()
                break
            #send over connection data and receiveditems if valid
            if ctx.connected_msg and ctx.is_connected():
                await ctx.send_msgs_proxy(ctx.connected_msg)
                ctx.update_items()
        elif not ctx.is_proxy_connected():
            break
        #send over any packets received from the game client to the server
        else:
            await ctx.send_msgs([msg])


async def on_client_connected(ctx: PTContext):
    if ctx.room_info and ctx.connected:
        await ctx.send_msgs_proxy(ctx.room_info)
    else:
        ctx.awaiting_info = True
        text = encode([{"cmd": "ClientPong"}])
        await ctx.send_msgs_proxy(text)


async def proxy_loop(ctx: PTContext):
    try:
        while not ctx.exit_event.is_set():
            if not ctx.is_connected():
                ctx.connected = False
            if len(ctx.server_msgs) > 0:
                for msg in ctx.server_msgs:
                    await ctx.send_msgs_proxy(msg)

                ctx.server_msgs.clear()
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.exception(e)
        logger.info("Aborting PT Proxy Client due to errors")


def launch(*launch_args: str):
    async def main():
        parser = get_base_parser()
        args = parser.parse_args(launch_args)

        ctx = PTContext(args.connect, args.password)
        logger.info("Starting Pizza Tower proxy server")
        ctx.proxy = websockets.serve(functools.partial(proxy, ctx=ctx),
                                     host="localhost", port=12312, ping_timeout=999999, ping_interval=999999)
        ctx.proxy_task = asyncio.create_task(proxy_loop(ctx), name="ProxyLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.proxy
        await ctx.proxy_task
        await ctx.exit_event.wait()

    Utils.init_logging("PTClient")
    # options = Utils.get_options()

    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
