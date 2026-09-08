# 維護工具（在 italy/ 目錄執行）
腳本說明見 `../_template/README.md`。改完內容後務必執行 `python3 tools/build_sw.py` 更新 sw.js 版本，手機端才會更新。
地圖重產：`python3 tools/mkmaps.py`（需 Pillow，磚快取在 .tiles/）後把 maps.json 合併到 data.js 的 days[].maps。
