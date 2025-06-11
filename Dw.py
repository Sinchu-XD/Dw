import asyncio
from playwright.async_api import async_playwright
from Cookies import headers as HEADERS

async def extract_video_url(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(extra_http_headers=HEADERS)
        page = await context.new_page()

        print(f"🌐 Visiting: {url}")
        
        async def on_response(response):
            try:
                ct = response.headers.get("content-type", "")
                if "application/json" in ct:
                    json_data = await response.json()
                    print(f"\n✅ JSON from {response.url}")
                    print(json_data)
            except:
                pass

        page.on("response", on_response)

        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000)
        print("✅ Done. Check above JSON for video links.")
        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Dw.py <DiskWala URL>")
    else:
        asyncio.run(extract_video_url(sys.argv[1]))
