import discord
from download import download_command

class JukeBotClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print("Username: " + client.user.name)
        print("User ID: " + str(client.user.id))
        print("Bot Token: " + token)
        print('------')

    async def on_message(self, message):
        if message.author.id == client.user.id:  # Do not process messages sent by the bot itself
            return
        print("Message: " + message.content)
        if message.content.startswith('!'):  # All command message shall be formatted as ![command]
            await detect_commands(message)

# Parse messages and handle any commands present
async def detect_commands(message):
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('!download'):
        await download_command(message)

# Get Discord bot token from file
with open('bot_token.txt', 'r') as file:
    token = file.read()

client = JukeBotClient(intents=discord.Intents.default())
client.run(token)
