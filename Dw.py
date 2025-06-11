from playwright.sync_api import sync_playwright
import requests
import uuid
import time

VIDEO_PAGE = "https://www.diskwala.com/app/6841bb76b42bb37213c22007"
COOKIE_RT = "rT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODNjN2ViNmI0MmJiMzcyMTNhZTFkNTgiLCJuYW1lIjoiQWJoaSIsImVtYWlsIjoiYWJoaXNoZWtiYW5zaGl3YWwyMDA1QGdtYWlsLmNvbSIsInB1YmxpY19kZXRhaWxzIjp7InRpdGxlIjoiIiwibGluayI6IiIsImxvZ28iOiIifSwiZV92Ijp0cnVlLCJkX2EiOmZhbHNlLCJibG9ja2VkIjpmYWxzZSwicGFzc3dvcmQiOiIkMmEkMTAkU0tHY0NWQmdCbzJpZXJXV0VEV0dhZTJxRXJqSW9xR3g0L0w1VGRrQ25BSjBQd0JjcGlXdnEiLCJpYXQiOjE3NDg3OTY1MzgsImV4cCI6MTc0ODg4MjkzOH0.il07nKAxyLZjntr8GB_j2j5TkcMObJ1U1QKOH8y-OAs; "  # 🔴 Replace with your actual rT token string

def extract_video_url_with_cookie(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        context.add_cookies([{
            "name": "rT",
            "value": COOKIE_RT,
            "domain": ".diskwala.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,
        }])
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        time.sleep(3)  # Let JS load if needed

        # Try to get a video or iframe or download link
        links = page.eval_on_selector_all(
            'a[href*=".mp4"], video > source[src], iframe[src], a[href*="cdn"]',
            'els => els.map(el => el.src || el.href)'
        )

        browser.close()
        if links:
            return links[0]
        else:
            raise RuntimeError("❌ No video URL found on page.")

if __name__ == "__main__":
    try:
        video_url = extract_video_url_with_cookie(VIDEO_PAGE)
        print("✅ Direct video URL found:\n", video_url)
    except Exception as e:
        print("❌ Error:", e)
