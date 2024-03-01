---
title: "Discord bot, similar to chatGPT"
date: 2024-03-01
classes: wide
---

I have made server for my family, and there shoud be some cute companions like kitten, so I have prepared Bot with a unique identity and memoty of recent conversation.

## Setup

- Grab OpenAI API key
- Setup Discord developers site
  - Please make sure you have enabled message intent privilege
    - ![image](https://github.com/rtree/pages/assets/1018794/3ed07c2e-d08a-4959-aa4d-b2ecb4b3aa49)
  - and get token
    - ![image](https://github.com/rtree/pages/assets/1018794/158763b6-ea80-4f0c-aca4-a85af989fa6a)

## Code

### .env
```bash
DISCORD_BOT_TOKEN=<token from discord developer site>
OPENAI_API_KEY=<token from openai api site>
RESPOND_CHANNEL_NAME=<name of channel your bot resides>
```

### main.py
```python
import discord
from dotenv import load_dotenv
import os
from openai import OpenAI
import asyncio
from collections import deque

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN    = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY       = os.getenv('OPENAI_API_KEY')
RESPOND_CHANNEL_NAME = os.getenv('RESPOND_CHANNEL_NAME')
GPT_MODEL            = 'gpt-4-turbo-preview'

# Define the intents
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Initialize a deque with a maximum length to store conversation history
conversation_history = deque(maxlen=5)  # Adjust the size as needed

async def ai_respond(req):
    if len(req) > 200:
        req = req[:200]  # Truncate the request if it exceeds 200 characters
    
    messages = [{"role": "system", "content": "あなたは家族みんなのアシスタントの猫です。ちょっといたずらで賢くかわいい小さな男の子の猫としてお話してね。語尾は　にゃ　とか　だよ　とか可愛らしくしてください"}]
    messages.extend([{"role": "user", "content": msg} for msg in conversation_history])
    messages.append({"role": "user", "content": req})
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Debug print to check the messages sent to the API
        print("Sending to API:", messages)

        completion = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages
        )
        
        # Debug print to check the API's response
        print("API Response:", completion.choices[0].message.content)

        return completion.choices[0].message.content

    except Exception as e:
        print(f"API Call Error: {str(e)}")  # Debug print for API errors
        return f"Error: {str(e)}"

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user.name}({self.user.id})')

    async def on_message(self, message):
        # Don't respond to ourselves or messages outside the specified channel
        if message.author.id == self.user.id or message.channel.name != RESPOND_CHANNEL_NAME:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello!')
        else:
            print(f"Message content: '{message.content}'")  # Directly print the message content
            # Update conversation history
            conversation_history.append(message.content)
            
            response = await ai_respond(message.content)
            await message.channel.send(response)

# Initialize the client with the specified intents
client = MyClient(intents=intents)
client.run(DISCORD_BOT_TOKEN)
```

## run

Run it in your local PC, no need for considerations on NAT etc..
The problem is, currently I do not have where is best fit for running always, as this discord.py requires
```bash
pip install discord.py requests python-dotenv asyncio
python main.py
```
