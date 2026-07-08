import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://min4jombang.my.id/berkas-madrasah/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
    links = re.findall(r'href=[\'\"]([^\'\"]+)[\'\"]', html)
    print('Total links:', len(links))
    for l in links:
        if '.pdf' in l.lower() or 'drive.google' in l.lower() or 'doc' in l.lower():
            print('Found file link:', l)
except Exception as e:
    print('Error:', e)
