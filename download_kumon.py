import os
import urllib.request

url = "https://ab.kumonglobal.com/wp-content/uploads/2020/04/cropped-Kumon-logo-black-A4-1.png"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
filepath = os.path.join("static", "img", "kumon.png")

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        with open(filepath, "wb") as f:
            f.write(resp.read())
    print("Downloaded Kumon logo successfully.")
except Exception as e:
    print(f"Failed to download: {e}")
