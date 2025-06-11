import asyncio
from playwright.async_api import async_playwright

async def intercept_and_find_video(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"🔍 Opening: {url}\n")

        # Track found video URLs
        video_urls = set()

        # Capture all requests
        page.on("request", lambda request: print(f"📡 Request: {request.url}"))

        async def handle_response(response):
            try:
                rurl = response.url
                ctype = response.headers.get("content-type", "")
                if rurl.endswith((".mp4", ".m3u8")) or "video" in ctype:
                    print(f"\n🎯 Found video URL: {rurl}")
                    video_urls.add(rurl)
                elif "application/json" in ctype:
                    json_data = await response.json()
                    if any(k in str(json_data).lower() for k in ["video", "file", "url"]):
                        print(f"\n📦 JSON from {rurl}:\n{json_data}")
            except Exception:
                pass

        page.on("response", handle_response)

        await page.goto(url)
        await page.wait_for_timeout(8000)  # Wait to load dynamic video
        print("\n✅ Finished. Closing browser.")
        await browser.close()

        if video_urls:
            print("\n🧲 Possible Direct Video URLs:")
            for v in video_urls:
                print("👉", v)
        else:
            print("\n❌ No direct video URLs found. Might be behind token or dynamic JS.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <DiskWala Video URL>")
    else:
        url = sys.argv[1]
        asyncio.run(intercept_and_find_video(url))
