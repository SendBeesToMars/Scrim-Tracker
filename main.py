import os
import requests
import asyncio
import websockets
import json

SERVICE_ID = os.environ.get("PS2_SERVICE_ID")

players = {}

# In order to access data across the domain boundary, one may want to use JSON Padding (jsonp).
#  To do this, append a callback attribute to the query string of the request.
# http://census.daybreakgames.com/get/ps2:v2/item/?item_id=70966&callback=foo

# r = requests.get("http://census.daybreakgames.com/s:example/xml/get/ps2:v2/character/")
# get character by name http://census.daybreakgames.com/get/ps2:v2/character/?name.first_lower=litebrite
# get outfit by tag http://census.daybreakgames.com/get/ps2:v2/outfit/?alias_lower=bhot

# r = requests.get("http://census.daybreakgames.com/get/ps2:v2/character/?name.first_lower=morka")

# print(r.status_code)
# print(r.json()["character_list"][0]["character_id"])

async def producer(ws):
    # msg = '{"service":"event","action":"help"}'
    msg = f'{{"service":"event","action":"subscribe","characters":[{",".join(players.keys())}],"worlds":["all"],"eventNames":["Death"]}}'
    await ws.send(msg)

async def consumer(ws):
    recv = True
    while recv != None:
        recv = await ws.recv()
        recv = json.loads(recv)
        # print(recv)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # players[recv["payload"]["character_id"]]["deaths"] += 1
        # print(players[recv["payload"]["character_id"]]["name"], players[recv["payload"]["character_id"]]["deaths"])
        # checks if message received is payload data
        if "payload" in recv and recv["payload"]["character_id"] in players:
            print(recv["payload"])
            players[recv["payload"]["character_id"]]["deaths"] += 1
            print(players[recv["payload"]["character_id"]]["name"], players[recv["payload"]["character_id"]]["deaths"])

async def handler():
    uri = f"wss://push.planetside2.com/streaming?environment=ps2&service-id=s:{SERVICE_ID}"
    async with websockets.connect(uri) as ws:
        producer_task = asyncio.ensure_future(producer(ws))
        consumer_task = asyncio.ensure_future(consumer(ws))
        await producer_task
        await consumer_task

def get_outfit_id_from_tag(tag):
    outfit_info = get_outfit_from_tag(tag)
    return outfit_info["outfit_id"]

def get_outfit_from_tag(tag):
    tag = tag.lower()
    req = requests.get(f"http://census.daybreakgames.com/get/ps2:v2/outfit/?alias_lower={tag}")
    return req.json()["outfit_list"][0]

def get_online_players(outfit):
    outfit_id = outfit["outfit_id"]
    req = requests.get(f"http://census.daybreakgames.com/get/ps2:v2/outfit_member/?outfit_id={outfit_id}&c:limit=9999&c:resolve=online_status,character_name")
    player_ids = []
    # goes thorugh each player in outfit
    for player in req.json()["outfit_member_list"]:
        if player["online_status"] != "0":
            player_ids.append(player["character_id"])
            players[str(player["character_id"])]= {"name": player["character"]["name"]["first"],
                                                    "kills": 0,
                                                    "deaths": 0,
                                                    "outfit": outfit["name"],
                                                    "outfit_alias": outfit["alias"]}
    return player_ids
    
online_list = get_online_players(get_outfit_from_tag("dig"))


asyncio.get_event_loop().run_until_complete(handler())


# get players from outfit using requests
# set up stream with players