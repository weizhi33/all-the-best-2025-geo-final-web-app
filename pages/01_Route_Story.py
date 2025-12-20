import solara
import leafmap.foliumap as leafmap
import io  # <--- 關鍵解藥：記憶體操作工具

# ==========================================
# 1. 定義沿途亮點 (埔里 -> 太魯閣)
# ==========================================
ROUTE_HIGHLIGHTS = [
    {
        "id": 0,
        "title": "📍 起點：埔里地理中心",
        "location": [23.9700, 120.9700], 
        "zoom": 13,
        "content": """
        **旅程的起點**
        
        我們從台灣地理中心——埔里出發。
        由此沿著台14甲線一路爬升，告別盆地，
        準備進入高山與峽谷的地理實察之旅。
        """,
        "icon": "home",
        "color": "blue"
    },
    {
        "id": 1,
        "title": "⛰️ 最高點：武嶺 (海拔3275m)",
        "location": [24.1370, 121.2760], 
        "zoom": 15,
        "content": """
        **亞熱帶的雪國遺跡**
        
        抵達公路最高點，這裡是視野最遼闊的地方。
        **(稍後的 Page 05，我們將在此尋找 1960 年代消失的「合歡山滑雪場」與纜車遺址)**。
        """,
        "icon": "star",
        "color": "orange" 
    },
    {
        "id": 2,
        "title": "⚠️ 險境：太魯閣峽谷",
        "location": [24.1735, 121.5650], # 燕子口一帶
        "zoom": 15,
        "content": """
        **立霧溪的切割與災害**
        
        進入中橫東段，地形轉為垂直的大理石峭壁。
        壯麗的背後，隱藏著落石與堰塞湖的危機。
        **(稍後的 Page 06，我們將深入分析這裡脆弱的地質災害)**。
        """,
        "icon": "warning-sign", 
        "color": "red" 
    },
    {
        "id": 3,
        "title": "🌊 終點：立霧溪出海口",
        "location": [24.1565, 121.6225], # 牌樓/出海口
        "zoom": 14,
        "content": """
        **山海交界處**
        
        穿過太魯閣牌樓，立霧溪在此注入太平洋。
        **(最後在 Page 08，我們將利用衛星影像，觀察這片河口三角洲與海岸線的 25 年變遷)**。
        """,
        "icon": "flag",
        "color": "purple"
    }
]

# ==========================================
# 2. 響應式變數
# ==========================================
current_step = solara.reactive(0) 

# ==========================================
# 3. 頁面元件
# ==========================================
@solara.component
def Page():
    
    highlight = ROUTE_HIGHLIGHTS[current_step.value]
    
    # 建立地圖物件
    m = leafmap.Map(
        center=highlight["location"],
        zoom=highlight["zoom"],
        google_map="HYBRID",
        draw_control=False,
        measure_control=False,
    )
    
    for item in ROUTE_HIGHLIGHTS:
        is_active = (item["id"] == current_step.value)
        m.add_marker(
            location=item["location"],
            popup=item["title"],
            icon=leafmap.folium.Icon(
                color=item["color"] if is_active else "gray", 
                icon=item["icon"] if is_active else "circle",
            )
        )

    # ★★★ 關鍵修復：使用 io.BytesIO 取代 .to_html() ★★★
    # 這樣就不會去寫硬碟，避開 Permission Error
    fp = io.BytesIO()
    m.save(fp, close_file=False)
    fp.seek(0)
    map_html_str = fp.read().decode('utf-8')

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        solara.Title("中橫公路：專題路線導覽")
        
        # --- 導言區 ---
        with solara.Row(style={"padding": "20px 20px 10px 20px", "background-color": "#f8f9fa", "flex-direction": "column", "align-items": "flex-start"}):
             solara.HTML(tag="h2", unsafe_innerHTML="🛣️ 01. 旅程導覽：西進東出", style="margin: 0 0 10px 0;")
             solara.Success("💡 本頁面依序串聯本次 GIS 報告的四大場域：從埔里出發，經武嶺（滑雪場）、太魯閣峽谷（災害），終至立霧溪口（海岸變遷）。", icon="mdi-map-marker-path")

        # --- 左右分割 ---
        with solara.Columns([1, 2], style={"height": "calc(100vh - 150px)"}):
            
            # 左側：導覽
            with solara.Column(style={"padding": "30px", "background-color": "white", "height": "100%", "overflow-y": "auto"}):
                
                with solara.Row(justify="space-between", style={"margin-bottom": "20px"}):
                    solara.Button("上一站", on_click=lambda: current_step.set(max(0, current_step.value - 1)), disabled=(current_step.value == 0))
                    solara.Text(f"第 {current_step.value + 1} 站 / 共 {len(ROUTE_HIGHLIGHTS)} 站")
                    solara.Button("下一站", on_click=lambda: current_step.set(min(len(ROUTE_HIGHLIGHTS) - 1, current_step.value + 1)), disabled=(current_step.value == len(ROUTE_HIGHLIGHTS) - 1))

                solara.Markdown("---")
                
                with solara.Column(key=f"hl-final-content-{highlight['id']}"):
                    solara.HTML(tag="h3", unsafe_innerHTML=highlight["title"], style=f"color: {highlight['color']};")
                    solara.Markdown(highlight["content"])

                solara.Markdown("---")
                solara.Markdown("#### 📍 路線節點")
                with solara.Column(gap="10px"):
                    for item in ROUTE_HIGHLIGHTS:
                        style = "font-weight: bold; color: black;" if item["id"] == current_step.value else "color: gray; cursor: pointer;"
                        prefix = "👉 " if item["id"] == current_step.value else "　 "
                        
                        def make_handler(idx):
                            return lambda: current_step.set(idx)
                            
                        solara.Button(
                            label=prefix + item["title"], 
                            text=True, 
                            on_click=make_handler(item["id"]),
                            style=style
                        )

            # 右側：地圖 (iframe)
            with solara.Column(style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[
                         solara.HTML(
                            tag="iframe",
                            attributes={
                                "srcdoc": map_html_str, # 使用記憶體生成的 HTML 字串
                                "width": "100%",
                                "height": "100%",
                                "style": "border: none; width: 100%; height: 750px;" 
                            }
                        )
                    ],
                    style={"height": "100%", "width": "100%"},
                    key=f"highlight-final-map-{current_step.value}" 
                )

Page()