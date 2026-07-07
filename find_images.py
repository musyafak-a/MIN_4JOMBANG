import urllib.request
import re

urls = [
    ("kelas", "https://min4jombang.my.id/pelaksanaan-ujian-penilaian-akhir-semester-pas-ganjil-tahun-2022-2023-min-4-jombang/"),
    ("ujian_pondok", "https://min4jombang.my.id/min-4-jombang-gelar-tes-penerimaan-siswa-baru-tahun-2025-2026/")
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

for name, url in urls:
    print(f"--- {name} ---")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
    
    # find all image sources
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    for img in imgs:
        print(img)
