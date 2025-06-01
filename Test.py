import asyncio
from playwright.async_api import async_playwright
import requests
import os
import sys

DOWNLOAD_FOLDER = "downloads"

async def get_download_links(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"🌐 Going to {url}")
        await page.goto(url, wait_until="networkidle")

        try:
            print("⏳ Waiting for and clicking Download button...")
            await page.wait_for_selector('button:has-text("Download")', timeout=10000)
            await page.click('button:has-text("Download")')
            await page.wait_for_timeout(3000)
        except Exception as e:
            print("⚠️ Could not find/click Download button:", e)

        # After click, check for <a> tags with download URLs
        # Try common selectors or text
        download_link = None

        # Try to find link by text containing 'Download' or ending with '.mp4'
        anchors = await page.query_selector_all('a')
        for a in anchors:
            href = await a.get_attribute('href')
            text = await a.inner_text()
            if href and ('.mp4' in href or 'download' in text.lower()):
                download_link = href
                print(f"✅ Found download link: {download_link}")
                break

        await browser.close()

        if download_link:
            return [download_link]
        else:
            return []



def download_file(url):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    local_filename = os.path.join(DOWNLOAD_FOLDER, url.split('/')[-1].split("?")[0])
    print(f"⬇️ Downloading file to {local_filename} ...")

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        done = int(50 * downloaded / total) if total else 0
                        print(f"\r[{'█'*done}{'.'*(50-done)}] {downloaded//1024}KB", end='')
        print("\n✅ Download complete!")
    except Exception as e:
        print(f"❌ Download failed: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 diskwala_downloader.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]

    links = asyncio.run(get_download_links(url))

    if not links:
        print("❌ No downloadable video links found.")
        sys.exit(1)

    print(f"⚡ {len(links)} downloadable link(s) found. Starting download...")

    for link in links:
        download_file(link)
