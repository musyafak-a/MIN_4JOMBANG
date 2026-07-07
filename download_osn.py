import os
import urllib.request

url = "https://sdia41.al-azhar.sch.id/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-13-at-08.16.01_e158e2ec-1-1210x642.jpg"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
output_dir = "static/img/gallery_new"
filepath = os.path.join(output_dir, "osn_ipa_new.jpg")

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    with open(filepath, "wb") as f:
        f.write(resp.read())

print("Downloaded OSN image")
