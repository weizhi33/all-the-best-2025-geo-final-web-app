import solara
import leafmap.leafmap as leafmap

def create_end_map():
    # 立霧溪出海口
    ESTUARY_CENTER = [24.138, 121.655]
    
    # --- 定義衛星圖源 (Sentinel-2 無雲鑲嵌圖) ---
    # 來源：EOX Sentinel-2 Cloudless (免費開源)
    # 這是目前不用 API Key 就能取得的最好歷史衛星圖源
    
    # 左側：2018 年
    URL_2018 = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2018_3857/default/g/{z}/{y}/{x}.jpg"
    
    # 右側：2022 年 (較新)
    URL_2022 = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2022_3857/default/g/{z}/{y}/{x}.jpg"

    m = leafmap.split_map(
        left_layer=URL_2018,
        right_layer=URL_2022,
        left_label="2018年 (衛星)",
        right_label="2022年 (衛星)",
        center=ESTUARY_CENTER,
        zoom=13, # Sentinel 解析度極限約在 13-14，拉太近會模糊
        control_position="bottomleft"
    )
    
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_end_map, dependencies=[])

    solara.Title("終點：衛星時光機")

    with solara.Columns([1, 3]):
        
        # --- 左側：導覽 ---
        with solara.Column(style={"padding": "20px", "background-color": "#eef6fc", "height": "100%"}):
            solara.Markdown("## 🛰️ 衛星眼中的變遷")
            solara.Markdown("透過 **Sentinel-2 衛星** 的年度影像，觀察立霧溪口的細微變化。")
            
            solara.Markdown("---")
            
            with solara.Card("🌊 觀察重點 1：陰陽海", margin=0, elevation=1):
                solara.Markdown("""
                拖曳中間的滑桿，比較左右兩邊的海水顏色。
                
                你會發現 **2018 (左)** 與 **2022 (右)** 的出海口泥沙擴散範圍（陰陽海）截然不同。這反映了該年度的降雨量與河流輸沙能力的差異。
                """)
            
            solara.Markdown("---")
            
            with solara.Card("🏖️ 觀察重點 2：沙灘與植被", margin=0, elevation=1):
                solara.Markdown("""
                雖然衛星解析度有限，但仍可觀察岸邊沙灘的寬度變化，以及河口沙洲的形狀改變。
                
                這是大自然最真實的紀錄，沒有任何人工繪製的線條。
                """)
                
            solara.Markdown("---")
            solara.Info("💡 註：使用歐盟哨兵衛星 (Sentinel-2) 10公尺解析度影像。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()