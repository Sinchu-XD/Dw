import asyncio
from playwright.async_api import async_playwright

async def intercept_requests(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Opening URL: {url}")

        # Listen to all requests
        page.on("request", lambda request: print(f"Request: {request.url}"))

        # Listen to all responses
        async def handle_response(response):
            try:
                url = response.url
                if url.endswith(('.mp4', '.m3u8')):
                    print(f"Video URL found: {url}")
                elif 'application/json' in response.headers.get('content-type', ''):
                    json_data = await response.json()
                    # Check if JSON contains video links or file info
                    if any(k in str(json_data).lower() for k in ['file', 'video', 'url']):
                        print(f"JSON response from {url} contains potential video info:")
                        print(json_data)
            except Exception as e:
                pass  # Ignore JSON parse errors

        page.on("response", handle_response)

        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        print("Done loading, closing browser.")
        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <DiskWala Video URL>")
    else:
        url = sys.argv[1]
        asyncio.run(intercept_requests(url))
