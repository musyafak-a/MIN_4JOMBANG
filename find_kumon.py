import urllib.request
import re

url = 'https://en.wikipedia.org/wiki/Kumon'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
m = re.search(r'href="/wiki/File:([^"]+\.svg)"', html)
if m:
    file_page_url = 'https://en.wikipedia.org/wiki/File:' + m.group(1)
    req2 = urllib.request.Request(file_page_url, headers={'User-Agent': 'Mozilla/5.0'})
    html2 = urllib.request.urlopen(req2).read().decode('utf-8')
    m2 = re.search(r'href="(//upload\.wikimedia\.org/wikipedia/[^\"]+\.svg)"', html2)
    if m2:
        svg_url = 'https:' + m2.group(1)
        print(f"kumon: {svg_url}")
        svg_req = urllib.request.Request(svg_url, headers={'User-Agent': 'Mozilla/5.0'})
        svg_data = urllib.request.urlopen(svg_req).read()
        with open('static/img/kumon.svg', 'wb') as f:
            f.write(svg_data)
    else:
        print("SVG Not found on file page")
else:
    print("Logo not found on Wikipedia")
