# https://discord.com/api/oauth2/authorize?client_id=1034692587099017338&permissions=154619341888&scope=bot

import os
#from keep_alive import keep_alive , it is not important for bot
import discord
# discord.py is an asynchronous library so things are done with callbacks

import requests
# we can now do http requests

import json
import random

from replit import db

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)  # we are making connection to discord

sad_words = [
    'bitter', 'dismal', 'heartbroken', 'melancholy', 'mournful', 'pessimistic',
    'somber', 'sorrowful', 'sorry'
]  # its a list of sad words that the bot will repond to

starter_encouragement = ["cheer up ", "hang in there", "stay strong"]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():  # we are using this function to get a random quote
    response = requests.get(
        "https://zenquotes.io/api/random")  # find it in zenquotes.io api docs
    json_data = json.loads(response.text)  # find it in zenquotes.io api docs

    quote = json_data[0]['q'] + " -" + json_data[0][
        'a']  #thats how the structure of the json data is. find it by printing everything and seeing structure
    return quote


def update_encouragements(encouraging_message):

    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if (len(encouragements) > index):
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event  # event decorator/wwrapper
async def on_ready():
    print(f"we logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        print('kk')
        return
    if message.content.startswith("$inspire"):
        print(message.content)
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"] == True:
        options = starter_encouragement
        if "encouragements" in db.keys():
            options = options + list(db["encouragements"])

        if any(word in message.content for word in sad_words):
            await message.channel.send(random.choice(options))

    if message.content.startswith("$new"):
        encouraging_message = message.content.split("$new", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging word added")

    if message.content.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(message.content.split("$del", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
            await message.channel.send(encouragements)

    if message.content.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
            await message.channel.send(encouragements)

    if (message.content.startswith("$responding")):
        value = message.content.split("$responding ", 1)[1].lower()
        if (value == "true"):
            db["responding"] = True
            await message.channel.send("responding is ON!")
        else:
            db["responding"] = False
            await message.channel.send("responding is OFF!")


#keep_alive() , its just a function I used to do stuff on replit. It is not important for bot
my_secret = os.environ['TOKEN']
client.run(my_secret)
