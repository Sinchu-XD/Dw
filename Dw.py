from playwright.async_api import async_playwright

async def intercept_requests(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"🔍 Opening: {url}")

        async def log_response(response):
            if "udapi.diskwala.com/api/v1/" in response.url:
                try:
                    body = await response.text()
                    print(f"\n📦 Response from {response.url}:\n{body}")
                except Exception:
                    pass

        page.on("response", log_response)
        await page.goto(url)
        await page.wait_for_timeout(7000)
        print("\n✅ Finished. Closing browser.")

        await browser.close()

import sys
if __name__ == "__main__":
    if len(sys.argv) > 1:
        import asyncio
        asyncio.run(intercept_requests(sys.argv[1]))
    else:
        print("❌ Please provide a DiskWala file URL.")
