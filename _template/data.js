// 旅遊導覽資料骨架。完整欄位說明見 README.md。
// 用實際內容取代下方範例；所有文字為繁體中文，名稱欄位另附當地語言與英文。
window.GUIDE = {
 "meta": {
  "id": "japan2027",            // localStorage 命名空間，每趟不同
  "title": "2027 日本",          // 側欄與瀏覽器標題
  "short": "日本導覽",           // 加入主畫面時的名稱
  "sub": "4/1 – 4/10 景點導覽",
  "year": 2027,                 // 判斷「今天」用
  "tz": 9                       // 目的地與 UTC 的時差（小時），算日出日落用
 },
 "days": [
  {
   "date": "4/1", "dow": "四", "city": "東京", "title": "抵達",
   "ll": [35.68, 139.77],                       // 城市座標，算日出日落
   "spots": ["sensoji", "eat_tokyo", "shop_tokyo"],   // 景點 id，順序 = 當日路線；eat_/shop_ 放在該城市第一天
   "plan": {
    "transport": [["10:00", "航班 XX123 抵達成田 T1"], ["11:30", "Skyliner → 上野 41 分"]],
    "hotel": { "id": "hotel_tokyo", "name": "Hotel Example", "addr": "1-2-3 Asakusa, Taito-ku", "note": "淺草站步行 5 分", "map": "https://www.google.com/maps/search/?api=1&query=Hotel+Example+Asakusa" },
    "todo": ["買 Suica", "飯店放行李"]
   }
   // "maps": 由 tools/mkmaps.py 產生後合併進來
  },
  { "date": "購物", "dow": "", "city": "伴手禮總覽", "title": "到處都能買", "spots": ["shop_general"] }
 ],
 "spots": {
  "sensoji": {
   "name": "淺草寺", "en": "Sensō-ji 浅草寺", "city": "東京",
   "booked": "4/1 下午",                         // 預約時段或備註，顯示為黃色 chip
   "imgs": [{ "f": "sensoji.jpg", "c": "雷門與仲見世通" }],   // 檔案相對於 img/
   "intro": "一段話說明為什麼值得來、現場第一眼看什麼。",
   "highlights": [
    // [中文, 當地語言, English, 說明, 縮圖(可省略或 null), 地圖連結(可省略)]
    ["雷門", "雷門 Kaminarimon", "Thunder Gate", "1960 年由松下幸之助捐建重製的大門，紅色大燈籠重 700 公斤。", "h/sensoji_0.jpg"],
    ["仲見世通", "仲見世通り", "Nakamise shopping street", "250 公尺、90 家店的參道商店街，人形燒與雷おこし是招牌。"]
   ],
   "history": ["一到三段：起源、關鍵年代與事件、看懂它的鑰匙。"],
   "tips": ["入口、票、服裝、時段、動線建議。"]
  },
  "eat_tokyo": {
   "kind": "eat", "name": "餐廳與商店推薦：東京", "en": "Where to eat & shop – Tokyo", "city": "東京", "booked": "東京 4/1–4/3",
   "imgs": [{ "f": "e/ramen.jpg", "c": "拉麵" }],
   "intro": "幾個地點、分幾區、哪個離住宿最近。",
   "highlights": [
    // 店家：一定要有第 6 欄地圖連結（用 https://www.google.com/maps/search/?api=1&query=店名,地址,城市）
    ["一蘭 淺草店", "一蘭 浅草店", "Ichiran ramen", "地址。朋友推薦：…。點什麼、價位、營業時間。", "e/ramen.jpg", "https://www.google.com/maps/search/?api=1&query=Ichiran+Asakusa"]
   ],
   "notes": [
    // 非店家的美食筆記（無地圖連結）：怎麼點餐、必吃清單
    ["怎麼點拉麵", "ラーメンの注文", "How to order ramen", "販賣機買券、硬度與濃度選項…", "e/ramen.jpg"]
   ],
   "history": ["一段小知識。"],
   "tips": ["動線與提醒。"]
  },
  "shop_tokyo": {
   "kind": "shop", "name": "伴手禮：東京", "en": "Souvenirs – Tokyo", "city": "東京", "booked": "東京 4/1–4/3",
   "imgs": [{ "f": "s/tokyobanana.jpg", "c": "東京香蕉" }],
   "intro": "這個城市限定的東西；全國通用的留到最後一天。",
   "highlights": [
    // 商品：[中文, 當地語言, English, 是什麼＋怎麼挑＋價位＋哪裡買, 縮圖]
    ["東京香蕉", "東京ばな奈", "Tokyo Banana", "車站與機場都有，保存 7 天…", "s/tokyobanana.jpg"]
   ],
   "history": ["背景。"],
   "tips": ["哪裡買、怎麼帶、海關限制。"]
  },
  "shop_general": {
   "kind": "shop", "name": "伴手禮：到處都能買", "en": "Souvenirs – anywhere", "city": "全日本", "booked": "超市、藥妝店皆有",
   "imgs": [{ "f": "s/kitkat.jpg", "c": "KitKat 地區限定" }],
   "intro": "全國通用的清單。",
   "highlights": [],
   "history": [],
   "tips": []
  }
 },
 // 地圖上用綠色標示的店（eat_* 條目裡屬於商店而非餐廳的項目 key：spotId_index）
 "storeKeys": [],
 // 額外採購地點（綠色 pin，出現在該城市每一天的「採購地點」）
 "stores": [
  { "city": "東京", "name": "唐吉訶德 淺草", "ll": [35.713, 139.796], "desc": "藥妝、零食一次買齊，可退稅。", "map": "https://www.google.com/maps/search/?api=1&query=Don+Quijote+Asakusa" }
 ],
 // 座標：景點 id、hotel_*、以及餐廳 key（spotId_index）。tools/mkmaps.py 與今日頁的步行分鐘數都用這裡
 "coords": {
  "sensoji": [35.7148, 139.7967],
  "hotel_tokyo": [35.711, 139.797],
  "eat_tokyo_0": [35.7115, 139.7965]
 }
};
