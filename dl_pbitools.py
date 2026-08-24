import urllib.request
url='https://github.com/pbi-tools/pbi-tools/releases/download/1.2.0/pbi-tools.core.1.2.0_win-x64.zip'
out=r'F:\BI\retail-bi-project\pbitools.zip'
try:
    urllib.request.urlretrieve(url, out)
    import os
    msg='downloaded bytes='+str(os.path.getsize(out))
except Exception as e:
    msg='ERR '+str(e)
with open(r'F:\BI\retail-bi-project\dl_out.txt','w') as f:
    f.write(msg)
print(msg)
