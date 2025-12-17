import solara
import leafmap.maplibregl as leafmap

def create_canyon_map():
    # 燕子口座標
    YANZIKOU_CENTER = [121.568, 24.173]
    
    m = leafmap.Map(
        center=YANZIKOU_CENTER,
        zoom=16.5,
        pitch=75,
        bearing=-80,
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
        "tileSize": 256,
        "encoding": "terrarium"
    })
    m.set_terrain({"source": "aws-terrain", "exaggeration": 2.0})

    # 3. 堰塞湖多邊形
    LAKE_POLYGON = [
        [
            [121.5695, 24.1728],
            [121.5680, 24.1735],
            [121.5660, 24.1725],
            [121.5640, 24.1730],
            [121.5620, 24.1745],
            [121.5610, 24.1750],
            [121.5615, 24.1740], 
            [121.5630, 24.1725],
            [121.5655, 24.1718],
            [121.5675, 24.1728],
            [121.5690, 24.1722],
            [121.5695, 24.1728]
        ]
    ]
    
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

    # 4. 災害標記
    popup_html = """<div style="font-size: 16px; font-weight: bold;">⛔ 堵塞點</div>"""
    m.add_marker(
        lng_lat=[121.5695, 24.1725],
        popup={"html": popup_html}
    )
    
    m.add_marker(
        lng_lat=[121.561, 24.174], 
        popup={"content": "靳珩公園 (淹沒區)"}
    )

    m.add_layer_control()
    return m

# ★★★ 關鍵在這裡！主函數一定要叫 Page ★★★
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
                **2. 堰塞湖形成 (🟦)** 藍色區域顯示回水範圍。
                **3. 潰壩瞬間** 水壓衝破土石壩將對下游造成毀滅性打擊。
                """)
            solara.Markdown("---")
            solara.Markdown("### 🧐 地形觀察")
            solara.Markdown("地圖已開啟 **2.0倍地形誇張**。")

        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()