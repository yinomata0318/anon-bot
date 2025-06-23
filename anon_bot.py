import discord
import os
import json
import asyncio

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.dm_messages = True

client = discord.Client(intents=intents)

MESSAGES_FILE = "messages.json"

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r") as f:
        return json.load(f)

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f)

async def send_unsent_messages():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    messages = load_messages()
    unsent = [m for m in messages if not m["sent"]]
    if unsent:
        for m in unsent:
            await channel.send(f"📩 **匿名メッセージ:**\n{m['content']}")
        for m in messages:
            m["sent"] = True
        save_messages(messages)
    await client.close()

if __name__ == "__main__":
    client.loop.create_task(send_unsent_messages())
    client.run(TOKEN)

