import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": (
        "_ga=GA1.1.468420041.1748796491; "
        "rT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODNjN2ViNmI0MmJiMzcyMTNhZTFkNTgiLCJuYW1lIjoiQWJoaSIsImVtYWlsIjoiYWJoaXNoZWtiYW5zaGl3YWwyMDA1QGdtYWlsLmNvbSIsInB1YmxpY19kZXRhaWxzIjp7InRpdGxlIjoiIiwibGluayI6IiIsImxvZ28iOiIifSwiZV92Ijp0cnVlLCJkX2EiOmZhbHNlLCJibG9ja2VkIjpmYWxzZSwicGFzc3dvcmQiOiIkMmEkMTAkU0tHY0NWQmdCbzJpZXJXV0VEV0dhZTJxRXJqSW9xR3g0L0w1VGRrQ25BSjBQd0JjcGlXdnEiLCJpYXQiOjE3NDg3OTY1MzgsImV4cCI6MTc0ODg4MjkzOH0.il07nKAxyLZjntr8GB_j2j5TkcMObJ1U1QKOH8y-OAs; "
        "_ga_9CY1MQHST7=GS2.1.s1748796490$o1$g1$t1748797215$j59$l0$h0"
    )
}

def print_all_meta_tags(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    print("All meta tags:")
    for meta in soup.find_all('meta'):
        print(meta)

    print("\nPotential uploader or date spans/divs:")
    for tag in soup.find_all(['span', 'div']):
        text = tag.get_text(strip=True)
        if text and (len(text) < 50):  # small snippet text only
            print(f"<{tag.name} class='{tag.get('class')}'>{text}</{tag.name}>")

video_url = "YOUR_VIDEO_PAGE_URL"
print_all_meta_tags(video_url)
