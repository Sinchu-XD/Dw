import requests

url = "https://udapi.diskwala.com/api/v1/auth"  # or any other authenticated endpoint

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.diskwala.com/",
    "Origin": "https://www.diskwala.com",
    "Cookie": "_ga=GA1.1.63933014.1748794995; "
              "rT=eyJhbGciOiJIUzI1NilsInR5cCl6lkpXVCJ9.eyJfaWQiOiI2ODNjN2ViNml0MmJiMzcyMTNhZTFKNTgiLC"
              "JuYW1lIjoiQWJoaSIsImVtYWlsljoiYWJoaXNoZWtYW5zaGI3YWwyMDA1QGdtYWlsLmNvbSIsInB1YmxpY19kZXRh"
              "aWxzljp7InRpdGxlljoiliwibGluayl6lilslmxvZ28iOilifSwiZV921jpmYWxzZSwiZF9hIjpmYWxzZSwiYmxvY2tl"
              "ZCI6ZmFsc2UsInBhc3N3b3JkljoiJDJhJDEWJFNLR2NDVKJnQm8yaWVyV1dFRFdHYWUycUVyaklvcUd4NC9MNVRka0NuQU"
              "owUHdCY3BpV3ZxliwiaWF0ljoxNzQ4Nzk1MDc3LCJleHAiOjE3NDg4ODEONzd9.PmlYg0GBIIVgd4p4GXB-RKU700QlabRCiv-iSel-OAI; "
              "_ga_9CY1MQHST7=GS2.1.s1748794995$o1$g1$t1748795526$j60$10$h0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
