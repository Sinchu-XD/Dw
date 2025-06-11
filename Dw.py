from playwright.sync_api import sync_playwright
import requests
import uuid
import os

# Use your valid authenticated headers here if needed for download
HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def extract_video_url(page_url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(page_url, wait_until="networkidle")
        # Wait for the download link/button to load in the DOM
        page.wait_for_selector('a[href*=".mp4"], a.download-button', timeout=20000)
        # Extract first link that ends in .mp4
        links = page.eval_on_selector_all(
            'a[href*=".mp4"]',
            'els => els.map(el => el.href)'
        )
        browser.close()

        if links:
            return links[0]
        else:
            raise RuntimeError("No .mp4 link found on the page")

def download_video(video_url: str, save_name: str = None):
    print(f"📥 Downloading from: {video_url}")
    resp = requests.get(video_url, headers=HEADERS, stream=True, timeout=60)
    resp.raise_for_status()

    if not save_name:
        cd = resp.headers.get("Content-Disposition", "")
        if "filename=" in cd:
            save_name = cd.split("filename=")[-1].strip().strip('"')
        else:
            save_name = f"video_{uuid.uuid4().hex[:8]}.mp4"

    with open(save_name, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✅ Saved video as: {save_name}")
    return save_name

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.diskwala.com/app/6841bb76b42bb37213c22007"
    try:
        video_url = extract_video_url(url)
        print("🔗 Found direct URL:", video_url)
        download_video(video_url)
    except Exception as e:
        print("❌ Failed:", e)
