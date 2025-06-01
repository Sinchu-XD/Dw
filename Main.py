import asyncio
from playwright.async_api import async_playwright
import requests

VIDEO_ID = "683aa235b42bb37213a69dd4"  # Replace with any DiskWala ID
URL = f"https://www.diskwala.com/app/{VIDEO_ID}"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Opening URL: {URL}")
        await page.goto(URL)

        # Wait for JS to load and API to be called
        await page.wait_for_timeout(3000)

        # Intercept the temp_info API response
        async def handle_response(response):
            if "temp_info" in response.url and response.status == 200:
                try:
                    data = await response.json()
                    print(f"\n✅ File Info:\n{data}\n")
                    file_url = data.get("data", {}).get("file_url")

                    if file_url:
                        print(f"🎯 Direct File URL: {file_url}")

                        # Download the file
                        download_file(file_url, VIDEO_ID + ".mp4")
                    else:
                        print("❌ File URL not found in response.")
                except Exception as e:
                    print(f"❌ Failed to parse JSON: {e}")

        page.on("response", handle_response)

        # Reload to catch the API call
        await page.reload()
        await page.wait_for_timeout(5000)

        await browser.close()


def download_file(url, filename):
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
