import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def dump_and_scrape(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        video_url = None

        # Intercept .mp4 or video requests
        async def on_response(response):
            nonlocal video_url
            if ".mp4" in response.url and "blob:" not in response.url:
                print(f"🎯 Found Video URL: {response.url}")
                video_url = response.url

        page.on("response", on_response)

        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000)

        # Save HTML for reference
        html = await page.content()
        with open("diskwala_download_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ Page HTML dumped to diskwala_download_page.html")

        await browser.close()

        # Extract info from HTML
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
            # Optional: Auto download
            import requests
            filename = file_name.replace(" ", "_") + ".mp4"
            with requests.get(video_url, stream=True) as r:
                r.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"✅ Video downloaded as {filename}")
        else:
            print("❌ Video URL not found in the network traffic.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <diskwala_url>")
        sys.exit(1)
    url = sys.argv[1]
    asyncio.run(dump_and_scrape(url))
