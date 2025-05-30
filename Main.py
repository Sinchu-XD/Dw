import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def dump_html(url, filename="diskwala_download_page.html"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # Wait extra time for JS to finish rendering
        await page.wait_for_timeout(5000)

        content = await page.content()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Page HTML dumped to {filename}")
        await browser.close()

def parse_html(filename="diskwala_download_page.html"):
    with open(filename, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract file name
    file_name_tag = soup.find_all('p', class_='MuiTypography-body1')
    file_name = file_name_tag[0].text if file_name_tag else 'Not found'

    # Extract file type
    file_type_tag = soup.find('span', class_='MuiTypography-caption')
    file_type = file_type_tag.text if file_type_tag else 'Not found'

    # Extract uploader name
    uploader_tag = soup.find_all('h6', class_='MuiTypography-h6')
    uploader = uploader_tag[1].text.replace("File By: ", "") if len(uploader_tag) > 1 else 'Not found'

    print(f"\nExtracted Info:")
    print(f"File Name: {file_name}")
    print(f"File Type: {file_type}")
    print(f"Uploaded By: {uploader}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <diskwala_url>")
        sys.exit(1)

    url = sys.argv[1]

    # Run async playwright task and then parse the saved HTML
    asyncio.run(dump_html(url))
    parse_html()
  
