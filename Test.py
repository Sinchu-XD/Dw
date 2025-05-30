import asyncio
from playwright.async_api import async_playwright

async def extract_video_or_iframe(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        try:
            # First try for video source
            await page.wait_for_selector("video source", timeout=5000)
            video_src = await page.get_attribute("video source", "src")
            if video_src:
                print("[+] Direct video source found.")
                return video_src
        except:
            print("[-] No direct video source found. Trying iframe...")

        try:
            iframe = await page.query_selector("iframe")
            iframe_src = await iframe.get_attribute("src")
            if iframe_src:
                print(f"[+] Iframe source found: {iframe_src}")
                return iframe_src
        except Exception as e:
            print(f"[-] Failed to get iframe: {e}")
            return None
        finally:
            await browser.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 Test.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]
    extracted = asyncio.run(extract_video_or_iframe(url))

    if extracted:
        print(f"\n✅ Extracted URL: {extracted}")
    else:
        print("\n❌ Failed to extract video or iframe.")
