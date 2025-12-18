import solara
import leafmap.leafmap as leafmap

def create_end_map():
    # 立霧溪出海口 (崇德/新城)
    ESTUARY_CENTER = [24.135, 121.650]
    
    # 定義圖源
    # 左：Google 地形 (lyrs=p) -> 看完美的沖積扇等高線
    # 右：Google 衛星 (lyrs=s) -> 看陰陽海與現代地貌
    URL_TERRAIN = "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}"
    URL_SATELLITE = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"

    m = leafmap.split_map(
        left_layer=URL_TERRAIN,
        right_layer=URL_SATELLITE,
        left_label="地形：沖積扇骨架",
        right_label="衛星：陰陽海",
        center=ESTUARY_CENTER,
        zoom=14,
        control_position="bottomleft"
    )
    
    # --- GIS 小巧思：繪製「歷史海岸線示意」 ---
    # 根據地理研究，花蓮海岸線因沙源減少而在退縮
    # 我們畫一條示意線在現在海岸的外側
    HISTORIC_COAST = [
        [121.645, 24.150],
        [121.655, 24.140], # 立霧溪口，以前比較突出
        [121.660, 24.130],
        [121.662, 24.120]
    ]
    
    # 注意：split_map 的 m 是 ipyleaflet 物件，加線的方法不太一樣
    # 這裡我們用 marker 標示就好，保持畫面乾淨，把重點放在 "扇狀地" 的形狀對比
    
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_end_map, dependencies=[])

    solara.Title("終點：山與海的對話")

    with solara.Columns([1, 3]):
        
        # --- 左側：結語 ---
        with solara.Column(style={"padding": "20px", "background-color": "#eef6fc", "height": "100%"}): # 海洋藍背景
            solara.Markdown("## 🌊 旅程終點：立霧溪出海口")
            solara.Markdown("從海拔 3275m 的武嶺，我們一路追隨立霧溪，終於來到了太平洋。")
            
            solara.Markdown("---")
            
            with solara.Card("📐 幾何之美：沖積扇", margin=0, elevation=1):
                solara.Markdown("""
                請觀察左側 **地形圖**：
                
                你可以看到一個完美的**半圓形**。這是立霧溪千萬年來從山上搬運下來的砂石，在出海口堆積而成的 **「沖積扇 (Alluvial Fan)」**。
                
                我們腳下的新城、崇德聚落，其實都是立霧溪「填」出來的陸地。
                """)
            
            solara.Markdown("---")
            
            with solara.Card("🎨 色彩之美：陰陽海", margin=0, elevation=1):
                solara.Markdown("""
                請觀察右側 **衛星圖**：
                
                注意看河口的海水顏色。灰色的溪水（富含大理岩泥沙）注入深藍色的太平洋，形成了一道清晰的界線，這就是花蓮著名的地理景觀。
                """)
                
            solara.Markdown("---")
            solara.Info("💡 思考：隨著上游水壩攔截泥沙，這個完美的扇狀地正在面臨「海岸線倒退」的危機。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()