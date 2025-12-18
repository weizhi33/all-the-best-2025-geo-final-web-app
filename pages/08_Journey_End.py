import solara
import leafmap.leafmap as leafmap

# --- 定義時光機圖源 (Sentinel-2 哨兵衛星) ---
# 這些是經過驗證、不用 API Key 也能跑的 URL
TIMELAPSE_LAYERS = {
    2016: {
        # 修正：2016 年的圖層名稱是 "s2cloudless_3857" (沒有年份後綴)
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2016 (起點)：哨兵二號最早的完整年度影像。注意河口沙洲的原始形狀。"
    },
    2017: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2017_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2017 年：觀察北側海岸線是否有變化。"
    },
    2018: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2018_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2018 年：注意陰陽海 (混濁海水) 的擴散範圍。"
    },
    2019: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2019_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2019 年：颱風較多的一年，輸沙量可能增加。"
    },
    2020: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2020_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2020 年：台灣大旱年。河川流量少，陰陽海可能較不明顯。"
    },
    2021: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2021_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2021 年：乾旱持續與緩解。觀察河口沙洲是否因流量變少而淤積變大？"
    },
    2022: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2022_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2022 (最新)：目前的海岸線狀態。"
    }
}

# 取得年份列表 [2016, 2017, ..., 2022]
AVAILABLE_YEARS = sorted(TIMELAPSE_LAYERS.keys())

# 使用索引 (Index) 控制滑桿，預設選最後一年 (2022)
year_index = solara.reactive(len(AVAILABLE_YEARS) - 1)

def create_sentinel_timelapse_map(current_year):
    ESTUARY_CENTER = [24.138, 121.655]
    
    m = leafmap.Map(
        center=ESTUARY_CENTER,
        zoom=13, # 哨兵解析度 10m，zoom 13-14 剛好
        height="700px",
        google_map=None
    )

    layer_info = TIMELAPSE_LAYERS.get(current_year)
    
    if layer_info:
        m.add_tile_layer(
            url=layer_info["url"],
            name=f"Sentinel-2 {current_year}",
            attribution="Sentinel-2 cloudless - https://s2maps.eu"
        )
        
        # 在地圖右下角顯示巨大年份，方便截圖或展示
        m.add_text(f"{current_year}", position="bottomright", fontsize=40, padding="20px")
    
    return m

@solara.component
def Page():
    # 透過 index 取得真實年份
    current_year_value = AVAILABLE_YEARS[year_index.value]

    map_object = solara.use_memo(
        lambda: create_sentinel_timelapse_map(current_year_value), 
        dependencies=[current_year_value]
    )

    # 取得描述
    current_desc = TIMELAPSE_LAYERS[current_year_value]["desc"]

    solara.Title("終點：海岸線時光機")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#2c3e50", "color": "white", "height": "100%"}):
            solara.Markdown("## 🛰️ 衛星時光機")
            solara.Markdown("觀測 **2016-2022** 年間，立霧溪口沙洲與水色的細微變化。")
            
            solara.Markdown("---")
            
            # 滑桿控制
            solara.Markdown(f"### 📅 年份：{current_year_value}")
            
            solara.SliderInt(
                label="時間軸",
                value=year_index,
                min=0,
                max=len(AVAILABLE_YEARS) - 1,
                step=1,
                tick_labels=AVAILABLE_YEARS, 
                thumb_label=False
            )
            
            solara.Markdown("---")
            
            with solara.Card(f"🎞️ {current_year_value} 年觀察重點", margin=0, elevation=1):
                solara.Markdown(f"**{current_desc}**")
                
            solara.Info("💡 為什麼沒有更早的年份？早期的 Landsat 衛星影像需要特殊權限才能獲取，為了確保您的網頁能穩定運行，我們選用最穩定且高清的 Sentinel-2 系列。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    key=f"sentinel-map-{current_year_value}"
                )

Page()