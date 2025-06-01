import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from playwright.async_api import async_playwright

# —— Telegram API credentials (replace with yours) ——
API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b" 
BOT_TOKEN = "7570465536:AAEXqxZ2iIcMni5E5MpCIW_RvmJTvY2HcTI"

# Where downloaded files will live
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Prevent concurrent downloads
active_download = False

# Pyrogram Bot setup
app = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def get_downloaded_file(terabox_url: str) -> str:
    """
    Opens the TeraBox share link in a headless browser, tries multiple selectors to click a download button,
    and waits for Playwright’s download event. Saves the file locally and returns the full path.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(terabox_url)

        # List of selectors to try for triggering a download
        download_selectors = [
            "text=Downloads",       # e.g., button with text “Downloads”
            "text=Download",        # fallback if singular “Download”
            "a.download-btn",       # common class-based link
            "a.tb-download-link"    # TeraBox-specific link class
        ]

        # Attempt to click each selector until a download is captured
        for sel in download_selectors:
            try:
                async with page.expect_download() as download_info:
                    await page.click(sel)
                download = await download_info.value
                suggested = download.suggested_filename or "unknown_file"
                local_path = os.path.join(DOWNLOAD_PATH, suggested)
                await download.save_as(local_path)
                await browser.close()
                return local_path
            except Exception:
                # if this selector fails, try the next one
                continue

        # If none of the selectors triggered a download, attempt fallback to any <a> link
        try:
            link = await page.wait_for_selector("a[href$='.zip'], a[href$='.mp4'], a[href$='.rar']", timeout=15000)
            href = await link.get_attribute("href")
            await browser.close()
            if href and href.startswith("http"):
                return href
            else:
                raise RuntimeError("Fallback found no valid href")
        except Exception:
            await browser.close()
            raise RuntimeError("❌ Could not trigger or capture any download from TeraBox link (requires signup?).")

@app.on_message(filters.command("get") & filters.private)
async def start_download(client: Client, message: Message):
    """
    /get <terabox_share_link>
    """
    global active_download

    if active_download:
        await message.reply_text("🚫 Another download is in progress. Try again later.")
        return

    parts = message.text.split()
    if len(parts) != 2:
        await message.reply_text("❌ Usage: /get <TeraBox_share_link>")
        return

    share_url = parts[1]
    if "teraboxlink.com" not in share_url:
        await message.reply_text("❌ That doesn’t look like a TeraBox link.")
        return

    active_download = True
    await message.reply_text("🔍 Processing your TeraBox link… (this may take a few seconds)")

    try:
        result = await get_downloaded_file(share_url)

        # If get_downloaded_file returned a local filepath, send that file
        if os.path.isfile(result):
            await message.reply_document(document=result, caption="✅ Here’s your file.")
            os.remove(result)

        # Otherwise, we got a direct URL fallback—download via aiohttp
        else:
            import aiohttp
            local_name = os.path.join(DOWNLOAD_PATH, os.path.basename(result))
            async with aiohttp.ClientSession() as session:
                async with session.get(result) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"❌ HTTP {resp.status} when downloading fallback URL.")
                    with open(local_name, "wb") as f:
                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
            await message.reply_document(document=local_name, caption="✅ Here’s your file (via fallback).")
            os.remove(local_name)

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

    finally:
        active_download = False

# Run the bot
app.run()
