import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def dump_and_scrape(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Change to headless=False for debugging
        context = await browser.new_context()
        page = await context.new_page()

        video_url = None
        print_logs = []

        # Log all requests
        async def on_request(request):
            if any(ext in request.url for ext in [".mp4", ".m3u8", ".ts", "blob", "/video", "cdn", ".json"]):
                print_logs.append(f"🛰️ Request: {request.method} {request.url}")

        # Log all responses
        async def on_response(response):
            if any(ext in response.url for ext in [".mp4", ".m3u8", ".ts", "blob", "/video", "cdn", ".json"]):
                print_logs.append(f"📡 Response: {response.status} {response.url}")
                try:
                    body = await response.text()
                    if ".mp4" in body:
                        video_url_candidate = body.split(".mp4")[0].split('"')[-1] + ".mp4"
                        video_url = video_url_candidate
                        print_logs.append(f"🎯 Extracted from JSON/Text: {video_url}")
                except:
                    pass

        page.on("request", on_request)
        page.on("response", on_response)

        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(8000)  # Longer wait

        # Save HTML
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

        if video_url:
            print(f"\n🎬 Video URL: {video_url}")
        else:
            print("❌ Video URL not found in the network traffic.\n🔍 Debug Log:")
            for line in print_logs:
                print(line)

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <diskwala_url>")
        sys.exit(1)
    url = sys.argv[1]
    asyncio.run(dump_and_scrape(url))
