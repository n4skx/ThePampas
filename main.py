from json import dumps, loads
from sanic import Sanic, Request, Websocket

# Fake-db
database = {"users": {}}

# App
app = Sanic("HiddenClub")

# Routes
app.static("/", "static/index.html")

@app.websocket("/ws")
async def websocket_handler(r: Request, ws: Websocket):
    async for packet in ws:
        try:
            packet = loads(packet)

            match packet["packet_type"]:
                case "join":
                    # Mini checks
                    if not packet["packet_data"] or not packet["packet_data"]["username"]:
                        return ws.send(dumps({
                            "error": 1,
                            "message": "Invalid packet, please check docs for packets"
                        })) 

                    username = str(packet["packet_data"]["username"]).replace(" ", "_")

                    # Already present user with that username
                    if username in database["users"].items():
                        return ws.send(dumps({
                            "error": 1,
                            "message": "User already present!"
                        })) 
                    

                case "message":
                    pass
        except:
            pass