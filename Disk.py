from pyrogram import Client, filters
from Cookies import download_video
import os

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
BOT_TOKEN = "7570465536:AAEXqxZ2iIcMni5E5MpCIW_RvmJTvY2HcTI"

bot = Client("VideoBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("👋 Send me a video link, and I'll download it for you!")

@bot.on_message(filters.text & ~filters.command("start"))
async def handle_video(_, message):
    video_url = message.text.strip()
    await message.reply("📥 Downloading video... Please wait.")

    try:
        video_path = download_video(video_url)
        if video_path:
            await message.reply_video(video_path, caption="🎉 Here's your video!")
            os.remove(video_path)
        else:
            await message.reply("❌ Failed to download video. Check the link or token.")
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

bot.run()
