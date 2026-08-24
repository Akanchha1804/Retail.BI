import urllib.request, json, sys
api='https://api.github.com/repos/pbi-tools/pbi-tools/releases/latest'
req=urllib.request.Request(api, headers={'User-Agent':'opencode'})
out=[]
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        data=json.load(r)
    out.append('tag: ' + data['tag_name'])
    for a in data['assets']:
        n=a['name'].lower()
        if 'core' in n and n.endswith('.zip'):
            out.append(a['name'] + ' -> ' + a['browser_download_url'])
except Exception as e:
    out.append('ERR ' + str(e))
with open(r'F:\BI\retail-bi-project\pbitools_out.txt','w') as f:
    f.write('\n'.join(out))
print('done')
