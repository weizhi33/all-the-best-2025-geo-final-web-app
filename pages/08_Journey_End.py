import solara
import leafmap.leafmap as leafmap

def create_end_map():
    # 立霧溪出海口 (崇德/新城)
    ESTUARY_CENTER = [24.135, 121.650]
    
    # --- 定義圖源大對決 ---
    
    # 1. 左側：1904 年台灣堡圖 (日治時期)
    # 這是台灣地理界最經典的「古地圖」，可以看到百年前最原始的地貌
    # 來源：台灣國土測繪中心 WMTS
    URL_HISTORY = "https://wmts.nlsc.gov.tw/wmts/JM20K_1904/default/GoogleMapsCompatible/{z}/{y}/{x}"
    
    # 2. 右側：Google 衛星 (現代)
    # 來源：Google Maps
    URL_SATELLITE = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"

    m = leafmap.split_map(
        left_layer=URL_HISTORY,
        right_layer=URL_SATELLITE,
        left_label="1904年 (台灣堡圖)",
        right_label="2024年 (Google衛星)",
        center=ESTUARY_CENTER,
        zoom=14,
        control_position="bottomleft"
    )
    
    # 我們不再需要畫那條紅線了，因為地圖本身就是最好的證據！
    
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_end_map, dependencies=[])

    solara.Title("終點：穿越百年的海岸線")

    with solara.Columns([1, 3]):
        
        # --- 左側：結語 ---
        with solara.Column(style={"padding": "20px", "background-color": "#e6f4ea", "height": "100%"}): # 換個復古綠背景
            solara.Markdown("## ⏳ 時光機：立霧溪口")
            solara.Markdown("我們不畫線了，直接讓歷史說話。")
            
            solara.Markdown("---")
            
            with solara.Card("📜 左圖：1904 年 (明治37年)", margin=0, elevation=1):
                solara.Markdown("""
                這是 **《台灣堡圖》**，日治時期最詳盡的地形圖。
                
                **觀察重點：**
                1.  **原始扇狀地**：你可以看到當時的立霧溪口是一個非常完整的扇形，沒有任何大型建物。
                2.  **消失的沙灘**：注意看海岸線的位置，當時的沙灘範圍比現在寬廣許多。
                """)
            
            solara.Markdown("---")
            
            with solara.Card("🛰️ 右圖：2024 年 (現代)", margin=0, elevation=1):
                solara.Markdown("""
                **觀察重點：**
                1.  **亞洲水泥廠**：巨大的挖掘痕跡與廠房出現在扇狀地的北側。
                2.  **海岸變化**：比較左右兩邊的海岸線，你會發現因為上游攔沙與港口突堤效應，現代的海岸線出現了明顯的侵蝕與後退。
                """)
                
            solara.Markdown("---")
            solara.Info("💡 操作：拖曳中間滑桿，直接體驗「滄海桑田」的視覺衝擊。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()