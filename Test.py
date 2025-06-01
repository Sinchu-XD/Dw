import requests

def extract_file_id(url):
    parts = url.rstrip('/').split('/')
    if len(parts) > 1 and parts[-2] == 'app':
        return parts[-1]
    return None

def get_video_info(file_id):
    api_url = "https://udapi.diskwala.com/api/v1/file/temp_info"
    payload = {"file_id": file_id}  # adjust if key differs
    
    response = requests.post(api_url, json=payload)
    if response.ok:
        data = response.json()
        print("API response:", data)
        video_url = data.get("fileInfo", {}).get("url")
        if video_url:
            return video_url
        else:
            print("No direct video URL found.")
            return None
    else:
        print("API request failed:", response.status_code)
        return None

def main(url):
    print("Opening URL:", url)
    file_id = extract_file_id(url)
    if not file_id:
        print("Invalid URL format. Could not extract file ID.")
        return
    
    print("Extracted file ID:", file_id)
    video_url = get_video_info(file_id)
    if video_url:
        print("Video URL found:", video_url)
        # You can now download the video or do whatever you want with this URL
    else:
        print("Could not find video URL.")

# Run main with your URL
if __name__ == "__main__":
    url = "https://www.diskwala.com/app/683aa235b42bb37213a69dd4"
    main(url)
