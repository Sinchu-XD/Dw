import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def dump_and_scrape(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        page.on("console", lambda msg: print(f"Console: {msg.type}: {msg.text}"))
        page.on("request", lambda request: print(f"Request: {request.method} {request.url}"))
        page.on("response", lambda response: print(f"Response: {response.status} {response.url}"))

        print(f"Opening URL: {url}")
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(8000)

        html = await page.content()
        with open("diskwala_download_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ Page HTML dumped to diskwala_download_page.html")

        soup = BeautifulSoup(html, "html.parser")
        file_name = soup.find_all('p', class_='MuiTypography-body1')
        file_name = file_name[0].text if file_name else 'Not found'
        file_type = soup.find('span', class_='MuiTypography-caption')
        file_type = file_type.text if file_type else 'Not found'
        uploader = soup.find_all('h6', class_='MuiTypography-h6')
        uploader = uploader[1].text.replace("File By: ", "") if len(uploader) > 1 else 'Not found'

        print(f"\n📄 File Info:\nFile Name: {file_name}\nFile Type: {file_type}\nUploaded By: {uploader}")

        # Try <video> src
        try:
            video_src = await page.eval_on_selector("video", "el => el.src")
        except Exception:
            video_src = None

        # If not found, try <video><source> src
        if not video_src:
            try:
                video_src = await page.eval_on_selector("video source", "el => el.src")
            except Exception:
                video_src = None

        if video_src:
            print(f"\n🎬 Video src found: {video_src}")
        else:
            print("❌ No video src found in <video> or <source> tags.")

        await page.screenshot(path="page_screenshot.png", full_page=True)
        print("📸 Full page screenshot saved as page_screenshot.png")

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <diskwala_url>")
        sys.exit(1)
    url = sys.argv[1]
    asyncio.run(dump_and_scrape(url))
