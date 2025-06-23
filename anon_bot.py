import os
import discord
from discord.ext import commands

# 環境変数から読み込む
TOKEN = os.environ['TOKEN']
TARGET_CHANNEL_ID = int(os.environ['TARGET_CHANNEL_ID'])

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Botログイン成功: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            await target_channel.send(f"📩 **匿名のメッセージ：**\n{message.content}")

        thank_you_msg = (
            "メッセージありがとう！\n"
            "幹部でいろいろ考えていくね！\n"
            "これからもよろしくね！"
        )
        await message.channel.send(thank_you_msg)

bot.run(TOKEN)

