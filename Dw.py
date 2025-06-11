import requests
import uuid

headers = {
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

def get_video_info(file_id: str):
    api_url = "https://udapi.diskwala.com/api/v1/file/temp_info"
    response = requests.post(api_url, headers=headers, json={"_id": file_id})

    if response.status_code != 200:
        print("❌ Failed to fetch file info:", response.status_code)
        return None

    data = response.json()
    try:
        u_id = data["fileInfo"]["u_id"]
        ext = data["fileInfo"]["extension"]
        video_id = data["fileInfo"]["_id"]
        name = data["fileInfo"]["name"]
    except KeyError:
        print("❌ Unexpected response format.")
        return None

    # Construct direct download URL
    direct_url = f"https://udapi.diskwala.com/api/v1/file/download/{u_id}/{video_id}?ext={ext}"
    return direct_url, name

def download_video(video_url, filename):
    print(f"📥 Downloading from: {video_url}")
    with requests.get(video_url, headers=headers, stream=True) as r:
        if r.status_code != 200:
            print("❌ Download failed:", r.status_code)
            return
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"✅ Download complete: {filename}")

if __name__ == "__main__":
    # Replace with your actual ID from the URL
    file_id = "68493575b42bb37213de4311"

    result = get_video_info(file_id)
    if result:
        direct_url, raw_name = result
        filename = raw_name if raw_name.endswith(".mp4") else f"{uuid.uuid4().hex[:8]}.mp4"
        download_video(direct_url, filename)
      
