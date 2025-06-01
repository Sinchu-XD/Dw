from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os
import subprocess
import aiohttp

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b" 
BOT_TOKEN = "7570465536:AAEXqxZ2iIcMni5E5MpCIW_RvmJTvY2HcTI"  # Replace with your Bot Token

app = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

active_download = False

async def get_direct_link(terabox_url: str) -> str:
    """
    Placeholder function - in a real implementation, use Selenium or Playwright
    to extract the actual download link from TeraBox.
    For now, this simulates that step.
    """
    # TODO: Replace this with actual scraping logic
    return "https://example.com/simulated-download-file.mp4"

async def download_file(session: aiohttp.ClientSession, url: str, dest: str):
    async with session.get(url) as resp:
        if resp.status == 200:
            with open(dest, "wb") as f:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
        else:
            raise Exception(f"Download failed with status {resp.status}")

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    await message.reply_text("Send me a TeraBox link and I'll try to fetch the file.")

@app.on_message(filters.text & ~filters.command("start"))
async def handle_link(client: Client, message: Message):
    global active_download

    if active_download:
        await message.reply_text("⏳ One file at a time. Wait for the current one to finish.")
        return

    url = message.text.strip()
    if "terabox.com" not in url:
        await message.reply_text("❌ Invalid link. Send a valid TeraBox link.")
        return

    active_download = True
    await message.reply_text("🔍 Processing your TeraBox link...")

    try:
        file_url = await get_direct_link(url)
        filename = os.path.join(DOWNLOAD_PATH, file_url.split("/")[-1])

        async with aiohttp.ClientSession() as session:
            await download_file(session, file_url, filename)

        await message.reply_document(document=filename, caption="✅ Here's your file.")

        os.remove(filename)
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
    finally:
        active_download = False

app.run()
