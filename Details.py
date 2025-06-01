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

def get_video_details(page_url):
    response = requests.get(page_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    details = {}

    # Example 1: Get Title from <title> or <meta property="og:title">
    title_tag = soup.find('title')
    if title_tag:
        details['title'] = title_tag.text.strip()
    else:
        og_title = soup.find('meta', property='og:title')
        if og_title:
            details['title'] = og_title.get('content', '').strip()

    # Example 2: Get Uploader Username - might be in a specific element
    # You need to check the page's HTML, e.g., a span or a div with uploader info
    uploader = soup.find('div', class_='uploader-name')  # Example class, change accordingly
    if uploader:
        details['uploader'] = uploader.text.strip()
    else:
        # Try alternative selectors or fallback
        details['uploader'] = 'Unknown'

    # Example 3: Get Duration - check if there's a meta tag or HTML span
    duration = soup.find('meta', property='video:duration')
    if duration:
        details['duration'] = duration.get('content')
    else:
        duration_span = soup.find('span', class_='duration')  # Adjust class as needed
        if duration_span:
            details['duration'] = duration_span.text.strip()

    # Example 4: Get Upload Date - meta tag or specific date element
    upload_date = soup.find('meta', itemprop='uploadDate')
    if upload_date:
        details['upload_date'] = upload_date.get('content')
    else:
        date_span = soup.find('span', class_='upload-date')  # Adjust class as needed
        if date_span:
            details['upload_date'] = date_span.text.strip()

    return details

# Example usage:
video_page_url = "https://www.diskwala.com/app/683aa235b42bb37213a69dd2"
video_info = get_video_details(video_page_url)
print(video_info)
