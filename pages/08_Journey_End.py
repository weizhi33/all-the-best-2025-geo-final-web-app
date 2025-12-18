import solara
import leafmap.leafmap as leafmap

# --- 定義時光機圖源 ---
# 混合 "Esri Landsat" (歷史) 與 "Sentinel-2" (現代)
# 這讓我們能跨越 40 年以上的尺度！

TIMELAPSE_LAYERS = {
    # --- Landsat 系列 (Esri ArcGIS 服務) ---
    # 解析度 30-60m，適合看大範圍地貌變遷
    1975: {
        "url": "https://services.arcgisonline.com/arcgis/rest/services/LandsatGLS/GLS1975/ImageServer/tile/{z}/{y}/{x}",
        "name": "Landsat 1-2 (MSS)",
        "desc": "1975年代：影像較模糊(60m)，但能看到最原始的立霧溪口。"
    },
    1990: {
        "url": "https://services.arcgisonline.com/arcgis/rest/services/LandsatGLS/GLS1990/ImageServer/tile/{z}/{y}/{x}",
        "name": "Landsat 4-5 (TM)",
        "desc": "1990年代：畫質提升(30m)。觀察亞泥港口建設初期的海岸線。"
    },
    2000: {
        "url": "https://services.arcgisonline.com/arcgis/rest/services/LandsatGLS/GLS2000/ImageServer/tile/{z}/{y}/{x}",
        "name": "Landsat 7 (ETM+)",
        "desc": "千禧年：海岸線開始明顯受到港口突堤效應影響。"
    },
    2010: {
        "url": "https://services.arcgisonline.com/arcgis/rest/services/LandsatGLS/GLS2010/ImageServer/tile/{z}/{y}/{x}",
        "name": "Landsat 5/7",
        "desc": "2010年代：可見明顯的海岸侵蝕與消波塊防護。"
    },
    
    # --- Sentinel 系列 (EOX 無雲鑲嵌) ---
    # 解析度 10m，高清現代影像
    2016: {"url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2016_3857/default/g/{z}/{y}/{x}.jpg", "name": "Sentinel-2", "desc": "現代高清：哨兵衛星加入，細節更清晰。"},
    2018: {"url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2018_3857/default/g/{z}/{y}/{x}.jpg", "name": "Sentinel-2", "desc": "現代高清：觀察陰陽海的擴散。"},
    2020: {"url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2020_3857/default/g/{z}/{y}/{x}.jpg", "name": "Sentinel-2", "desc": "現代高清：河口沙洲形狀持續改變。"},
    2022: {"url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2022_3857/default/g/{z}/{y}/{x}.jpg", "name": "Sentinel-2", "desc": "最新影像：目前的海岸線狀態。"}
}

# 取得所有可用年份並排序
AVAILABLE_YEARS = sorted(TIMELAPSE_LAYERS.keys())

# 預設選中最新的一年
selected_year = solara.reactive(2022)

def create_mixed_timelapse_map(year):
    ESTUARY_CENTER = [24.138, 121.655]
    
    m = leafmap.Map(
        center=ESTUARY_CENTER,
        zoom=13, # Landsat 解析度較低，拉遠一點看大趨勢比較美
        height="700px",
        google_map=None
    )

    layer_info = TIMELAPSE_LAYERS.get(year)
    
    if layer_info:
        # 加入圖層
        m.add_tile_layer(
            url=layer_info["url"],
            name=f"{year} {layer_info['name']}",
            attribution="Esri Landsat / EOX Sentinel-2"
        )
        
        # 在地圖上顯示巨大年份標籤
        m.add_text(f"{year}", position="bottomright", fontsize=40, padding="20px")
    
    return m

@solara.component
def Page():
    map_object = solara.use_memo(
        lambda: create_mixed_timelapse_map(selected_year.value), 
        dependencies=[selected_year.value]
    )

    # 取得當前年份的描述
    current_desc = TIMELAPSE_LAYERS[selected_year.value]["desc"]
    current_source = TIMELAPSE_LAYERS[selected_year.value]["name"]

    solara.Title("終點：跨世紀海岸線")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#2c3e50", "color": "white", "height": "100%"}):
            solara.Markdown("## 🛰️ 跨世紀時光機")
            solara.Markdown("結合 **Landsat (1975-2010)** 與 **Sentinel (2016-2022)**，見證半個世紀的變遷。")
            
            solara.Markdown("---")
            
            # 核心滑桿
            solara.Markdown(f"### 📅 年份：{selected_year.value}")
            solara.SliderInt(
                label="年份",
                value=selected_year,
                min=min(AVAILABLE_YEARS),
                max=max(AVAILABLE_YEARS),
                step=None, # 設為 None 讓它只能停在我們有資料的 tick 上
                tick_labels=AVAILABLE_YEARS,
                thumb_label="always"
            )
            
            solara.Markdown("---")
            
            # 動態資訊卡
            with solara.Card(f"🎞️ {selected_year.value} ({current_source})", margin=0, elevation=1):
                solara.Markdown(f"**{current_desc}**")
                
                if selected_year.value <= 1990:
                    solara.Warning("💡 歷史影像小知識：早期的 Landsat 解析度較低 (60m/30m)，看起來會有點『馬賽克』是正常的，這就是歲月的痕跡！")

            solara.Markdown("---")
            solara.Markdown("### 🔍 觀察指南")
            solara.Markdown("""
            1. **切換 1975 -> 2022**：看「亞洲水泥港口」從無到有的過程。
            2. **觀察海岸線**：注意 1990 年後，北側海岸線如何因為港口阻擋漂沙而逐漸後退。
            """)

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    key=f"mixed-map-{selected_year.value}"
                )

Page()