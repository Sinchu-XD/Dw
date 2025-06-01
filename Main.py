import asyncio
from playwright.async_api import async_playwright
import re

async def get_video_url(diskwala_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Opening URL: {diskwala_url}")
        await page.goto(diskwala_url)

        # Wait for JS to fully load
        await page.wait_for_load_state('networkidle')

        # Extract fileInfo using JavaScript object from global JS context
        try:
            data = await page.evaluate("""() => {
                return window.__NUXT__.state[1].data[0]
            }""")
        except Exception as e:
            print("❌ Failed to extract video metadata:", e)
            return

        if not data or 'fileInfo' not in data:
            print("❌ Video metadata not found.")
            return

        file_info = data['fileInfo']
        uploader = data.get('uploader', {})

        print("\n✅ File Info:")
        print(file_info)

        u_id = file_info.get('u_id')
        file_name = file_info.get('name')
        extension = file_info.get('extension', 'mp4')

        # Clean the filename (DiskWala sometimes obfuscates it)
        safe_name = re.sub(r'[^\w\-_.]', '', file_name)

        # Construct CDN URL
        cdn_url = f"https://cdn.diskvideos.com/videos/{u_id}/{safe_name}.{extension}"

        print(f"\n✅ Possible Video URL:\n{cdn_url}")

        # Optional: verify URL by opening in new tab
        video_check = await context.new_page()
        try:
            response = await video_check.goto(cdn_url)
            if response and response.status == 200:
                print("\n🎉 Direct Video URL is valid and ready to download.")
            else:
                print("\n⚠️ Video URL might be invalid or expired.")
        except Exception as e:
            print("\n❌ Error verifying video URL:", e)

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <DiskWala Video URL>")
    else:
        url = sys.argv[1]
        asyncio.run(get_video_url(url))
