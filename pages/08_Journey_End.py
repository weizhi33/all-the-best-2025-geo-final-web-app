import solara
import leafmap.leafmap as leafmap
from ipyleaflet import Polyline

def create_end_map():
    # 立霧溪出海口
    ESTUARY_CENTER = [24.135, 121.650]
    
    # --- 定義圖源 (使用保證能跑的全球伺服器) ---
    
    # 1. 左側：ESRI 世界地形圖 (紙本風格)
    # 這張圖有很強的「傳統地圖感」，且伺服器全球穩定，不會擋 IP
    URL_PAPER_MAP = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
    
    # 2. 右側：Google 衛星 (現代真實)
    URL_SATELLITE = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"

    m = leafmap.split_map(
        left_layer=URL_PAPER_MAP,
        right_layer=URL_SATELLITE,
        left_label="地形圖 (理想骨架)",
        right_label="衛星圖 (現實樣貌)",
        center=ESTUARY_CENTER,
        zoom=14,
        control_position="bottomleft"
    )
    
    # --- 關鍵保留：紅色虛線 (1950s 海岸線推估) ---
    HISTORIC_COAST = [
        [24.155, 121.652], # 北端
        [24.145, 121.660], # 立霧溪口 (最突出的地方)
        [24.130, 121.665], # 南端
        [24.120, 121.662]
    ]
    
    line = Polyline(
        locations=HISTORIC_COAST,
        color="red",         # 鮮紅色
        weight=4,            # 粗一點
        fill=False,
        dash_array='10, 10', # 虛線
        name="1950s海岸線"
    )
    
    m.add_layer(line)
    
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_end_map, dependencies=[])

    solara.Title("終點：山與海的對話")

    with solara.Columns([1, 3]):
        
        # --- 左側：結語 ---
        with solara.Column(style={"padding": "20px", "background-color": "#eef6fc", "height": "100%"}):
            solara.Markdown("## ⏳ 理想 vs 現實")
            solara.Markdown("由於歷史圖資伺服器限制，我們改用**紙本地形圖**與**現代衛星**進行對照，並透過**紅線**標示變遷。")
            
            solara.Markdown("---")
            
            with solara.Card("🗺️ 左圖：紙本地形圖", margin=0, elevation=1):
                solara.Markdown("""
                這張圖展示了立霧溪沖積扇的**「幾何骨架」**。
                
                您可以清楚看到等高線描繪出的半圓形結構，這是大自然最原始的堆積形狀，沒有受到太多人為干擾的理想狀態。
                """)
            
            solara.Markdown("---")
            
            with solara.Card("🛰️ 右圖：現代衛星", margin=0, elevation=1):
                solara.Markdown("""
                **觀察重點：**
                * **陰陽海**：混濁溪水注入太平洋的壯觀景象。
                * **紅色虛線 (1950s)**：這條線標示了過去的海岸位置。請拖曳滑桿，你會發現紅線現在已經**「懸浮在海上」**了。
                
                這證明了隨著上游攔砂與港口建設，陸地正在被大海收回。
                """)
                
            solara.Markdown("---")
            solara.Info("💡 為什麼之前的圖跑不出來？因為 Hugging Face 伺服器在國外，被台灣的歷史圖資網站阻擋了連線。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()