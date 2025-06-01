import requests

# Define the target URL
url = "https://udapi.diskwala.com/api/v1/auth"

# Define headers with your full cookie
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

# Send the GET request
response = requests.get(url, headers=headers)

# Output the result
print("Status Code:", response.status_code)
print("Response JSON:")

try:
    print(response.json())  # If the server responds with JSON
except Exception as e:
    print("Non-JSON response:", response.text)
