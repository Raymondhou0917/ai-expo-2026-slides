# Cloudflare 靜態部署

更新：2026-10-10 America/Lima。

## 公開邊界

`public-files.json` 是逐檔公開白名單，`python3 scripts/build-public.py` 僅複製這些檔案到 `dist/`，不得部署 repo 根目錄。新增公開資產時先核對用途，再加入白名單。CI 是乾淨 checkout；本機建置若發現多餘產物會失敗，不會默默發布。

Pages 專案：`lifehacker-expo`。正式網址：`https://expo.lifehacker.tw/`。

## 搜尋與預覽

正式內容在原始 HTML，建置加入 canonical、OG、與可見內容一致的 WebPage schema、標題錨點、robots、sitemap；不宣稱能保證排名或 AI 引用。`site-config.json` 只列主要可索引內容頁，不列內部文檔、個別元件預覽與下載原始碼。Pages 預覽網域回 `X-Robots-Tag: noindex`，正式自訂網域不套用。404 真正回 404，不做 SPA 萬用 fallback。

## 部署與還原

先提交分支，核對 preview、功能與資產，通過後 fast-forward `master`。核對 Git push 觸發的 production deployment commit，才切 DNS。保留 Zeabur service/project 與舊 DNS 資料；驗收後停服務及舊 Git trigger，還原需恢復 service/trigger 並把 DNS 指回舊目標。不可刪除舊 project。

`talk.lifehacker.tw` 與 `expo.lifehacker.tw` 繼續顯示相同簡報；以既有 AI Expo 名稱的 `expo` 作 canonical，不新增轉址以保留兩域與 hash 操作。原 repo 已 archived；本輪為恢復 push 自動部署而解除 archived，原 PUBLIC 可見度未更動。已移除原本 404 的缺檔圖片容器，未以其他帳目圖片替代。

## 正式完成與切換事件

2026-10-10 22:12 America/Lima（UTC 2026-10-11 03:12），expo／talk 的 Pages domain、verification、validation 均 active，正式 HTTPS 與簡報資產正常。先前 fresh-context reviewer 已驗簡報鍵盤導航與 38 個引用資產。Talk canonical 指 Expo，兩域皆可繼續閱讀簡報，不改 hash 操作。

初次切換曾短暫 522，Talk 回退 Zeabur 保留可用來源；後續將 Talk CNAME 設成 `lifehacker-expo.pages.dev`、DNS-only、TTL 60，再完成 CF 驗證。台灣 Mini 已正常讀 CF，本機曾保留舊 IP，確認公共 DNS 和路由器 DNS 均正確後，清除本機系統 DNS cache 亦正常。沒有改網路代理／路由器設定。

重新核對 project `69b281bf03b668320b253267`、environment `69b281c06853f6f4f5f68c83`、service `69c49cca82fb34707a9efc19` 的 repo 與雙域後，解除 Git trigger 並暫停舊 Zeabur；保留專案與設定。未刪服務；恢復方式見前節。
