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
            font-size: 2.5em; /* 確保字體夠大 */
            line-height: 1.2;
        }
        .tech-tag {
            background-color: #e0f2f1;
            color: #00695c;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 5px;
            display: inline-block; /* 確保標籤排列整齊 */
            margin-bottom: 5px;
        }
        .card-container {
            transition: transform 0.2s;
            height: 100%;
        }
        .card-container:hover {
            transform: translateY(-5px);
            z-index: 10;
        }
    """)

    with solara.Column(style={"padding": "40px", "max-width": "1200px", "margin": "0 auto"}):
        
        # --- 1. Hero Section (主視覺區) ---
        with solara.Column(align="center", style={"margin-bottom": "50px"}):
            # ★★★ 修正點 1：改用 solara.HTML 來支援 classes ★★★
            solara.HTML(tag="h1", unsafe_innerHTML="🇹🇼 中橫數位地誌", classes=["hero-title"])
            
            solara.Markdown("### Cross-Island Chronicle: From Sea to Summit")
            solara.Markdown("從海平面 0m 到海拔 3275m 的地理空間探索之旅")
            
            # 技術堆疊標籤
            with solara.Row(style={"margin-top": "20px", "flex-wrap": "wrap", "justify-content": "center"}):
                for tech in ["Python", "Solara", "Leafmap", "DuckDB", "USGS API", "Sentinel-2"]:
                    solara.HTML(tag="span", classes=["tech-tag"], unsafe_innerHTML=tech)

        solara.Markdown("---")

        # --- 2. 專案亮點 (四大金剛) ---
        solara.Markdown("## 🗺️ 專案亮點導覽 (Project Highlights)")
        
        with solara.GridFixed(columns=2, row_gap="20px", column_gap="20px"):
            
            # ★★★ 修正點 2：用 solara.Div 包住 Card 來做 hover 動畫，避免 Card 不支援 classes ★★★
            
            # Card 1: 歷史滑雪場
            with solara.Div(classes=["card-container"]):
                with solara.Card(elevation=2):
                    with solara.Column():
                        solara.Markdown("### 🏔️ 05. 亞熱帶的雪國傳說")
                        solara.Markdown("**主題：歷史地理重建 (Historical GIS)**")
                        solara.Markdown("利用古地圖與航照，結合 GPS 精確座標校正，在地圖上重現 1960 年代合歡山滑雪場的纜車與滑道遺址。")
                        solara.Markdown("**技術重點：** GeoJSON 向量繪製、座標校正")
                        solara.Button("前往探索", color="primary", text=True, icon_name="mdi-arrow-right", href="/05_Ski_Resort")

            # Card 2: 海岸線變遷
            with solara.Div(classes=["card-container"]):
                with solara.Card(elevation=2):
                    with solara.Column():
                        solara.Markdown("### 🌊 08. 穿越百年的海岸線")
                        solara.Markdown("**主題：環境變遷監測 (Change Detection)**")
                        solara.Markdown("聚焦立霧溪出海口，透過 Sentinel-2 衛星影像與 USGS 歷史圖資，觀察 25 年來的海岸線退縮與陰陽海變化。")
                        solara.Markdown("**技術重點：** 衛星影像串接、時序滑桿")
                        solara.Button("前往探索", color="primary", text=True, icon_name="mdi-arrow-right", href="/08_Journey_End")

            # Card 3: 地震大數據
            with solara.Div(classes=["card-container"]):
                with solara.Card(elevation=2):
                    with solara.Column():
                        solara.Markdown("### 💓 09. 中橫震災大數據")
                        solara.Markdown("**主題：災害地理資訊 (Hazard GIS)**")
                        solara.Markdown("串接 USGS 真實資料流，利用 DuckDB 在瀏覽器端即時分析過去 25 年、數千筆地震紀錄的板塊構造。")
                        solara.Markdown("**技術重點：** DuckDB In-Memory 運算、API 串接")
                        solara.Button("前往探索", color="primary", text=True, icon_name="mdi-arrow-right", href="/09_Seismic_Activity")

            # Card 4: 峽谷災害
            with solara.Div(classes=["card-container"]):
                with solara.Card(elevation=2):
                    with solara.Column():
                        solara.Markdown("### ⚠️ 06. 峽谷之險與堰塞湖")
                        solara.Markdown("**主題：地形災害分析 (Geomorphology)**")
                        solara.Markdown("探討太魯閣峽谷脆弱的地質條件，並透過歷史案例分析土石流與堰塞湖的形成機制。")
                        solara.Markdown("**技術重點：** 地形圖判釋、災害潛勢分析")
                        solara.Button("前往探索", color="primary", text=True, icon_name="mdi-arrow-right", href="/06_Canyon_Hazard")

        solara.Markdown("---")

        # --- 3. 研究方法與資料來源 ---
        with solara.Details(summary="📚 資料來源與研究方法 (Methodology)"):
            solara.Markdown("""
            **本專案採用全端 GIS (Full-Stack GIS) 架構開發：**
            
            * **前端框架**：Solara (React-based Python framework) + Leafmap
            * **資料庫引擎**：DuckDB (WASM/In-Memory OLAP)
            * **數據來源**：
                * *地震*：USGS Earthquake Hazards Program (API)
                * *衛星*：Sentinel-2 (EOX Cloudless)
                * *歷史圖資*：中研院台灣百年歷史地圖
            """)
            
        solara.Markdown("---")
        solara.Info("💡 導覽提示：請點擊上方卡片按鈕，或使用左側選單 (Sidebar) 進行章節切換。", icon="mdi-hand-pointing-left")

Page()