import os
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from playwright.async_api import async_playwright

# Telegram API credentials
API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b" 
BOT_TOKEN = "7570465536:AAEXqxZ2iIcMni5E5MpCIW_RvmJTvY2HcTI"

# Download directory
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Global flag for concurrent download control
active_download = False

# Telegram Bot Initialization
app = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to extract real download link using Playwright
async def get_direct_link(terabox_url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(terabox_url)

        # Replace this with actual selector used by TeraBox for the real download button
        DOWNLOAD_SELECTOR = "a.download-btn"

        try:
            download_el = await page.wait_for_selector(DOWNLOAD_SELECTOR, timeout=15000)
        except Exception:
            await browser.close()
            raise RuntimeError("❌ Could not find Download button on TeraBox page.")

        file_url = await download_el.get_attribute("href")
        await browser.close()

        if not file_url:
            raise RuntimeError("❌ Download button had no href attribute")

        return file_url

# Function to download the file using aiohttp
async def download_file(session: aiohttp.ClientSession, url: str, dest: str):
    async with session.get(url) as resp:
        if resp.status != 200:
            raise RuntimeError(f"❌ Failed to download file: {resp.status}")
        with open(dest, "wb") as f:
            while True:
                chunk = await resp.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)

# Command handler for /get
@app.on_message(filters.command("get") & filters.private)
async def start_download(client: Client, message: Message):
    global active_download

    if active_download:
        await message.reply_text("🚫 Another download is in progress. Try again later.")
        return

    text = message.text.split()
    if len(text) != 2:
        await message.reply_text("❌ Usage: /get <terabox_share_link>")
        return

    url = text[1]
    if "terabox.com" not in url:
        await message.reply_text("❌ That doesn’t look like a TeraBox link.")
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

    active_download = False

# Run the bot
app.run()
