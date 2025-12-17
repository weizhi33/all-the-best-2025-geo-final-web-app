import solara
import leafmap.leafmap as leafmap

def create_wushe_map():
    # 霧社水庫座標
    WUSHE_CENTER = [24.018, 121.148]
    
    # 定義圖磚網址 (暴力法，確保圖層正確!)
    URL_SATELLITE = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}" # 純衛星
    URL_TERRAIN = "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}"   # 地形圖 (帶等高線)

    # 建立捲簾地圖
    m = leafmap.split_map(
        left_layer=URL_SATELLITE,
        right_layer=URL_TERRAIN,
        left_label="衛星：淤積水色",
        right_label="地形：河谷等高線",
        center=WUSHE_CENTER,
        zoom=14,
        control_position="bottomleft"
    )
    
    # 設定高度 (ipyleaflet 修正)
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_wushe_map, dependencies=[])

    solara.Title("霧社水庫")

    with solara.Columns([1, 3]):
        
        # --- 左側：單純講水庫 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f0f2f6", "height": "100%"}):
            solara.Markdown("## 🛑 霧社水庫的哀愁")
            solara.Markdown("台14甲線起點旁的碧湖，美景之下隱藏著嚴重的淤積危機。")
            
            solara.Markdown("---")
            
            with solara.Card("🔍 觀察重點", margin=0, elevation=1):
                solara.Markdown("""
                **1. 水色差異 (左圖)**
                請拖曳捲簾，觀察靠近上游（地圖上方）的水色呈現**混濁的土黃色**。這是萬大溪帶來的巨量泥沙。
                
                **2. 縱谷地形 (右圖)**
                切換到右側地形圖，觀察密集的**等高線**。霧社水庫位於狹窄的 V 型谷中，這雖然利於蓄水，但也容易淤積。
                """)
            
            solara.Markdown("---")
            solara.Info("💡 提示：因為使用了 Google 地形圖層(lyrs=p)，右側地圖會有很漂亮的立體暈渲效果！")

        # --- 右側：地圖區 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()