import os
import requests
import asyncio
import websockets
import json
from unsync import unsync

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

@unsync
async def producer(ws):
    # msg = '{"service":"event","action":"help"}'
    msg = f'{{"service":"event","action":"subscribe","characters":[{",".join(players.keys())}],"worlds":["all"],"eventNames":["Death"]}}'
    print(msg)
    await ws.send(msg)

@unsync
async def consumer(ws):
    recv = True
    while recv != None:
        recv = await ws.recv()
        # converts received message to json
        recv = json.loads(recv)
        if "payload" in recv and recv["payload"]["character_id"] in players and recv["payload"]["attacker_character_id"] in players:
            print(recv)
            # if not suicide
            if players[recv["payload"]["character_id"]] != players[recv["payload"]["attacker_character_id"]]:
                players[recv["payload"]["character_id"]]["deaths"] += 1
                players[recv["payload"]["attacker_character_id"]]["kills"] += 1
            print(players[recv["payload"]["character_id"]]["name"], players[recv["payload"]["character_id"]]["deaths"])
            print("Name\t".expandtabs(27), "Kills\tDeaths\tGuild")
            for player in players.values():
                print(f'{player["name"]}\t'.expandtabs(27), f'\t{player["kills"]}\t{player["deaths"]}\t{player["outfit_alias"]}')

@unsync
async def handler():
    uri = f"wss://push.planetside2.com/streaming?environment=ps2&service-id=s:{SERVICE_ID}"
    async with websockets.connect(uri) as ws:
        producer_task = asyncio.ensure_future(producer(ws))
        consumer_task = asyncio.ensure_future(consumer(ws))
        await producer_task
        await consumer_task

@unsync
def get_outfit_id_from_tag(tag):
    outfit_info = get_outfit_from_tag(tag)
    return outfit_info["outfit_id"]

@unsync
def get_outfit_from_tag(tag):
    tag = tag.lower()
    req = requests.get(f"http://census.daybreakgames.com/get/ps2:v2/outfit/?alias_lower={tag}")
    return req.json()["outfit_list"][0]

@unsync
def get_online_players(outfit):
    outfit_id = outfit["outfit_id"]
    req = requests.get(f"http://census.daybreakgames.com/get/ps2:v2/outfit_member/?outfit_id={outfit_id}&c:limit=9999&c:resolve=online_status,character_name")
    player_ids = []
    # goes thorugh each player in outfit
    for player in req.json()["outfit_member_list"]:
        if player["online_status"] != "0":
            player_ids.append(player["character_id"])
            # appends to global dict
            players[str(player["character_id"])]= {"name": player["character"]["name"]["first"],
                                                    "kills": 0,
                                                    "deaths": 0,
                                                    "outfit": outfit["name"],
                                                    "outfit_alias": outfit["alias"]}
    return player_ids
    
tag1 = "xlla"
tag2 = "geyx"
team = get_online_players(get_outfit_from_tag(tag1).result()).result()
print(team)
team = get_online_players(get_outfit_from_tag(tag2).result()).result()
print(team)


# asyncio.get_event_loop().run_until_complete(handler())
handler().result()


# get players from outfit using requests
# set up stream with players