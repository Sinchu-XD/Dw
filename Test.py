import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import sys
import os

HTML_DUMP_FILE = "diskwala_dump.html"
DOWNLOAD_FOLDER = "downloads"


async def dump_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000)
        content = await page.content()
        with open(HTML_DUMP_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        await browser.close()


def extract_details_and_download():
    with open(HTML_DUMP_FILE, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # File name
    file_name_tag = soup.find_all('p', class_='MuiTypography-body1')
    file_name = file_name_tag[0].text.strip() if file_name_tag else 'Unknown_File'

    # File type
    file_type_tag = soup.find('span', class_='MuiTypography-caption')
    file_type = file_type_tag.text.strip() if file_type_tag else 'Unknown_Type'

    # Uploader
    uploader_tags = soup.find_all('h6', class_='MuiTypography-h6')
    uploader = uploader_tags[1].text.replace("File By: ", "").strip() if len(uploader_tags) > 1 else 'Unknown'

    print("📄 File Name:", file_name)
    print("📂 File Type:", file_type)
    print("👤 Uploaded By:", uploader)

    # Attempt to find the download link
    download_link_tag = soup.find('a', string=lambda text: text and "download" in text.lower())
    download_link = download_link_tag['href'] if download_link_tag else None

    if not download_link:
        print("❌ Download link not found.")
        return

    print("🔗 Download Link Found:", download_link)

    # Create folder if not exists
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name + ".mp4")

    try:
        response = requests.get(download_link, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        with open(file_path, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    done = int(50 * downloaded / total_size)
                    sys.stdout.write(f"\r⬇️ Downloading: [{'█' * done}{'.' * (50 - done)}] {downloaded // (1024*1024)}MB")
                    sys.stdout.flush()
        print(f"\n✅ Download complete: {file_path}")
    except Exception as e:
        print("❌ Failed to download:", e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_info.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(dump_html(url))
    extract_details_and_download()
