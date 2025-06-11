from playwright.sync_api import sync_playwright
import time

URL = "https://www.diskwala.com/app/6841bb76b42bb37213c22007"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://diskwala.com",
    "Referer": "https://diskwala.com/",
    "Cookie": (
        "_ga=GA1.1.468420041.1748796491; "
        "rT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODNjN2ViNmI0MmJiMzcyMTNhZTFkNTgiLCJuYW1lIjoiQWJoaSIsImVtYWlsIjoiYWJoaXNoZWtiYW5zaGl3YWwyMDA1QGdtYWlsLmNvbSIsInB1YmxpY19kZXRhaWxzIjp7InRpdGxlIjoiIiwibGluayI6IiIsImxvZ28iOiIifSwiZV92Ijp0cnVlLCJkX2EiOmZhbHNlLCJibG9ja2VkIjpmYWxzZSwicGFzc3dvcmQiOiIkMmEkMTAkU0tHY0NWQmdCbzJpZXJXV0VEV0dhZTJxRXJqSW9xR3g0L0w1VGRrQ25BSjBQd0JjcGlXdnEiLCJpYXQiOjE3NDg3OTY1MzgsImV4cCI6MTc0ODg4MjkzOH0.il07nKAxyLZjntr8GB_j2j5TkcMObJ1U1QKOH8y-OAs; "
        "_ga_9CY1MQHST7=GS2.1.s1748796490$o1$g1$t1748797215$j59$l0$h0"
    )
}

def extract_video_from_network(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(extra_http_headers=HEADERS)
        page = context.new_page()
        video_url = None

        # Intercept responses to sniff .mp4 links
        def handle_response(response):
            nonlocal video_url
            if ".mp4" in response.url:
                video_url = response.url

        page.on("response", handle_response)

        print("🌐 Opening page and sniffing network...")
        page.goto(url, wait_until="networkidle")

        # Wait for JS to load and media to stream
        time.sleep(10)

        browser.close()

        if video_url:
            print(f"✅ Found video URL:\n{video_url}")
        else:
            print("❌ No .mp4 video found in network traffic.")
        return video_url

if __name__ == "__main__":
    extract_video_from_network(URL)
