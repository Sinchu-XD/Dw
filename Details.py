import asyncio
from playwright.async_api import async_playwright

cookies = {
    "name": "rT",
    "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODNjN2ViNmI0MmJiMzcyMTNhZTFkNTgiLCJuYW1lIjoiQWJoaSIsImVtYWlsIjoiYWJoaXNoZWtiYW5zaGl3YWwyMDA1QGdtYWlsLmNvbSIsInB1YmxpY19kZXRhaWxzIjp7InRpdGxlIjoiIiwibGluayI6IiIsImxvZ28iOiIifSwiZV92Ijp0cnVlLCJkX2EiOmZhbHNlLCJibG9ja2VkIjpmYWxzZSwicGFzc3dvcmQiOiIkMmEkMTAkU0tHY0NWQmdCbzJpZXJXV0VEV0dhZTJxRXJqSW9xR3g0L0w1VGRrQ25BSjBQd0JjcGlXdnEiLCJpYXQiOjE3NDg3OTY1MzgsImV4cCI6MTc0ODg4MjkzOH0.il07nKAxyLZjntr8GB_j2j5TkcMObJ1U1QKOH8y-OAs",
    "domain": "diskwala.com",
    "path": "/",
    "httpOnly": False,
    "secure": False
}

async def get_video_details(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_cookies([cookies])
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")

        title = await page.title()
        try:
            uploader = await page.inner_text("a[href^='/user/']")
        except:
            uploader = "Unknown"
        try:
            duration = await page.inner_text(".video-duration")
        except:
            duration = "Unknown"
        try:
            upload_date = await page.inner_text(".upload-date")
        except:
            upload_date = "Unknown"

        await browser.close()

        return {
            "title": title,
            "uploader": uploader,
            "duration": duration,
            "upload_date": upload_date
        }

# Run the function
video_url = "https://www.diskwala.com/app/683aa235b42bb37213a69dd2"
result = asyncio.run(get_video_details(video_url))
print(result)
