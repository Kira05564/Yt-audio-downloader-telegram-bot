import os
import yt_dlp
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# === CONFIG ===
API_ID = 22545644  # replace with your api_id
API_HASH = "5b8f3b235407aea5242c04909e38d33d"
BOT_TOKEN = "8447148137:AAEaEu_JYaRfMd-uZjr5gDQpFA_hzOmemSs"

app = Client("kira_audio_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

users = set()

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    users.add(message.chat.id)
    await message.reply("🎧 *Welcome to Ultra HD YT Audio Bot!*\n\nUse `/yta <youtube link>` to get audio.\n\n__Powered by Kira Bots__")

@app.on_message(filters.command("yta"))
async def yta_handler(client, message: Message):
    users.add(message.chat.id)

    if len(message.command) < 2:
        return await message.reply("❌ *Please provide a YouTube link!*\nExample: `/yta https://youtu.be/...`")

    url = message.command[1]

    msg = await message.reply("🔄 Downloading... Please wait!")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Audio")
        
        await msg.edit("✅ Uploading Audio...")

        await message.reply_audio("audio.mp3", title=title, caption=f"🎶 *{title}*\n\n__Powered by Kira Bots__")
        os.remove("audio.mp3")

    except Exception as e:
        await msg.edit(f"❌ Failed:\n`{e}`")

@app.on_message(filters.command("broadcast"))
async def broadcast(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ *Please enter a message to broadcast.*")

    text = message.text.split(None, 1)[1]
    sent, fail = 0, 0

    for uid in list(users):
        try:
            await app.send_message(uid, text)
            sent += 1
        except:
            fail += 1

    await message.reply(f"📣 *Broadcast Done!*\n✅ Sent: {sent}\n❌ Failed: {fail}")

app.run()