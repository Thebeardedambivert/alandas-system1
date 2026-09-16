---
name: dynasafe-2025-ppt
description: 基於 Dynasafe 2025 年度 PPT 模版的簡報生成技能。使用紅白配色系統與微軟正黑體，適用於公司內部會議、技術分享與客戶提案。
---

# Dynasafe 2025 PPT 生成規範

## 核心視覺規範
* **配色系統**：紅白配 (Red: #FF3B30, White: #FFFFFF)。
* **字體**：中文使用『微軟正黑體 (Microsoft JhengHei)』，英數使用『Arial』。
* **版型比例**：16:9 橫向佈局。

## 投影片佈局與對應 (使用 assets/template.pptx)

在使用本技能生成 PPT 時，請務必遵循以下 Layout 映射邏輯：

### 1. 封面頁 (Layout 0: 首頁)
* **主標題**：動力安全資訊股份有限公司
* **副標題**：Dynasafe Technologies Inc. (或特定的專案名稱)

### 2. 章節頁 (Layout 2: 章節)
* **標題**：議題名稱 (例如：1. 技術架構分析)
* **內容**：講者名稱 (格式：講者: [姓名])

### 3. 目錄頁 (Layout 3: 目錄)
* **標題**：目錄  Agenda
* **內容**：列出本次會議的所有章節要點。

### 4. 內容頁 (Layout 1: 標題及物件)
* **標題**：簡短明確的頁面標題。
* **內容**：專業精練的內容要點。

### 5. 結束頁 (Layout 15: Slide with title and subtitle)
* **主標題**：THANK YOU
* **副標題**：www.dynasafe.com.tw

## 執行流程
1. **分析內容**：根據使用者提供的材料，提取出章節、要點與核心結論。
2. **對應佈局**：將提取的內容映射到上述的 Layout 序號。
3. **生成 PPT**：使用 `pptxgenjs` 並載入 `assets/template.pptx` 作為基礎模板進行生成。

## 品質檢核清單
1. 是否嚴格遵守紅白配色？
2. 字體是否設定為微軟正黑體？
3. 目錄頁標題是否包含 "Agenda" 字樣？
4. 結束頁是否包含官方網址？
