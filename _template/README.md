# Travel Guide Template

一份可離線使用的旅遊導覽 PWA：每日頁（時間表、住宿、路線、離線地圖）、景點導覽（三語看點可打勾、歷史、提示）、伴手禮清單、餐廳與商店推薦。純靜態檔案，放到 GitHub Pages 即可，手機用 Safari「加入主畫面」後離線可用。

範例：`../italy/`（2026 義大利）。

## 檔案

| 檔案 | 說明 |
|---|---|
| `index.html` | 應用程式本體，不用改。所有文字與圖片來自 `data.js`。 |
| `data.js` | 唯一要寫的內容檔。骨架含每個欄位的說明。 |
| `manifest.webmanifest` | 把 `TRIP_TITLE`、`TRIP_SHORT` 換掉。 |
| `sw.js` | Service worker。內容改完後跑 `tools/build_sw.py` 更新版本與快取清單，手機才會更新。 |
| `icons/` | `icon-180.png`、`icon-192.png`、`icon-512.png`。用一張代表照片裁正方形縮圖即可。 |
| `img/` | 景點主圖；`img/h/` 看點縮圖、`img/s/` 商品圖、`img/e/` 餐廳與菜色圖、`img/maps/` 每日地圖。 |
| `tools/` | 抓圖、座標、地圖、sw 版本等腳本，見各檔開頭說明。 |

## data.js 結構

```
meta      id / title / short / sub / year / tz
days[]    date "M/D", dow, city, title, ll[lat,lng], spots[id…], plan{transport[[時間,文字]], hotel{id,name,addr,note,map}, todo[]}, maps[]（由工具產生）
spots{}   id → { name, en, city, booked, imgs[{f,c}], intro, highlights[], history[], tips[] }
          highlights 每筆：[中文, 當地語言, English, 說明, 縮圖(可省), 地圖連結(可省)]
          kind:"eat"  餐廳與商店條目：highlights 為店家（第 6 欄必填地圖連結），notes[] 為非店家的美食筆記
          kind:"shop" 伴手禮條目：highlights 為商品
storeKeys[]  eat 條目裡屬於商店的項目 key（spotId_index），地圖上畫綠色
stores[]     額外採購地點 {city,name,ll,desc,map}
coords{}     景點 id、hotel_*、餐廳 key → [lat,lng]；地圖與步行分鐘數用
```

規則：
- `days[].spots` 的順序就是當日路線。`eat_*` 與 `shop_*` 放在該城市**行程開始的第一天**（不是抵達當晚）。
- 最後加一個 `date:"購物"` 的 day 放 `shop_general`（到處都能買的伴手禮）。
- 每個看點一定要有當地語言名稱，現場標示才對得上。
- 店家一定要有地圖連結：`https://www.google.com/maps/search/?api=1&query=店名,地址,城市`。朋友給的短網址可直接用。
- 說明文字用繁體中文，簡短：是什麼、為什麼看、怎麼挑或怎麼點。

## 產出流程（約 2–3 小時）

1. **行程**：從行程表整理 `days`（日期、城市、預約時段、火車班次、住宿）。
2. **景點內容**：每個景點寫 intro、6–10 個看點、2–3 段歷史、3–5 條提示。景點 id 用英文小寫。
3. **圖片**：寫一份 `{key: "Wikipedia 標題"}` 對照表，跑 `tools/fetch_wiki.py mapping.json img/`（看點縮圖用 `img/h/`，key 為 `spotId_index`）。抓完用縮圖檢查表看一遍，刪掉 logo、地圖、抓錯的圖。`sips -Z 480` 縮小。
4. **伴手禮**：每城市一條 `shop_*`，最後 `shop_general`。商品圖同樣用 fetch_wiki。
5. **餐廳與商店**：短網址用 `tools/resolve_links.py`；Google Maps 分享清單用 `tools/gmaps_list_dump.mjs`（需 headless Chrome）。每城市一條 `eat_*`，非店家的知識放 `notes`。
6. **座標**：`tools/geocode.py` 產 `coords.json`，人工核對後合併進 `data.js`。連鎖店常被定位到別的分店。
7. **地圖**：`python3 tools/mkmaps.py`（需 Pillow）→ `img/maps/` 與 `maps.json`，把 `maps.json` 各日內容合併到 `days[].maps`。地圖磚目前用 OSM France（`tile.openstreetmap.fr/osmfr`），官方 `tile.openstreetmap.org` 會封鎖批次下載，CARTO 需金鑰。
8. **PWA**：改 `manifest.webmanifest`、做 icons、跑 `tools/build_sw.py`。
9. **檢查**：`node -e` 檢查 index.html 內 JS 語法；headless Chrome 截圖總覽、一個景點頁、一個每日頁（手機寬 500px）。
10. **部署**：commit 到 GitHub Pages repo 的子目錄，root `index.html` 加一個連結。手機 Safari 開網址 → 加入主畫面。

## 已知陷阱

- iOS「檔案」App 的 HTML 預覽不執行 JavaScript，AirDrop 單檔行不通，一定要走網址。
- Wikipedia 縮圖要用 `pithumbsize` 參數，自己拼 thumb 網址會 400；一次 40 個標題、間隔 2 秒，否則 429。
- Google Maps 分享清單的 getlist API 只回前 10 筆，要用 headless Chrome 捲動側欄。
- 快取名稱含內容 hash，改內容一定要重跑 `build_sw.py`。
- 公開 repo 不要放：email、本機路徑、帳號設定、票券編號、保單號。住宿與航班是否公開自行決定。
- 圖片總量控制在 50 MB 以下（iOS 快取上限），單張 480–1600px、JPEG 75–80。

## 授權與來源

圖片來自 Wikipedia / Wikimedia Commons（各 `credits.json` 有來源），地圖 © OpenStreetMap contributors。內容為旅行參考。
