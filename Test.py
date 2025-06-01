import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import sys

async def dump_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000)
        content = await page.content()
        with open("diskwala_dump.html", "w", encoding="utf-8") as f:
            f.write(content)
        await browser.close()

def extract_details_from_html():
    with open('diskwala_dump.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    file_name_tag = soup.find_all('p', class_='MuiTypography-body1')
    file_name = file_name_tag[0].text.strip() if file_name_tag else 'Not found'

    file_type_tag = soup.find('span', class_='MuiTypography-caption')
    file_type = file_type_tag.text.strip() if file_type_tag else 'Not found'

    uploader_tags = soup.find_all('h6', class_='MuiTypography-h6')
    uploader = uploader_tags[1].text.replace("File By: ", "").strip() if len(uploader_tags) > 1 else 'Not found'

    print("📄 File Name:", file_name)
    print("📂 File Type:", file_type)
    print("👤 Uploaded By:", uploader)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_info.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(dump_html(url))
    extract_details_from_html()
