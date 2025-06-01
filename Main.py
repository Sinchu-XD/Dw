import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import sys
import re

async def dump_and_scrape(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(7000)  # extra wait

        html_content = await page.content()
        with open("diskwala_download_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ Page HTML dumped to diskwala_download_page.html")

        # Now parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract File Name
        name_tag = soup.find('p', class_='MuiTypography-body1')
        file_name = name_tag.text.strip() if name_tag else 'Not Found'

        # Extract File Type
        type_tag = soup.find('span', class_='MuiTypography-caption')
        file_type = type_tag.text.strip() if type_tag else 'Not Found'

        # Extract Uploader
        uploader_tags = soup.find_all('h6', class_='MuiTypography-h6')
        uploader = uploader_tags[1].text.replace("File By: ", "").strip() if len(uploader_tags) > 1 else 'Not Found'

        print(f"\n📄 File Info:")
        print(f"File Name: {file_name}")
        print(f"File Type: {file_type}")
        print(f"Uploaded By: {uploader}")

        # Try finding video URL inside <video> or <source> or JS data
        video_url = None

        # Attempt 1: <video src="">
        video_tag = soup.find("video")
        if video_tag and video_tag.get("src"):
            video_url = video_tag["src"]

        # Attempt 2: <source src="">
        if not video_url:
            source_tag = soup.find("source")
            if source_tag and source_tag.get("src"):
                video_url = source_tag["src"]

        # Attempt 3: Raw search in JS data
        if not video_url:
            raw_urls = re.findall(r'https://[^\'" ]+\.mp4', html_content)
            if raw_urls:
                video_url = raw_urls[0]

        if video_url:
            print(f"🎥 Video URL: {video_url}")
            safe_name = file_name.replace(" ", "_").replace("/", "_")
            ext = (file_type.split("/")[-1]) if "/" in file_type else "mp4"
            output_file = f"{safe_name}.{ext}"
            download_video(video_url, output_file)
        else:
            print("❌ Video URL not found in the HTML.")

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
