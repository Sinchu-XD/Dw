import asyncio
from playwright.async_api import async_playwright
import re

VIDEO_ID = "683aa235b42bb37213a69dd4"
URL = f"https://www.diskwala.com/app/{VIDEO_ID}"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Opening URL: {URL}")
        await page.goto(URL)

        video_url_found = False

        def looks_like_video_url(url):
            return re.search(r'\.(mp4|m3u8)(\?|$)', url)

        # Log any response that looks like a video
        async def handle_response(response):
            nonlocal video_url_found
            url = response.url
            if looks_like_video_url(url) and not video_url_found:
                video_url_found = True
                print(f"\n🎯 Possible Video URL Found:\n{url}\n")

                # Optional: download the video (only for direct .mp4)
                if url.endswith(".mp4"):
                    download_file(url, f"{VIDEO_ID}.mp4")

        page.on("response", handle_response)

        await page.wait_for_timeout(10000)
        await browser.close()

def download_file(url, filename):
    import requests
    print(f"⬇️ Downloading {filename} ...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ Download complete: {filename}")
    except Exception as e:
        print(f"❌ Error downloading file: {e}")

if __name__ == "__main__":
    asyncio.run(run())
