import os
import urllib.request

links = {
    "osn_ipa": "https://rz.utakatikotak.com/x.php?src=http://cdn.utakatikotak.com/sekolah/20250818_10055920200929_161730sukabumi2prb.png&w=80&h=80&zc=1",
    "kelas": "https://min4jombang.my.id/wp-content/uploads/2022/12/WhatsApp-Image-2022-12-05-at-07.41.49-1024x768.jpeg",
    "ujian_pondok": "https://min4jombang.my.id/wp-content/uploads/2025/03/MIN-4-Jombang-Gelar-Tes-Penerimaan-Siswa-Baru-Tahun-2025-2026-1024x768.jpg",
    "bisnis_day": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1Gj3Fblht8v7X1GzJCJFUVfvuInF1HWabvq-CkwgSR6c-l4ZcRmsmv6g&s=10",
    "penghargaan": "https://min4jombang.my.id/wp-content/uploads/2023/09/WhatsApp-Image-2023-08-07-at-11.44.15.jpeg"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

output_dir = "static/img/gallery_new"
os.makedirs(output_dir, exist_ok=True)

for name, url in links.items():
    print(f"Downloading {name} from {url}")
    try:
        img_req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(img_req) as img_resp:
            content = img_resp.read()
            
        ext = ".jpg"
        if "png" in url.lower() or name == "osn_ipa": ext = ".png"
        elif "jpeg" in url.lower(): ext = ".jpeg"
        
        filepath = os.path.join(output_dir, f"{name}{ext}")
        with open(filepath, "wb") as f:
            f.write(content)
        print(f"Saved {filepath}")
    except Exception as e:
        print(f"Error processing {name}: {e}")
