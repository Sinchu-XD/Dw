import asyncio
from playwright.async_api import async_playwright
import re

URL = "https://www.diskwala.com/app/683aa235b42bb37213a69dd4"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Opening URL: {URL}")
        
        def looks_like_video_url(url):
            return re.search(r'\.(mp4|m3u8)(\?|$)', url)

        # Log all requests with video extensions
        page.on("request", lambda request: print(f"Request: {request.url}") if looks_like_video_url(request.url) else None)

        # Also log responses with video extensions (sometimes redirected URLs)
        page.on("response", lambda response: print(f"Response: {response.url}") if looks_like_video_url(response.url) else None)

        await page.goto(URL)

        # Wait to capture all requests
        await page.wait_for_timeout(15000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
