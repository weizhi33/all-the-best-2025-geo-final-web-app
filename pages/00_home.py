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
        .toc-item {
            display: flex;
            align-items: center;
            padding: 8px 0;
            color: #444;
            font-size: 1rem;
        }
        .toc-icon {
            margin-right: 12px !important;
        }
    """)

    with solara.Column(style={"padding": "40px", "max-width": "1200px", "margin": "0 auto"}):
        
        # --- 1. Hero Section ---
        with solara.Column(align="center", style={"margin-bottom": "40px"}):
            solara.HTML(tag="h1", unsafe_innerHTML="穿越 3275m 的雲端地誌：中橫公路時空探索", classes=["hero-title"])
            solara.HTML(tag="div", unsafe_innerHTML="整合 Solara、DuckDB 與 3D 視覺化的 WEB GIS 實踐", classes=["hero-subtitle"])
            
            with solara.Row(style={"margin-top": "15px", "flex-wrap": "wrap", "justify-content": "center"}):
                for tech in ["Huggingface", "storymap", "Solara", "Leafmap", "DuckDB", "USGS API", "GeoAI"]:
                    solara.HTML(tag="span", classes=["tech-tag"], unsafe_innerHTML=tech)

        solara.Markdown("---")

        # --- 2. 內容與目錄 ---
        with solara.Columns([3, 2], style={"gap": "40px"}):
            
            # 左欄：專案背景
            with solara.Column():
                solara.Markdown("## 📖 前言：從海平面到 3275m 的數位實察")
                
                with solara.Div(classes=["section-card"]):
                    solara.Markdown("### 1. 背景與動機")
                    solara.Markdown("""
                    **地理的垂直跨度**：
                    台灣是一座高山島嶼，中橫公路（台14甲+台8線）是唯一能從埔里盆地直達海拔 3275m 武嶺，再下切至花蓮立霧溪口的「黃金剖面」。
                    
                    **實踐課程所學**：
                    傳統 GIS 軟體難以分享，我們希望利用本學期學到的技能打造一個互動圖臺，讓大家認識穿越台灣沿途的事物。
                    """)
                    
                    solara.Markdown("### 2. 問題意識")
                    solara.Markdown("""
                    * **資訊破碎化**：遊客往往忽略了腳下的斷層帶與消失的歷史地景。
                    * **缺乏互動**：現有網頁多為靜態圖文，缺乏時空互動性。
                    """)

            # 右欄：章節目錄 (保留 Icon，去除按鈕連結)
            with solara.Column():
                solara.Markdown("## 🗺️ 章節目錄")
                
                with solara.Div(classes=["section-card"]):
                    solara.Markdown("**本專案包含以下四大核心章節：**")
                    
                    # 定義一個內部組件方便重複使用
                    def TocEntry(icon, text, color="#444"):
                        with solara.Row(classes=["toc-item"]):
                            solara.Icon(name=icon, classes=["toc-icon"], style=f"color: {color}")
                            solara.Text(text, style=f"color: {color}")

                    solara.Text("第一部：啟程與地理環境", style="font-weight: bold; color: #666; margin-top: 10px; display: block;")
                    TocEntry("mdi-map-marker-path", "01. 路線導覽：西進東出", "#094885")
                    TocEntry("mdi-chart-bell-curve", "02. 地形探索：垂直剖面", "#094885")
                    
                    solara.Text("第二部：水利與歷史人文", style="font-weight: bold; color: #666; margin-top: 15px; display: block;")
                    TocEntry("mdi-compare", "03. 霧社水庫：捲簾比較", "#1d976c")
                    TocEntry("mdi-water-pump", "04. 武界引水：地下隧道", "#1d976c")
                    TocEntry("mdi-snowflake", "05. 歷史滑雪場：古今對照", "#1d976c")
                    
                    solara.Text("第三部：災害與實用資訊", style="font-weight: bold; color: #666; margin-top: 15px; display: block;")
                    TocEntry("mdi-alert-decagram", "06. 峽谷災害：3D 模擬", "#e67e22")
                    TocEntry("mdi-gas-station", "07. 行前攻略：補給管制", "#e67e22")
                    
                    solara.Text("第四部：進階 GIS 分析", style="font-weight: bold; color: #666; margin-top: 15px; display: block;")
                    TocEntry("mdi-satellite-variant", "08. 海岸變遷：GeoAI 應用", "#c0392b")
                    TocEntry("mdi-database-search", "09. 地震大數據：DuckDB", "#c0392b")

        solara.Markdown("---")
        
        with solara.Column(align="center", style={"margin-top": "20px", "color": "#888"}):
            solara.Markdown("© 2025 地理資訊系統運用程式期末專題 | Developed with Solara & Leafmap")

Page()