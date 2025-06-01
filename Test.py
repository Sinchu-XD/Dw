import asyncioAdd commentMore actions
from playwright.async_api import async_playwright

async def dump_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # Wait a bit extra for JS to run
        await page.wait_for_timeout(5000)
        content = await page.content()
        with open("diskwala_dump.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Page HTML dumped to diskwala_dump.html")
        await browser.close()
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 dump.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(dump_html(url))
