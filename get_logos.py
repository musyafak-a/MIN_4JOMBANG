import urllib.request
import re

urls = {
    'unicef': 'https://en.wikipedia.org/wiki/File:UNICEF_Logo.png', # SVG often protected, let's look for SVG anyway
    'kumon': 'https://en.wikipedia.org/wiki/File:Kumon_Logo.svg',
    'ruangguru': 'https://id.wikipedia.org/wiki/Berkas:Ruang_Guru_logo.svg'
}

# Actually Wikipedia URLs:
urls = {
    'unicef': 'https://en.wikipedia.org/wiki/File:UNICEF_Logo.svg',
    'kumon': 'https://en.wikipedia.org/wiki/File:Kumon_Logo.svg',
    'ruangguru': 'https://id.wikipedia.org/wiki/Berkas:Ruang_Guru_logo.svg'
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        m = re.search(r'href="(//upload\.wikimedia\.org/wikipedia/[^\"]+\.svg)"', html)
        if m:
            svg_url = 'https:' + m.group(1)
            print(f"{name}: {svg_url}")
            
            svg_req = urllib.request.Request(svg_url, headers={'User-Agent': 'Mozilla/5.0'})
            svg_data = urllib.request.urlopen(svg_req).read()
            with open(f'static/img/{name}.svg', 'wb') as f:
                f.write(svg_data)
        else:
            print(f"{name}: SVG Not found in HTML. Looking for png.")
            m_png = re.search(r'href="(//upload\.wikimedia\.org/wikipedia/[^\"]+\.png)"', html)
            if m_png:
                png_url = 'https:' + m_png.group(1)
                print(f"{name}: {png_url}")
                png_req = urllib.request.Request(png_url, headers={'User-Agent': 'Mozilla/5.0'})
                png_data = urllib.request.urlopen(png_req).read()
                with open(f'static/img/{name}.png', 'wb') as f:
                    f.write(png_data)
    except Exception as e:
        print(f"{name}: Error - {e}")
