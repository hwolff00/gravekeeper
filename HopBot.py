import asyncio
from rctogether import bots, RestApiSession, messages, api
from rctogether import WebsocketSubscription
import pickle
import re
import random
import datetime
import time
#-------------------------------------------------------------------------------
# Home (Where HopBot starts.)
Home = {"x": 6, "y": 1}

Tour_positions = [{"name": "emma-bot", "pos": {"x": 4, "y": 4}},
{"name": "emma-bot", "pos": {"x": 4, "y": 3}},
{"name": "emma-bot", "pos": {"x": 1, "y": 3}},
{"name": "emma-bot", "pos": {"x": 0, "y": 4}},
{"name": "emma-bot", "pos": {"x": 2, "y": 6}},
{"name": "emma-bot", "pos": {"x": 4, "y": 5}},
{"name": "the furthest emma-bot", "pos": {"x": 18, "y": 4}},
{"name": "Testbot2000", "pos": {"x": 1, "y": 18}},
{"name": "Testbot2000", "pos": {"x": 3, "y": 18}},
{"name": "Testbot2000", "pos": {"x": 1, "y": 18}},
{"name": "Testbot2000", "pos": {"x": 0, "y": 20}},
{"name": "Testbot2000", "pos": {"x": 4, "y": 20}},
{"name": "TestbotNewName", "pos": {"x": 5, "y": 22}}]

# Randomize which tour location and bot Hop will talk about
tour = random.choice(Tour_positions)
#-------------------------------------------------------------------------------
# Language section
#
def unpickle(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

tokenized_dic = unpickle("tagged")

TECH = ["unit tests", "b-trees", "linked lists", "Schemas", "bytes", "booleans",
        "chars", "nodes", "vertices", "arrays", "constants", 'Docker containers',
        "black-box testing"]

BAD_TECH = ["memory leaks", "HTTP 404 ERROR: Not Founds", "SQL injections",
            "bad cron jobs", "data integrity errors", "constraint violations",
            "illegal access", "illegal operations", "HTTP 418: I'm a teapots",
            "dead locks", "live locks", "syntax errors", "stack overflows",
            "buffer overruns", "side channel vulnerabilities",
            "underflow errors", "segmentation faults", "broken pipes",
            "index out of bounds", "user errors", "metaclass conflicts",
            "cd: /home: No such file or directory issues", "timeout issues",
           "race conditions", "type mismatches", "inexhaustive pattern matches",
           "redundant pattern matches", "compiler errors"]

WOW = ["The Big Moments Are Going To Come. You Can't Help That. It's What You Do Afterwards That Counts.",
         "I May Be Dead, But I'm Still Pretty.",
         "I laugh in the face of danger. Then I hide until it goes away.",
         "Sometimes the most adult thing you can do is ask for help when you need it.",
         "There’s more than one way to skin a cat, and I happen to know that’s factually true."]

Past_Verb = random.choice(tokenized_dic["VBN"])
Second_Past_Verb = random.choice(tokenized_dic["VBN"])
Pronoun = random.choice(tokenized_dic["PRP"])
Plural_Noun = random.choice(tokenized_dic["NNS"])
Second_Plural_Noun = random.choice(tokenized_dic["NNS"])
DT = random.choice(tokenized_dic["DT"])
IN = random.choice(tokenized_dic["IN"])
Tech = random.choice(TECH)
Bad_Tech = random.choice(BAD_TECH)

SCRIPTS = [f"Our life was all {Tech} until it became {Bad_Tech}.",
f"{Pronoun.capitalize()} {Past_Verb} the {Tech} {IN.lower()} {Second_Plural_Noun}. Finally there would be no more {Bad_Tech}!",
f"{tour['name']} was born out of {Tech} and {Past_Verb} due to {Bad_Tech}.",
f"{Bad_Tech.capitalize()} {Past_Verb} {tour['name']} but it also {Second_Past_Verb} them."
]

COMMANDS = []
#-------------------------------------------------------------------------------

def story():
    return f"{random.choice(['Ah, yes I remember', 'Did you know', 'Have I ever told you about'])} {tour['name']}: {random.choice(SCRIPTS)}"

def words_of_wisdom():
    return random.choice(WOW)

def response_handler(commands, pattern):
    def handler(f):
        commands.append((pattern, f))
        return f

    return handler

#-------------------------------------------------------------------------------
#TODO make this code less insane
#TODO add in input functionality

async def speak(session, id, message):
    await messages.send(session, id, f"@**{message['person_name']}** {story()}")

async def movement(message):
    async with RestApiSession() as session:
        for bot in await bots.get(session):
            if bot['emoji'] == "🧛":
                print("Found Hop!")
                # print(i["id"])
                if bot["pos"] == Home:
                    await speak(session, bot["id"], message)
                    await bots.update(session, bot["id"], tour["pos"])
                    # print(story())
                    time.sleep(6)
                    await bots.update(session, bot["id"], Home)
                if bot["pos"] != Home:
                    await bots.update(session, bot["id"], Home)


async def main():
    processed_message_dt = datetime.datetime.utcnow()
    async for message in WebsocketSubscription():
        for key, value in message.items():
            if type(value) is dict and 'mentioned_entity_ids' in value.keys():
                    if value['mentioned_entity_ids'] == [92348]:
                        # print(message['message']['sent_at'])
                        message_dt = datetime.datetime.strptime(message['message']['sent_at'], "%Y-%m-%dT%H:%M:%SZ")
                        if message_dt <= processed_message_dt:
                            print("Skipping old message")
                            # print(message)
                        else:
                            processed_message_dt = message_dt
                            await movement(message)



asyncio.run(main())
