import os
import threading
from flask import Flask
import discord
from discord.ext import commands

# 環境変数から取得（Renderの環境変数設定で登録する）
TOKEN = os.environ['TOKEN']
TARGET_CHANNEL_ID = int(os.environ['TARGET_CHANNEL_ID'])

# Discord intents（メッセージ内容を読むためにmessage_contentをTrueにする）
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

app = Flask('')  # Flaskアプリを作成

# HTTPのルートエンドポイント（Renderがポート検査するためのページ）
@app.route('/')
def home():
    return "Bot is running"

# Flaskを別スレッドで起動する関数
def run_flask():
    app.run(host="0.0.0.0", port=8080)

@bot.event
async def on_ready():
    print(f"✅ Botログイン成功: {bot.user}")

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
            "幹部でいろいろ考えていきます！\n"
            "これからもよろしく！"
        )
        await message.channel.send(thank_you_msg)

if __name__ == "__main__":
    # Flaskを別スレッドで起動
    threading.Thread(target=run_flask).start()
    # Discord Botを起動
    bot.run(TOKEN)

