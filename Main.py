import asyncio
from playwright.async_api import async_playwright
import json
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

        content = await page.content()

        # Try to find JSON data inside <script> tag with type="application/json" or a global variable
        # Often sites embed initial state in a <script> tag.

        # Example regex to extract JSON inside a <script> tag containing 'fileInfo'
        pattern = re.compile(r'window\.__NUXT__\s*=\s*({.*?});', re.DOTALL)
        match = pattern.search(content)

        if match:
            try:
                data = json.loads(match.group(1))
                # Look for fileInfo inside this data recursively if needed
                # Let's try to find fileInfo in the JSON keys
                file_info = None
                uploader = None

                def search_file_info(obj):
                    if isinstance(obj, dict):
                        if 'fileInfo' in obj:
                            return obj['fileInfo'], obj.get('uploader', None)
                        for v in obj.values():
                            res = search_file_info(v)
                            if res is not None:
                                return res
                    elif isinstance(obj, list):
                        for item in obj:
                            res = search_file_info(item)
                            if res is not None:
                                return res
                    return None

                result = search_file_info(data)
                if result:
                    file_info, uploader = result
                else:
                    file_info = None

                if not file_info:
                    print("❌ fileInfo not found in extracted JSON data.")
                    return

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

            except Exception as e:
                print("❌ Failed to parse JSON data:", e)
                return
        else:
            print("❌ Could not find JSON data containing video info on the page.")
            return

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <DiskWala Video URL>")
    else:
        url = sys.argv[1]
        asyncio.run(get_video_url(url))
