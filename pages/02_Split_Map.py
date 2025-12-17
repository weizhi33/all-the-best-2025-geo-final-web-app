import solara
import leafmap.leafmap as leafmap

def create_split_map():
    # 霧社水庫座標 [緯度 Lat, 經度 Lon]
    # 注意：2D 地圖的座標順序跟 3D 的是相反的！
    WUSHE_CENTER = [24.015, 121.145]

    # 直接使用 split_map 函式建立地圖
    # 這是最穩定的寫法 (參考你之前的馬太鞍溪專案)
    m = leafmap.split_map(
        left_layer="Esri.WorldImagery",  # 左邊：衛星圖
        right_layer="OpenStreetMap",     # 右邊：街道圖
        left_label="衛星影像",
        right_label="街道地圖",
        center=WUSHE_CENTER,
        zoom=14,
        control_position="bottomleft"
    )
    
    # 強制設定高度
    m.layout.height = "700px"
    
    return m

@solara.component
def Page():
    # 使用 use_memo 避免重複渲染
    map_object = solara.use_memo(create_split_map, dependencies=[])

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
                1. **水庫淤積**：透過衛星影像(左)，可觀察濁水溪上游帶來的泥沙淤積情形，與右側地圖的水體範圍做對照。
                2. **開發邊界**：比較右側地圖上的道路網與左側衛星圖中的實際開墾地。
                """)
            
            solara.Markdown("---")
            solara.Info("💡 提示：拖曳地圖中央的「直桿」來切換視野。")

        # --- 右側：捲簾地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                # 關鍵：2D 地圖必須使用 element()
                map_object.element()

Page()