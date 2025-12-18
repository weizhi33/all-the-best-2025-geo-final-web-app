import solara
import leafmap.leafmap as leafmap
from ipyleaflet import Polyline

def create_end_map():
    # 立霧溪出海口
    ESTUARY_CENTER = [24.135, 121.650]
    
    # --- 定義圖源大對決 ---
    
    # 1. 左側：1944 年美軍地形圖 (US Army Map)
    # 這張圖比 1904 年的更接近現代一點，海岸線描繪非常清晰
    # 來源：台灣國土測繪中心 WMTS
    URL_HISTORY = "https://wmts.nlsc.gov.tw/wmts/AM50K_1944/default/GoogleMapsCompatible/{z}/{y}/{x}"
    
    # 2. 右側：Google 衛星 (現代)
    URL_SATELLITE = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"

    m = leafmap.split_map(
        left_layer=URL_HISTORY,
        right_layer=URL_SATELLITE,
        left_label="1944年 (美軍地圖)",
        right_label="2024年 (現代衛星)",
        center=ESTUARY_CENTER,
        zoom=14,
        control_position="bottomleft"
    )
    
    # --- 關鍵：保留紅色虛線 (1950s 海岸線推估) ---
    HISTORIC_COAST = [
        [24.155, 121.652], # 北端
        [24.145, 121.660], # 當時的河口尖端
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
    
    # 把紅線加上去！
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
            solara.Markdown("## ⏳ 穿越時空的海岸線")
            solara.Markdown("我們結合了 **古地圖** 與 **歷史推估線**，還原立霧溪口的原始樣貌。")
            
            solara.Markdown("---")
            
            with solara.Card("📜 左圖：1944 年 (美軍繪製)", margin=0, elevation=1):
                solara.Markdown("""
                這是二戰期間美軍繪製的台灣地形圖。
                
                **觀察重點：**
                * **清晰的扇狀地**：你可以看到當時的立霧溪口，是一個沒有被切割的完整扇形。
                * **海岸位置**：請注意圖中的黑色海岸線，它與右邊的現代衛星圖有顯著差異。
                """)
            
            solara.Markdown("---")
            
            with solara.Card("🔴 紅線：消逝的國土", margin=0, elevation=1):
                solara.Markdown("""
                地圖上的 **紅色虛線** 代表 1950 年代推估的海岸位置。
                
                **為什麼海岸會後退？**
                當你在右側衛星圖看到 **「亞洲水泥廠」** 的港口與防波堤時，就能找到答案。人為設施阻擋了沿岸漂沙的補給，加上上游水壩攔砂，導致大海開始「吃掉」陸地。
                """)
                
            solara.Markdown("---")
            solara.Info("💡 操作：拖曳中間滑桿。你會發現紅線（舊海岸）現在已經懸浮在海面上了！")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()