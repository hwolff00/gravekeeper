import eventlet

eventlet.monkey_patch()

import time
import logging
import traceback
import random
import rctogether
import pickle
import re
import datetime
from collections import defaultdict

#logging.basicConfig(level=logging.INFO)

# Home (Where HopBot starts.)

HOME = {"x": 6, "y": 1}

TOUR_POSITIONS = [{"name": "emma-bot", "x": 4, "y": 4},
{"name": "the furthest emma-bot", "x": 18, "y": 4},
{"name": "Testbot2000", "x": 1, "y": 18},
{"name": "TestbotNewName", "x": 5, "y": 22}]


TARGETS = {}
ROCKET_LOCATION = None


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
         "I May Be Dead, But I'm Still Pretty.", "The Hardest Thing In This World Is To Live In It. Be Brave. Live… For Me.",
         "I laugh in the face of danger. Then I hide until it goes away.",
         "Sometimes the most adult thing you can do is ask for help when you need it.",
         "There’s more than one way to skin a cat, and I happen to know that’s factually true."]

# SCRIPTS = ["Our life was all {} until it became {}.".format(t, b),
# "{} {} the {} {} {}. Finally there would be no more {}!".format(Pronoun.capitalize(), Past_Verb, t, IN.lower(), Second_Plural_Noun,  b),
# "{} was born out of {} and {} due to {}.".format(name, t, Past_Verb, b),
# "{} {} {} but it also {} them.".format(b.capitalize(), Past_Verb, name, Second_Past_Verb)
# ]

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


# def story(name):
#     return random.choice(SCRIPTS)
#
# def words_of_wisdom():
#     return random.choice(WOW)
#
def response_handler(commands, pattern):
    def handler(f):
        commands.append((pattern, f))
        return f
    return handler

class Gravekeeper:
    COMMANDS = []

    def __init__(self):
        self.Hop = None
        self.processed_message_dt = datetime.datetime.utcnow()

        for bot in rctogether.get_bots():
            if bot["emoji"] == "🧛‍":
                print("Found Hop!")
                self.Hop = rctogether.Bot(bot, print)
            else:
                if bot.get("message"):
                    owner_id = bot["message"]["mentioned_entity_ids"][0]

    def undying(self):
        if not self.Hop:
            self.Hop = subscription.create_bot(
                name = "HopBot",
                emoji = "🧛‍",
                x = HOME["x"],
                y = HOME["y"],
                can_be_mentioned=True,
                handle_update=print,
            )

    # def get_by_name(self, animal_name):
    #     for animal in self.available_animals.values():
    #         if animal.name == animal_name:
    #             return animal
    #     return None

    # def random_available_animal(self):
    #     return random.choice(list(self.available_animals.values()))
    #
    # def random_owned(self, owner):
    #     return random.choice(self.owned_animals[owner['id']])

    def send_message(self, recipient, message_text, sender=None):
        sender = sender or self.Hop
        rctogether.send_message(
            sender.id, f"@**{recipient['person_name']}** {message_text}"
        )


    # @response_handler(COMMANDS, "adopt (a|an|the|one)? ([A-Za-z-]+),? please")
    # def handle_adoption(self, adopter, match):
    #     animal_name = match.groups()[1]
    #
    #     if animal_name == "horse":
    #         return "Sorry, that's just a picture of a horse."
    #
    #     if animal_name == "genie":
    #         return "You can't adopt me. I'm not a pet!"
    #
    #     animal = self.get_by_name(animal_name)
    #
    #     if not animal:
    #         alternative = self.random_available_animal().name
    #         return f"Sorry, we don't have {a_an(animal_name)} at the moment, perhaps you'd like {a_an(alternative)} instead?"
    #
    #     self.send_message(adopter, NOISES.get(animal.emoji, '💖'), animal)
    #
    #     rctogether.update_bot(
    #         animal.id, {"name": f"{adopter['person_name']}'s {animal.name}"}
    #     )
    #     del self.available_animals[position_tuple(animal.bot_json["pos"])]
    #     self.owned_animals[adopter["id"]].append(animal)
    #
    #     return None

    @response_handler(COMMANDS, r"word")
    def words_of_wisdom(self, adopter, match):
        return random.choice(WOW)

    @response_handler(COMMANDS, "thank")
    def handle_thanks(self, adopter, match):
        return random.choice(["Of course.", "❤️"])

    def handle_mention(self, adopter, message):
        for (pattern, handler) in self.COMMANDS:
            match = re.search(pattern, message["text"], re.IGNORECASE)
            if match:
                response = handler(self, adopter, match)
                if response:
                    self.send_message(adopter, response)
                return

        self.send_message(
            adopter, "I don't understand the question and I won't respond."
        )

    def handle_entity(self, entity):
        if entity["type"] == "Avatar":
            message = entity.get("message")

            if message and self.Hop.id in message["mentioned_entity_ids"]:
                message_dt = datetime.datetime.strptime(
                    message["sent_at"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if message_dt <= self.processed_message_dt:
                    print("Skipping old message: ", message)
                else:
                    self.handle_mention(entity, message)
                    self.processed_message_dt = message_dt

        # if entity["type"] == "Avatar":
        #     for animal in self.owned_animals.get(entity["id"], []):
        #         print(entity)
        #         position = offset_position(entity["pos"], random.choice(DELTAS))
        #         print(f"Moving {animal} to {position}")
        #         animal.update(position)


if __name__ == '__main__':
    gravekeeper = Gravekeeper()
    subscription = rctogether.RcTogether(callbacks=[gravekeeper.handle_entity])
    subscription.block_until_done()
