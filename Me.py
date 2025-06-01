import base64
import json

jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODNjN2ViNmI0MmJiMzcyMTNhZTFkNTgiLCJuYW1lIjoiQWJoaSIsImVtYWlsIjoiYWJoaXNoZWtiYW5zaGl3YWwyMDA1QGdtYWlsLmNvbSIsInB1YmxpY19kZXRhaWxzIjp7InRpdGxlIjoiIiwibGluayI6IiIsImxvZ28iOiIifSwiZV92Ijp0cnVlLCJkX2EiOmZhbHNlLCJibG9ja2VkIjpmYWxzZSwicGFzc3dvcmQiOiIkMmEkMTAkU0tHY0NWQmdCbzJpZXJXV0VEV0dhZTJxRXJqSW9xR3g0L0w1VGRrQ25BSjBQd0JjcGlXdnEiLCJpYXQiOjE3NDg3OTY1MzgsImV4cCI6MTc0ODg4MjkzOH0.il07nKAxyLZjntr8GB_j2j5TkcMObJ1U1QKOH8y-OAs"


payload_base64 = jwt_token.split('.')[1]

padded = payload_base64 + "=" * (-len(payload_base64) % 4)
decoded = base64.urlsafe_b64decode(padded)
data = json.loads(decoded)


print("User Info from JWT:")
print(json.dumps(data, indent=2))
