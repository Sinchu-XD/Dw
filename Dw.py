import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a DiskWala URL.")
        return

    url = sys.argv[1]
    print(f"🔍 Opening: {url}")

    video_urls = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Intercept requests to catch video URLs
        page.on("request", lambda request: log_video_request(request, video_urls))

        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(3000)

        try:
            print("🖱️ Trying to click Download button...")
            await page.click("button:has-text('Download')", timeout=5000)
        except:
            print("⚠️ Download button not found or click failed")

        print("⏳ Waiting for network activity to reveal the video URL...")
        await page.wait_for_timeout(6000)

        if video_urls:
            print("🎥 Found video URLs:")
            for link in video_urls:
                print(link)
        else:
            print("❌ No direct video URLs found. Might be behind token or dynamic JS.")

        await browser.close()

def log_video_request(request, video_urls):
    url = request.url
    if any(ext in url for ext in [".mp4", ".m3u8", ".webm"]):
        if url not in video_urls:
            video_urls.append(url)

if __name__ == "__main__":
    asyncio.run(main())
