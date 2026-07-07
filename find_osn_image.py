import urllib.request
import re

url = "https://sdia41.al-azhar.sch.id/sd-islam-al-azhar-41-karawang-juarai-osn-ipa-tingkat-kecamatan-dan-berhak-maju-ke-tingkat-kabupaten/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8', errors='ignore')

# print main image or all images
imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
for img in imgs:
    print(img)
