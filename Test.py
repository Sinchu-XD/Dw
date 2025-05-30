import asyncio
from playwright.async_api import async_playwright

async def extract_video_url(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # Wait for video tag or source
        try:
            await page.wait_for_selector("video source", timeout=10000)
            video_src = await page.get_attribute("video source", "src")
            if video_src:
                return video_src
        except Exception as e:
            print(f"Video source not found: {e}")
            return None
        finally:
            await browser.close()


async def download_video(video_url, output_file="diskwala_video.mp4"):
    import requests
    print(f"Downloading from: {video_url}")
    try:
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(output_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Video downloaded as: {output_file}")
    except Exception as e:
        print(f"Download failed: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 Dw.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]
    video_url = asyncio.run(extract_video_url(url))

    if video_url:
        asyncio.run(download_video(video_url))
    else:
        print("Failed to extract video URL.")
      
