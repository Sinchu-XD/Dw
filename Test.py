import asyncio
from playwright.async_api import async_playwright
import requests
import os
import sys

DOWNLOAD_FOLDER = "downloads"

async def get_download_links(url):
    download_urls = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True to hide browser
        page = await browser.new_page()

        # Capture requests for video files
        async def on_request(request):
            if request.url.endswith(('.mp4', '.mkv', '.avi', '.mov')):
                print("🔗 Found downloadable URL:", request.url)
                download_urls.append(request.url)

        page.on("request", on_request)

        print(f"🌐 Going to {url}")
        await page.goto(url, wait_until="networkidle")

        try:
            print("⏳ Waiting for and clicking Download button...")
            await page.wait_for_selector('button:has-text("Download")', timeout=10000)
            await page.click('button:has-text("Download")')
            await page.wait_for_timeout(5000)  # wait for the download link or video request to load
        except Exception as e:
            print("⚠️ Could not find/click Download button:", e)

        # Give some extra time for requests to fire
        await page.wait_for_timeout(5000)

        await browser.close()

    return download_urls


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
