import asyncio
from playwright.async_api import async_playwright
import json

async def dump_scripts(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Opening URL: {url}")
        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        scripts = await page.query_selector_all("script")

        count = 0
        for script in scripts:
            content = await script.text_content()
            if content and len(content) > 500:
                count += 1
                print(f"\n--- Script #{count} Content ({len(content)} chars) ---")
                snippet = content[:1500]
                print(snippet)
                print("------------------------------")

        if count == 0:
            print("No large <script> tags found.")

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 Main.py <DiskWala Video URL>")
    else:
        url = sys.argv[1]
        asyncio.run(dump_scripts(url))
