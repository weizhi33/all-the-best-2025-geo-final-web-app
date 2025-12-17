import solara
import leafmap.maplibregl as leafmap # 這頁我們用 3D 庫來畫線，比較漂亮

def create_wujie_map():
    # 武界壩座標
    WUJIE_CENTER = [121.05, 23.90] # 位於武界與日月潭中間
    
    m = leafmap.Map(
        center=WUJIE_CENTER,
        zoom=12,
        style="liberty",
        height="700px"
    )

    # 1. 加入 Google 混合衛星圖 (看清楚山脈與日月潭)
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

    # 2. 加入地形
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    m.set_terrain({"source": "aws-terrain", "exaggeration": 1.5})

    # 3. 繪製「引水隧道」示意線 (武界壩 -> 日月潭)
    # 這是一條大概的路徑示意
    TUNNEL_COORDS = [
        [121.048, 23.918], # 起點：武界壩
        [120.940, 23.860]  # 終點：日月潭 (大竹湖出水口)
    ]
    
    # 使用 GeoJSON 畫線
    m.add_geojson({
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": TUNNEL_COORDS
        },
        "properties": {"name": "新武界引水隧道"}
    }, layer_type="line", paint={"line-color": "#00ffff", "line-width": 5, "line-dasharray": [2, 1]})

    # 4. 加入標記
    m.add_marker(lng_lat=[121.048, 23.918], popup={"content": "起點：武界壩"})
    m.add_marker(lng_lat=[120.940, 23.860], popup={"content": "終點：日月潭出水口"})

    m.add_layer_control()
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_wujie_map, dependencies=[])

    solara.Title("武界引水")

    with solara.Columns([1, 3]):
        with solara.Column(style={"padding": "20px", "background-color": "#f0f2f6", "height": "100%"}):
            solara.Markdown("## 🌊 看不見的地下河流")
            solara.Markdown("濁水溪的水並不是全部流向大海，有一大部分在這裡被「攔截」了。")
            
            solara.Markdown("---")
            with solara.Card("工程奇蹟", margin=0, elevation=1):
                solara.Markdown("""
                **新武界引水隧道**
                
                * **長度**：約 16.5 公里
                * **功能**：越域引水
                
                這條隧道直接穿穿過中央山脈，將濁水溪的水送往**日月潭**。這也是為什麼日月潭雖然沒有大河注入，水位卻能終年保持穩定的原因。
                """)
            
            solara.Markdown("---")
            solara.Markdown("**地圖圖例**：\n * 🟦 **虛線**：引水隧道示意路徑\n * 📍 **標記**：武界壩與出水口")

        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()

Page()