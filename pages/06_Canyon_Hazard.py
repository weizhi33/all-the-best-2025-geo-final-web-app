import solara
import leafmap.maplibregl as leafmap

def create_canyon_map():
    # 燕子口座標
    YANZIKOU_CENTER = [121.568, 24.173]
    
    m = leafmap.Map(
        center=YANZIKOU_CENTER,
        zoom=15.5,     # 稍微拉遠一點點，才能看到你設定的那些上游點位
        pitch=75,
        bearing=170,
        style="liberty",
        height="700px"
    )

    # 1. 混合衛星圖
    m.add_source("google-hybrid", {
        "type": "raster",
        "tiles": ["https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"],
        "tileSize": 256
    })
    m.add_layer({
        "id": "google-hybrid-layer",
        "type": "raster",
        "source": "google-hybrid",
        "paint": {"raster-opacity": 1.0}
    })

    # 2. 地形 (2.0倍誇張)
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256
    })
    m.set_terrain({"source": "aws-terrain", "exaggeration": 2.0})

    # 3. [修正] 使用你提供的 6 個座標點建立堰塞湖
    # 注意：已將 Google 的 (Lat, Lon) 轉換為 GIS 的 [Lon, Lat]
    # 並且為了形成多邊形，我稍微調整了順序讓它繞一圈
    LAKE_POLYGON = [
        [
            [121.558641, 24.173954], # 點 1 (起點)
            [121.550570, 24.174189], # 點 2
            [121.549654, 24.173071], # 點 3
            [121.558215, 24.173396], # 點 4
            [121.556225, 24.175016], # 點 5
            [121.553420, 24.170589], # 點 6
            [121.558641, 24.173954]  # 閉合 (回到起點)
        ]
    ]
    
    # 繪製水域
    m.add_geojson({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": LAKE_POLYGON
        },
        "properties": {"name": "模擬堰塞湖"}
    }, layer_type="fill", paint={
        "fill-color": "#0099ff",
        "fill-opacity": 0.6,
        "fill-outline-color": "#ffffff"
    })

    # 4. 災害標記 (標示在你提供的第一個點附近)
    popup_html = """<div style="font-size: 16px; font-weight: bold;">⛔ 堵塞模擬點</div>"""
    m.add_marker(
        lng_lat=[121.558641, 24.173954],
        popup={"html": popup_html}
    )
    
    m.add_layer_control()
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_canyon_map, dependencies=[])

    solara.Title("峽谷災害模擬")

    with solara.Columns([1, 3]):
        with solara.Column(style={"padding": "20px", "background-color": "#fff0f0", "height": "100%"}):
            solara.Markdown("## ⚠️ 致命的美景：堰塞湖危機")
            solara.Markdown("燕子口是太魯閣峽谷最壯麗、也是最危險的路段。")
            solara.Markdown("---")
            with solara.Card("🔥 災害劇本模擬", margin=0, elevation=1):
                solara.Markdown("""
                **情境：** 當強震或豪雨導致大量落石崩塌。
                **1. 瓶頸效應 (⚠️)** 燕子口河道極窄，崩落巨石易堵住河口。
                **2. 堰塞湖形成 (🟦)** 藍色區域顯示回水範圍 (根據實地座標模擬)。
                **3. 潰壩瞬間** 水壓衝破土石壩將對下游造成毀滅性打擊。
                """)
            solara.Markdown("---")
            solara.Markdown("### 🧐 地形觀察")
            solara.Markdown("地圖已開啟 **2.0倍地形誇張**。")

        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()