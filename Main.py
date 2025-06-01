import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import sys
import os

async def dump_html(url, filename="diskwala_download_page.html"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000)
        content = await page.content()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        await browser.close()
        print(f"✅ Page HTML dumped to {filename}")

def parse_and_download(filename="diskwala_download_page.html"):
    with open(filename, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract file name
    file_name_tag = soup.find_all('p', class_='MuiTypography-body1')
    file_name = file_name_tag[0].text.strip() if file_name_tag else 'unknown_file'

    # Extract file type
    file_type_tag = soup.find('span', class_='MuiTypography-caption')
    file_type = file_type_tag.text.strip() if file_type_tag else 'unknown_type'

    # Extract uploader name
    uploader_tag = soup.find_all('h6', class_='MuiTypography-h6')
    uploader = uploader_tag[1].text.replace("File By: ", "").strip() if len(uploader_tag) > 1 else 'unknown_uploader'

    # Extract video URL
    video_tag = soup.find('video')
    video_url = video_tag['src'] if video_tag and video_tag.has_attr('src') else None

    print(f"\n📄 File Info:")
    print(f"File Name: {file_name}")
    print(f"File Type: {file_type}")
    print(f"Uploaded By: {uploader}")

    if video_url:
        print(f"🎥 Video URL: {video_url}")
        safe_name = file_name.replace(" ", "_").replace("/", "_")
        output_file = f"{safe_name}.{file_type.split('/')[-1]}"
        download_video(video_url, output_file)
    else:
        print("❌ Video URL not found in the HTML.")

def download_video(url, filename):
    print(f"⬇️ Downloading video to {filename} ...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"✅ Download complete: {filename}")
    else:
        print(f"❌ Failed to download. HTTP {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]

    asyncio.run(dump_html(url))
    parse_and_download()
