import asyncio
from playwright.async_api import async_playwright

async def dump_scripts(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Opening URL: {url}")
        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        scripts = await page.query_selector_all("script")

        found = False
        for script in scripts:
            content = await script.text_content()
            if content and ("fileInfo" in content or "video" in content or "url" in content):
                found = True
                print("--- Script Content Snippet ---")
                print(content[:1000])  # print first 1000 chars
                print("------------------------------\n")

        if not found:
            print("No relevant <script> tags found containing 'fileInfo' or 'video' keywords.")

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <DiskWala Video URL>")
    else:
        url = sys.argv[1]
        asyncio.run(dump_scripts(url))
