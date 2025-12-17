import solara
import leafmap.leafmap as leafmap

# 霧社水庫座標 [緯度 Lat, 經度 Lon]
# 注意：這是 ipyleaflet (2D) 的格式，經緯度順序與 maplibre 相反
WUSHE_CENTER_LAT_LON = [24.015, 121.145]

def create_split_map():
    # 建立捲簾地圖
    # 嚴格參照成功案例 pages/05_split.py 的寫法
    m = leafmap.split_map(
        left_layer="Esri.WorldImagery",  # 左側：衛星
        right_layer="OpenStreetMap",     # 右側：街道
        left_label="衛星影像",
        right_label="街道地圖",
        center=WUSHE_CENTER_LAT_LON,     # [Lat, Lon]
        zoom=14,
        control_position="bottomleft"
    )
    
    # 設定高度 (這是給 ipyleaflet 內部使用的)
    m.layout.height = "700px"
    
    return m

@solara.component
def Page():
    # 使用 use_memo 確保地圖只建立一次
    split_map_widget = solara.use_memo(create_split_map, dependencies=[])

    solara.Title("環境變遷對比")

    with solara.Columns([1, 3]):
        
        # --- 左側：導覽資訊 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f0f2f6", "height": "100%"}):
            solara.Markdown("## ⚔️ 環境今昔對照")
            solara.Markdown("透過左右滑動的捲簾(Split Map)，比較不同圖層下的地景差異。")
            
            solara.Markdown("---")
            
            with solara.Card("💧 案例：霧社水庫", margin=0, elevation=1):
                solara.Markdown("""
                又稱碧湖，是台14甲線前往清境與武嶺的必經之地。
                
                **觀察重點：**
                1. **水庫淤積**：透過衛星影像(左)，觀察濁水溪上游的泥沙淤積。
                2. **開發邊界**：比較右側地圖上的道路網與左側衛星圖中的實際開墾地。
                """)
            
            solara.Markdown("---")
            solara.Info("💡 提示：拖曳地圖中央的「直桿」來切換視野。")

        # --- 右側：捲簾地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                
                # ★★★ 關鍵修正 ★★★
                # 參考成功案例：不要直接用 element()，而是放在 Column 的 children 裡
                # 這樣 Solara 才能正確傳遞尺寸資訊，避免地圖縮成 (0,0)
                solara.Column(
                    children=[split_map_widget], 
                    style={"width": "100%", "height": "700px"}
                )

Page()