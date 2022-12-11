import discord
import json
from src import responses
import time

with open('config.json', 'r') as f:
    data = json.load(f)

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if len(response) > 2000:
            # Split the response into smaller chunks of no more than 2000 characters each
            response_chunks = [response[i:i+2000]
                               for i in range(0, len(response), 2000)]
            for chunk in response_chunks:
                # Send each chunk separately
                await message.author.send(chunk) if is_private else await message.channel.send(chunk)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        await message.channel.send("**Error: I think something went wrong. Please try again later!**")
        print(e)

intents = discord.Intents.default()
intents.message_content = True

def run_discord_bot():
    TOKEN = data['discord_bot_token']

    # Set the time interval (in seconds) for resetting the connection
    RESET_INTERVAL = 21600

    # Define the client and the main loop
    client = discord.Client(intents=intents)

    while True:
        @client.event
        async def on_ready():
            print(f'{client.user} is now running!')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{username} said: '{user_message}' ({channel})")

            if user_message == '!reset':
                responses.chatbot.reset_chat()
                await message.channel.send("**Info: I have forgotten everything.**")
                print("The CHAT BOT has been successfully reset")
            elif user_message[0] == '!':
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            else:
                # Check if the bot was mentioned in the message
                if client.user in message.mentions:
                    await send_message(message, user_message, is_private=False)

        client.run(TOKEN)
		
		# Sleep for the specified interval before resetting the connection
        time.sleep(RESET_INTERVAL)