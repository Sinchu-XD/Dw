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

    # Extract title from page title or video title tag
    title = soup.find("h1")
    if title:
        title = title.get_text(strip=True)
    else:
        title = soup.title.string.strip() if soup.title else "Unknown"

    # Extract uploader
    uploader = soup.find("a", href=lambda x: x and "/user/" in x)
    uploader = uploader.get_text(strip=True) if uploader else "Unknown"

    # Duration (if present)
    duration = soup.find("span", class_="video-duration")
    duration = duration.get_text(strip=True) if duration else "Unknown"

    # Upload date (if present in a meta tag or visible span)
    upload_date = None
    for meta in soup.find_all("meta"):
        if meta.get("property") == "video:release_date":
            upload_date = meta.get("content")
            break
    if not upload_date:
        # Try fallback span
        date_span = soup.find("span", class_="upload-date")
        upload_date = date_span.get_text(strip=True) if date_span else "Unknown"

    return {
        "title": title,
        "uploader": uploader,
        "duration": duration,
        "upload_date": upload_date
    }

# Example usage
video_url = "https://www.diskwala.com/app/683aa235b42bb37213a69dd2"
details = get_video_details(video_url)
print(details)
