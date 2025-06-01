import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import sys

async def dump_and_scrape(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000)

        # Grab HTML for backup/debug
        html_content = await page.content()
        with open("diskwala_download_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ Page HTML dumped to diskwala_download_page.html")

        # Try to extract video src directly from <video> or <source>
        video_src = await page.eval_on_selector("video source", "el => el.src")  # Try <source>
        if not video_src:
            video_src = await page.eval_on_selector("video", "el => el.src")  # Fallback to <video src="">

        # Get file name, type, uploader
        file_name = await page.text_content("p.MuiTypography-body1")
        file_type = await page.text_content("span.MuiTypography-caption")
        uploader = await page.text_content("h6.MuiTypography-h6:nth-of-type(2)")

        if uploader:
            uploader = uploader.replace("File By: ", "")

        print(f"\n📄 File Info:")
        print(f"File Name: {file_name or 'Not Found'}")
        print(f"File Type: {file_type or 'Not Found'}")
        print(f"Uploaded By: {uploader or 'Not Found'}")

        if video_src:
            print(f"🎥 Video URL: {video_src}")
            safe_name = (file_name or "video").replace(" ", "_").replace("/", "_")
            ext = (file_type or "mp4").split("/")[-1]
            output_file = f"{safe_name}.{ext}"
            download_video(video_src, output_file)
        else:
            print("❌ Video URL not found in the page (JS-loaded or obfuscated).")

        await browser.close()

def download_video(url, filename):
    print(f"⬇️ Downloading video to {filename} ...")
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Download complete: {filename}")
        else:
            print(f"❌ Failed to download. HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error downloading video: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(dump_and_scrape(url))
