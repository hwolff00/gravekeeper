import asyncio
from rctogether import bots, RestApiSession, messages, api
import pickle
import re
import random
import time

# Home (Where HopBot starts.)


Home = {"x": 6, "y": 1}
Away = {"x": 4, "y": 4}
#
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


tour = random.choice(Tour_positions)

#
# def unpickle(name):
#     with open('obj/' + name + '.pkl', 'rb') as f:
#         return pickle.load(f)
#
# tokenized_dic = unpickle("tagged")
#
# TECH = ["unit tests", "b-trees", "linked lists", "Schemas", "bytes", "booleans",
#         "chars", "nodes", "vertices", "arrays", "constants", 'Docker containers',
#         "black-box testing"]
#
# BAD_TECH = ["memory leaks", "HTTP 404 ERROR: Not Founds", "SQL injections",
#             "bad cron jobs", "data integrity errors", "constraint violations",
#             "illegal access", "illegal operations", "HTTP 418: I'm a teapots",
#             "dead locks", "live locks", "syntax errors", "stack overflows",
#             "buffer overruns", "side channel vulnerabilities",
#             "underflow errors", "segmentation faults", "broken pipes",
#             "index out of bounds", "user errors", "metaclass conflicts",
#             "cd: /home: No such file or directory issues", "timeout issues",
#            "race conditions", "type mismatches", "inexhaustive pattern matches",
#            "redundant pattern matches", "compiler errors"]
#
# WOW = ["The Big Moments Are Going To Come. You Can't Help That. It's What You Do Afterwards That Counts.",
#          "I May Be Dead, But I'm Still Pretty.", "The Hardest Thing In This World Is To Live In It. Be Brave. Live… For Me.",
#          "I laugh in the face of danger. Then I hide until it goes away.",
#          "Sometimes the most adult thing you can do is ask for help when you need it.",
#          "There’s more than one way to skin a cat, and I happen to know that’s factually true."]
#
# SCRIPTS = ["Our life was all {} until it became {}.".format(t, b),
# "{} {} the {} {} {}. Finally there would be no more {}!".format(Pronoun.capitalize(), Past_Verb, t, IN.lower(), Second_Plural_Noun,  b),
# "{} was born out of {} and {} due to {}.".format(name, t, Past_Verb, b),
# "{} {} {} but it also {} them.".format(b.capitalize(), Past_Verb, name, Second_Past_Verb)
# ]
#
# Past_Verb = random.choice(tokenized_dic["VBN"])
# Second_Past_Verb = random.choice(tokenized_dic["VBN"])
# Pronoun = random.choice(tokenized_dic["PRP"])
# Plural_Noun = random.choice(tokenized_dic["NNS"])
# Second_Plural_Noun = random.choice(tokenized_dic["NNS"])
# DT = random.choice(tokenized_dic["DT"])
# IN = random.choice(tokenized_dic["IN"])
# t = random.choice(TECH)
# b = random.choice(BAD_TECH)
# name = "TestbotNewName"

#
# def story(name):
#     return random.choice(SCRIPTS)
#
# def words_of_wisdom():
#     return random.choice(WOW)

#TODO fix speeches formatting
#TODO make it so HopBot only speaks when mentioned

#dict_keys(['id', 'type', 'pos', 'emoji', 'direction', 'can_be_mentioned', 'app', 'name', 'display_name', 'message'])
async def main():
    async with RestApiSession() as session:
        for i in await bots.get(session):
            if i['emoji'] == "🧛":
                print("Found Hop!")
                #print(i["id"])
                if i["pos"] == Home:
                    #await messages.send(session, i["id"], "🦇")
                    await bots.update(session, i["id"], tour["pos"])
                    print(tour["name"])
                    time.sleep(6)
                    await bots.update(session, i["id"], Home)
                if i["pos"] != Home:
                    await bots.update(session, i["id"], Home)
                    #await self.particle.update(PARTICLE_HOME)


asyncio.run(main())
