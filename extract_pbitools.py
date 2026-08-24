import zipfile, os, sys
zpath = r'F:\BI\retail-bi-project\pbitools.zip'
dest = r'F:\BI\retail-bi-project\pbitools'
msg=[]
try:
    if not os.path.exists(zpath):
        msg.append('zip missing')
    else:
        msg.append('zip size='+str(os.path.getsize(zpath)))
        with zipfile.ZipFile(zpath) as z:
            bad = z.testzip()
            msg.append('testzip='+str(bad))
            z.extractall(dest)
            msg.append('extracted='+str(len(z.namelist())))
            msg.append('first='+z.namelist()[0])
except Exception as e:
    msg.append('ERR '+repr(e))
with open(r'F:\BI\retail-bi-project\extract_out.txt','w') as f:
    f.write('\n'.join(msg))
print('\n'.join(msg))
