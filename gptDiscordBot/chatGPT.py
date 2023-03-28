import discord
import openai
import json

client = discord.Client(intents=discord.Intents.all())

def create_config_json():
    info = input("Do you want to change info?[Y/n] (default n)\n-")
    info = info.lower()
    if info == "y":
        gptkey =  input("Enter your openai api key:\n")
        DISCORD_TOKEN = input("Enter your discord token:\n")
        

        config = {
            "discord": DISCORD_TOKEN,
            "gpt": gptkey
        }

        json_data = {
            "config": config
        }

        with open("config.json", "w") as outfile:
            json.dump(json_data, outfile)

def get_info():

    try:

        with open('config.json', 'r') as f:
            data = json.load(f)
        discord = data['config']['discord']
        gptkey = data['config']['gpt']
        print('your discord token is:', discord)
        print('your gpt API key is:', gptkey)
        return discord, gptkey
    except:
        print("you don't have discord token or gpt API key")


create_config_json()
get_info()

DISCORD_TOKEN = get_info()[0]
openai.api_key = get_info()[1]

async def ask_gpt3(question):
    prompt = f"Q: {question}\nA:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return answer


@client.event
async def on_ready():
    print(f'{client.user} adlı botunuz başarıyla giriş yaptı!')

@client.event
async def on_message(message):

    if message.author.bot:
        return
    if message.content.startswith('!ask'):
        question = message.content.split("!ask ")[1]
        answer = await ask_gpt3(question)
        await message.channel.send(answer)

client.run(DISCORD_TOKEN)
