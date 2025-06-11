import asyncio
from playwright.async_api import async_playwright

TARGET_URL = "https://www.diskwala.com/app/6841bb76b42bb37213c22007"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Headless False to render everything
        context = await browser.new_context()
        page = await context.new_page()

        print(f"🔍 Opening: {TARGET_URL}")
        await page.goto(TARGET_URL)

        # Wait for page to load completely
        await page.wait_for_load_state("networkidle")

        # Optional: Click on download button if it exists
        try:
            print("🖱️ Trying to click Download button...")
            await page.click('text=Download', timeout=10000)
        except Exception:
            print("⚠️ Download button not found or click failed")

        # Monitor network requests
        def log_video_requests(request):
            url = request.url
            headers = request.headers
            if (
                url.endswith(".mp4")
                or "video" in headers.get("accept", "")
                or "video" in headers.get("content-type", "")
            ):
                print(f"\n🎯 Video Request URL: {url}\n")

        page.on("request", log_video_requests)

        print("⏳ Waiting for network activity to reveal the video URL...")
        await asyncio.sleep(15)  # Adjust as needed

        await browser.close()
        print("✅ Done.")

asyncio.run(main())
