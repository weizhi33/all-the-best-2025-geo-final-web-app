import solara
import leafmap.leafmap as leafmap
from ipyleaflet import Polyline  # <--- 1. 引入畫線工具

def create_end_map():
    # 立霧溪出海口 (崇德/新城)
    ESTUARY_CENTER = [24.135, 121.650]
    
    # 定義圖源
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
    
    # --- GIS 繪圖：繪製「歷史海岸線示意」 ---
    # 這是根據地形推估的古海岸線 (示意線)
    HISTORIC_COAST = [
        [24.155, 121.648], # 北端 (崇德)
        [24.145, 121.658], # 立霧溪口 (往外突出)
        [24.130, 121.662], # 南端 (新城海灘)
        [24.120, 121.660]
    ]
    
    # 2. 真的把它畫上去！
    line = Polyline(
        locations=HISTORIC_COAST,
        color="red",         # 紅色
        weight=3,            # 線條粗細
        fill=False,          # 不要填滿
        dash_array='10, 10', # 虛線效果 (畫10, 空10)
        name="1950s海岸線推估"
    )
    
    m.add_layer(line) # <--- 這行最重要，之前就是漏了它！
    
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_end_map, dependencies=[])

    solara.Title("終點：山與海的對話")

    with solara.Columns([1, 3]):
        
        # --- 左側：結語 ---
        with solara.Column(style={"padding": "20px", "background-color": "#eef6fc", "height": "100%"}):
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
            
            with solara.Card("📉 環境變遷：倒退的海岸線", margin=0, elevation=1):
                solara.Markdown("""
                請看地圖上的 **🔴 紅色虛線**：
                
                這是推估 1950 年代的海岸線位置。
                
                由於上游興建水壩攔截泥沙，加上港口效應，這片美麗的扇狀地正在面臨「海岸線倒退」的危機，陸地正慢慢被大海收回。
                """)
            
            solara.Markdown("---")
            solara.Info("💡 操作：拖曳中間滑桿，比較地形骨架與真實衛星影像。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()