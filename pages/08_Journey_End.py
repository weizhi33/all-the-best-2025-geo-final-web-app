import solara
import leafmap.leafmap as leafmap

# --- 定義時光機圖源 ---
TIMELAPSE_LAYERS = {
    # --- Landsat 系列 ---
    1975: {
        "url": "https://services.arcgisonline.com/arcgis/rest/services/LandsatGLS/GLS1975/ImageServer/tile/{z}/{y}/{x}",
        "name": "Landsat 1-2 (MSS)",
        "desc": "1975年代：影像較模糊，但能看到最原始的立霧溪口。"
    },
    1990: {
        "url": "https://services.arcgisonline.com/arcgis/rest/services/LandsatGLS/GLS1990/ImageServer/tile/{z}/{y}/{x}",
        "name": "Landsat 4-5 (TM)",
        "desc": "1990年代：畫質提升。觀察亞泥港口建設初期的海岸線。"
    },
    2000: {
        "url": "https://services.arcgisonline.com/arcgis/rest/services/LandsatGLS/GLS2000/ImageServer/tile/{z}/{y}/{x}",
        "name": "Landsat 7 (ETM+)",
        "desc": "千禧年：海岸線明顯受到港口突堤效應影響。"
    },
    2010: {
        "url": "https://services.arcgisonline.com/arcgis/rest/services/LandsatGLS/GLS2010/ImageServer/tile/{z}/{y}/{x}",
        "name": "Landsat 5/7",
        "desc": "2010年代：可見明顯的海岸侵蝕與消波塊防護。"
    },
    
    # --- Sentinel 系列 ---
    2016: {"url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2016_3857/default/g/{z}/{y}/{x}.jpg", "name": "Sentinel-2", "desc": "現代高清：哨兵衛星加入，細節更清晰。"},
    2018: {"url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2018_3857/default/g/{z}/{y}/{x}.jpg", "name": "Sentinel-2", "desc": "現代高清：觀察陰陽海的擴散。"},
    2020: {"url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2020_3857/default/g/{z}/{y}/{x}.jpg", "name": "Sentinel-2", "desc": "現代高清：河口沙洲形狀持續改變。"},
    2022: {"url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2022_3857/default/g/{z}/{y}/{x}.jpg", "name": "Sentinel-2", "desc": "最新影像：目前的海岸線狀態。"}
}

# 取得年份列表並排序 [1975, 1990, ..., 2022]
AVAILABLE_YEARS = sorted(TIMELAPSE_LAYERS.keys())

# ★★★ 關鍵修正：改用「索引 (Index)」來控制，預設選最後一個 (2022) ★★★
year_index = solara.reactive(len(AVAILABLE_YEARS) - 1)

def create_mixed_timelapse_map(current_year):
    ESTUARY_CENTER = [24.138, 121.655]
    
    m = leafmap.Map(
        center=ESTUARY_CENTER,
        zoom=13,
        height="700px",
        google_map=None
    )

    layer_info = TIMELAPSE_LAYERS.get(current_year)
    
    if layer_info:
        m.add_tile_layer(
            url=layer_info["url"],
            name=f"{current_year} {layer_info['name']}",
            attribution="Esri Landsat / EOX Sentinel-2"
        )
        
        # 顯示年份
        m.add_text(f"{current_year}", position="bottomright", fontsize=40, padding="20px")
    
    return m

@solara.component
def Page():
    # 根據 index 找出對應的真實年份
    current_year_value = AVAILABLE_YEARS[year_index.value]

    map_object = solara.use_memo(
        lambda: create_mixed_timelapse_map(current_year_value), 
        dependencies=[current_year_value]
    )

    # 取得描述資料
    current_desc = TIMELAPSE_LAYERS[current_year_value]["desc"]
    current_source = TIMELAPSE_LAYERS[current_year_value]["name"]

    solara.Title("終點：跨世紀海岸線")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#2c3e50", "color": "white", "height": "100%"}):
            solara.Markdown("## 🛰️ 跨世紀時光機")
            solara.Markdown("結合 Landsat 與 Sentinel，見證半世紀變遷。")
            
            solara.Markdown("---")
            
            # ★★★ 核心修正：Slider 控制 Index ★★★
            solara.Markdown(f"### 📅 年份：{current_year_value}")
            
            solara.SliderInt(
                label="時間軸",
                value=year_index,        # 控制的是 0, 1, 2, 3...
                min=0,
                max=len(AVAILABLE_YEARS) - 1,
                step=1,
                tick_labels=AVAILABLE_YEARS, # 標籤顯示真實年份
                thumb_label=False # 關閉 thumb label 避免顯示 index 數字
            )
            
            solara.Markdown("---")
            
            with solara.Card(f"🎞️ {current_year_value} ({current_source})", margin=0, elevation=1):
                solara.Markdown(f"**{current_desc}**")
                
                if current_year_value <= 1990:
                    solara.Warning("💡 歷史影像畫質較低 (馬賽克感) 是正常的，這是早期的 Landsat 技術限制。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    # key 用真實年份，確保刷新
                    key=f"mixed-map-{current_year_value}"
                )

Page()