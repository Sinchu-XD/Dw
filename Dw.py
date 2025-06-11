import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a DiskWala URL.")
        return

    url = sys.argv[1]
    print(f"🔍 Opening: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # set headless=False to see browser
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(3000)  # small wait to allow JS rendering

        try:
            print("🖱️ Trying to click Download button...")
            # Try a few possible selectors
            await page.wait_for_selector("button:has-text('Download')", timeout=7000)
            await page.click("button:has-text('Download')")
        except Exception as e:
            print("⚠️ Download button not found or click failed")
            # For debugging, take a screenshot
            await page.screenshot(path="debug.png", full_page=True)

        print("⏳ Waiting for network activity to reveal the video URL...")
        await page.wait_for_timeout(5000)  # wait for requests to happen

        print("✅ Done.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
