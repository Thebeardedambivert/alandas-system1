---
name: gog
description: OpenClaw 官方 Google Workspace (Gmail, Drive, Sheets, Docs, Calendar) 自動化管理技能。
---

# GOG：Google Workspace 自動化總管

此技能透過 `gog` (Google Workspace CLI) 讓 Gemini 直接操控你的 Google 帳號，實現郵件處理、檔案搜尋、日曆排程與表格更新。

## 1. 核心指令範例

### Gmail 郵件管理
- **搜尋郵件**：`gog gmail search 'newer_than:7d' --max 10`
- **發送郵件**：`gog gmail send --to user@example.com --subject "標題" --body "內容"`
- **查看詳情**：`gog gmail get <messageId>`

### Google Drive 雲端硬碟
- **搜尋檔案**：`gog drive search "文件名" --max 5`
- **查看內容**：`gog docs cat <docId>` (適用於 Google Docs)
- **匯出檔案**：`gog docs export <docId> --format txt`

### Google Sheets 試算表
- **讀取數據**：`gog sheets get <sheetId> "Sheet1!A1:D10" --json`
- **更新數據**：`gog sheets update <sheetId> "Sheet1!A1" --values-json '[["新數值"]]'`

### Google Calendar 日曆
- **列出事件**：`gog calendar events <calendarId> --from <startTime> --to <endTime>`

## 2. 初始化與設定 (Setup)

1. **安裝 GogCLI**：確保系統已安裝 `gog` 命令行工具。
2. **OAuth 認證**：首次使用需執行 `gog auth credentials /path/to/client_secret.json` 進行授權。
3. **環境變數**：建議設定 `GOG_ACCOUNT=your-email@gmail.com` 以簡化指令。

## 3. 安全規範
- 在執行 **發送郵件 (Send Email)** 或 **修改數據 (Update)** 之前，**務必**向用戶確認操作內容，嚴禁自動發送未經審核的內容。

## 4. 執行邏輯
本技能調用 `run_shell_command` 執行 `gog` 對應指令，並透過 `--json` 格式解析結果回傳。
