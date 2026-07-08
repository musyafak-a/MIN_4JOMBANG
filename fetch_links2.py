import urllib.request
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://min4jombang.my.id/category/prestasi/page/4/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            if 'wp-content/uploads' in src:
                print(src)
except Exception as e:
    print('Error:', e)
