import solara

@solara.component
def Page():
    # 設定 CSS 樣式
    solara.Style("""
        .hero-title {
            background: -webkit-linear-gradient(45deg, #094885, #1d976c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            margin-bottom: 10px;
            font-size: 2.8em; 
            line-height: 1.2;
            text-align: center;
        }
        .hero-subtitle {
            color: #555;
            font-size: 1.2em;
            font-weight: 500;
            text-align: center;
            margin-bottom: 20px;
        }
        .tech-tag {
            background-color: #e0f2f1;
            color: #00695c;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            margin: 0 5px;
            display: inline-block;
        }
        .section-card {
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .toc-button {
            width: 100% !important;
            justify-content: flex-start !important;
            margin-bottom: 10px !important;
            height: auto !important;
            padding: 10px !important;
        }
    """)

    with solara.Column(style={"padding": "40px", "max-width": "1200px", "margin": "0 auto"}):
        
        # --- 1. Hero Section (主視覺標題區) ---
        with solara.Column(align="center", style={"margin-bottom": "40px"}):
            # 主標題
            solara.HTML(tag="h1", unsafe_innerHTML="穿越 3275m 的雲端地誌：中橫公路時空探索", classes=["hero-title"])
            # 副標題
            solara.HTML(tag="div", unsafe_innerHTML="整合 Solara、DuckDB 與 3D 視覺化的 WEB GIS 實踐", classes=["hero-subtitle"])
            
            # 技術標籤
            with solara.Row(style={"margin-top": "15px", "flex-wrap": "wrap", "justify-content": "center"}):
                for tech in ["Python Full-Stack", "Solara", "Leafmap", "DuckDB Spatial", "USGS API", "GeoAI"]:
                    solara.HTML(tag="span", classes=["tech-tag"], unsafe_innerHTML=tech)

        solara.Markdown("---")

        # --- 2. 前言與動機 (Motivation) ---
        # 使用兩欄佈局：左邊放文字敘述，右邊放目錄
        with solara.Columns([3, 2], style={"gap": "40px"}):
            
            # 左欄：專案背景與動機
            with solara.Column():
                solara.Markdown("## 📖 前言：從海平面到 3275m 的數位敘事")
                
                with solara.Div(classes=["section-card"]):
                    solara.Markdown("### 1. 背景與動機 (Background)")
                    solara.Markdown("""
                    **地理的垂直跨度**：
                    台灣是一座高山島嶼，中橫公路（台14甲+台8線）是唯一能從埔里盆地直達海拔 3275m 武嶺，再下切至花蓮立霧溪口的「黃金剖面」。
                    
                    **實踐課程所學**：
                    傳統 GIS 軟體難以分享，我們希望利用本學期學到的 **Python 全端技術 (Solara + Leafmap + DuckDB)**，打造一個「雲原生 (Cloud-Native)」的互動圖臺。
                    """)
                    
                    solara.Markdown("### 2. 問題意識 (Problem Statement)")
                    solara.Markdown("""
                    * **資訊破碎化**：遊客往往只依賴導航，忽略了腳下的斷層帶、頭頂的崩塌地，以及消失的歷史地景。
                    * **缺乏互動**：現有的旅遊網頁多為靜態圖文，缺乏「時空互動性」（如衛星變遷、地震深度視覺化）。
                    """)
                    
                    solara.Markdown("### 3. 專案目標 (Goal)")
                    solara.Markdown("""
                    以「橫越台灣」為軸線，整合 **食衣住行育樂** 六大面向，打造完整的 StoryMap：
                    * **行與食**：整理加油站與補給攻略 (Page 07)。
                    * **育與樂**：重現滑雪場歷史 (Page 05) 與 3D 災害模擬 (Page 06)。
                    * **地與理**：結合 GeoAI 海岸變遷 (Page 08) 與 DuckDB 地震大數據 (Page 09)。
                    """)

            # 右欄：目錄 (Table of Contents) - 無圖片，純按鈕導覽
            with solara.Column():
                solara.Markdown("## 🗺️ 章節目錄 (Directory)")
                
                with solara.Div(classes=["section-card"]):
                    solara.Markdown("**請點擊下方按鈕前往各章節：**")
                    
                    # 依據故事邏輯分組
                    solara.Text("第一部：啟程與地理環境", style="font-weight: bold; color: #666; margin-top: 10px;")
                    solara.Button("01. 路線導覽：西進東出", icon_name="mdi-map-marker-path", color="primary", text=True, href="/01_Route_Story", classes=["toc-button"])
                    solara.Button("02. 地形探索：垂直剖面", icon_name="mdi-chart-bell-curve", color="primary", text=True, href="/02_Terrain_Explorer", classes=["toc-button"])
                    
                    solara.Text("第二部：水利與歷史人文", style="font-weight: bold; color: #666; margin-top: 10px;")
                    solara.Button("03. 霧社水庫：捲簾比較", icon_name="mdi-compare", color="teal", text=True, href="/03_Split_Map", classes=["toc-button"])
                    solara.Button("04. 武界引水：地下隧道", icon_name="mdi-water-pump", color="teal", text=True, href="/04_Wujie_Diversion", classes=["toc-button"])
                    solara.Button("05. 歷史滑雪場：古今對照", icon_name="mdi-snowflake", color="teal", text=True, href="/05_Ski_Resort", classes=["toc-button"])
                    
                    solara.Text("第三部：災害與實用資訊", style="font-weight: bold; color: #666; margin-top: 10px;")
                    solara.Button("06. 峽谷災害：3D 模擬", icon_name="mdi-alert-decagram", color="orange", text=True, href="/06_Canyon_Hazard", classes=["toc-button"])
                    solara.Button("07. 行前攻略：補給管制", icon_name="mdi-gas-station", color="orange", text=True, href="/07_Travel_Guide", classes=["toc-button"])
                    
                    solara.Text("第四部：進階 GIS 分析 (Tech)", style="font-weight: bold; color: #666; margin-top: 10px;")
                    solara.Button("08. 海岸變遷：GeoAI 應用", icon_name="mdi-satellite-variant", color="red", text=True, href="/08_Journey_End", classes=["toc-button"])
                    solara.Button("09. 地震大數據：DuckDB", icon_name="mdi-database-search", color="red", text=True, href="/09_Seismic_Activity", classes=["toc-button"])

        solara.Markdown("---")
        
        # --- 3. 頁尾 ---
        with solara.Column(align="center", style={"margin-top": "20px", "color": "#888"}):
            solara.Markdown("© 2025 地理資訊系統運用程式期末專題 | Developed with Solara & Leafmap")

Page()