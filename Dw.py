import asyncio
from playwright.async_api import async_playwright

async def intercept_requests(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=False for debugging
        context = await browser.new_context()
        page = await context.new_page()

        print(f"🌐 Opening: {url}")

        # Intercept requests
        page.on("request", lambda request: print(f"[REQ] {request.method} - {request.url}"))

        # Intercept responses
        async def handle_response(response):
            try:
                r_url = response.url
                content_type = response.headers.get("content-type", "")

                if r_url.endswith((".mp4", ".m3u8")):
                    print(f"✅ Video Link Found: {r_url}")
                elif "application/json" in content_type:
                    json_data = await response.json()
                    if any(k in str(json_data).lower() for k in ["file", "video", "url"]):
                        print(f"[JSON] From {r_url}")
                        print(json_data)
            except Exception:
                pass

        page.on("response", handle_response)

        # Listen to console logs (some blobs are printed)
        page.on("console", lambda msg: print(f"[CONSOLE] {msg.type}: {msg.text}"))

        # Go to the main page
        await page.goto(url, wait_until="networkidle")

        # Try scanning iframe
        iframes = page.frames
        print(f"🔍 Found {len(iframes)} frame(s)")

        for frame in iframes:
            try:
                content = await frame.content()
                if ".mp4" in content or ".m3u8" in content:
                    print("🎯 Possible video found in iframe HTML")
            except:
                continue

        # Evaluate for blob or JS-loaded video
        await page.wait_for_timeout(5000)
        video_links = await page.evaluate("""
        () => {
            const links = [];
            document.querySelectorAll('video, source').forEach(el => {
                if (el.src) links.push(el.src);
            });
            return links;
        }
        """)

        if video_links:
            print("🎥 Video Tags Found:")
            for link in video_links:
                print(f"🎯 {link}")
        else:
            print("❌ No direct <video> tags found.")

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Dw.py <DiskWala Video URL>")
    else:
        asyncio.run(intercept_requests(sys.argv[1]))
