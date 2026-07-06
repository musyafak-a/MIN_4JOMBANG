import urllib.request
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://id.wikipedia.org/'
}

logos = {
    'unicef.svg': 'https://upload.wikimedia.org/wikipedia/commons/2/23/UNICEF_Logo.svg',
    'kumon.svg': 'https://upload.wikimedia.org/wikipedia/commons/5/52/Kumon_Logo.svg',
    'ruangguru.svg': 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Ruang_Guru_logo.svg'
}

for name, url in logos.items():
    path = os.path.join('static', 'img', name)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded {name}")
        time.sleep(2)
    except Exception as e:
        print(f"Failed {name}: {e}")
