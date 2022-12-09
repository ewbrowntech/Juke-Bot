import discord
intents = discord.Intents.default()

class JukeBotClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print("Username: " + client.user.name)
        print("User ID: " + str(client.user.id))
        print("Bot Token: " + token)
        print('------')

    async def on_message(self, message):
        if message.author.id == client.user.id: # Do not process messages sent by the bot itself
            return
        print("Message: " + message.content)
        if message.content.startswith('!hello'):
            await message.channel.send('Hello!')

with open('bot_token.txt', 'r') as file:
    token = file.read()

client = JukeBotClient(intents=intents)
client.run(token)
