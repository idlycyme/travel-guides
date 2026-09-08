# 維護工具（在 italy_guide/ 目錄執行）

- `mkmaps.py`：依 data.js 的 days / coords 產生每日離線地圖到 img/maps/，並輸出 maps.json（需 venv 含 Pillow）。
- `fetch_imgs.py` / `fetch_hl.py`：從 Wikipedia 抓景點與看點縮圖。
- `html2docx.py`：行程摘要 HTML → docx。
- 更新 sw.js 版本：改完內容後執行下方指令（快取名稱含內容 hash，手機才會更新）。

```
python3 - <<'PY'
import os,hashlib,json,re
files=['./','index.html','data.js','manifest.webmanifest']
for d in ['img','img/h','img/s','img/e','img/maps']: files+=sorted(d+'/'+f for f in os.listdir(d) if f.endswith('.jpg'))
files+=sorted('icons/'+f for f in os.listdir('icons'))
h=hashlib.sha1()
for f in files:
    if f!='./': h.update(open(f,'rb').read())
ver=h.hexdigest()[:10]; sw=open('sw.js').read()
sw=re.sub(r"// auto-generated\. version \w+",f"// auto-generated. version {ver}",sw,count=1)
sw=re.sub(r"const CACHE = 'italy-guide-\w+';",f"const CACHE = 'italy-guide-{ver}';",sw,count=1)
sw=re.sub(r"const ASSETS = \[.*?\];",'const ASSETS = '+json.dumps(files,ensure_ascii=False)+';',sw,count=1,flags=re.S)
open('sw.js','w').write(sw); print('sw',ver,len(files))
PY
```

部署：把本資料夾內容 commit 到 GitHub Pages 所在的 repo 對應子目錄後 push。
