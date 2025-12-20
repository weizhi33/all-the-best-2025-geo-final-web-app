import solara
import leafmap.maplibregl as leafmap

def create_canyon_map():
    # 1. 視角中心：稍微往西北移，同時看到「紀念公園 (右)」與「災害區 (左)」
    CENTER = [121.555, 24.174]
    
    m = leafmap.Map(
        center=CENTER,
        zoom=15.8,   # 調整縮放，讓公園和堰塞湖都在畫面內
        pitch=75,    # 3D 傾斜，感受峽谷壓迫感
        bearing=-90, # 視角朝西 (從下游往上游看)
        style="liberty",
        height="700px"
    )

    # 2. Google 混合衛星圖
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

    # 3. 3D 地形 (2.0倍誇張)
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    m.set_terrain({"source": "aws-terrain", "exaggeration": 2.0})

    # 4. 堰塞湖 (藍色)
    LAKE_POLYGON = [
        [
            [121.558641, 24.173954],
            [121.556225, 24.175016],
            [121.550570, 24.174189],
            [121.549654, 24.173071],
            [121.553420, 24.170589],
            [121.558215, 24.173396],
            [121.558641, 24.173954]
        ]
    ]
    m.add_geojson({
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": LAKE_POLYGON},
        "properties": {"name": "堰塞湖 (淹沒區)"}
    }, layer_type="fill", paint={
        "fill-color": "#0099ff", 
        "fill-opacity": 0.6,
        "fill-outline-color": "#ffffff"
    })

    # 5. 天然壩 (黃色)
    DAM_POLYGON = [
        [
            [121.558502, 24.173547], 
            [121.558858, 24.173786], 
            [121.559375, 24.173142], 
            [121.559111, 24.172841], 
            [121.558502, 24.173547]
        ]
    ]
    m.add_geojson({
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": DAM_POLYGON},
        "properties": {"name": "天然壩 (崩塌熱點)"}
    }, layer_type="fill", paint={
        "fill-color": "#ffcc00", 
        "fill-opacity": 0.8,
        "fill-outline-color": "#ff0000"
    })

    # 6. ★★★ 靳珩段長紀念標記 (保留重點) ★★★
    popup_jinheng = """
        <div style="font-family: sans-serif; width: 220px;">
            <h3 style="margin:0; color:#333; border-bottom:2px solid red; padding-bottom:5px;">🕯️ 靳珩公園</h3>
            <p style="font-size:13px; color:#555; margin-top:8px;">
                <b>「路是人開出來的，也是命換來的。」</b><br><br>
                民國46年，中橫建設期間發生大地震。靳珩段長於此處視察時，不幸被落石擊中殉職。
                後人將此橋命名為「靳珩橋」，並設立公園以茲紀念。
            </p>
        </div>
    """
    m.add_marker(
        lng_lat=[121.561, 24.174], 
        popup={"html": popup_jinheng} # 使用 HTML 豐富內容
    )
    
    # 7. 災害解說點
    m.add_marker(
        lng_lat=[121.559, 24.1732],
        popup={"content": "<b>⚠️ 天然壩阻塞點</b><br>燕子口峽谷最窄處，易形成土石壩"}
    )

    m.add_layer_control()
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_canyon_map, dependencies=[])

    solara.Title("峽谷災害模擬")

    with solara.Columns([1, 3]):
        
        # --- 左側：解說面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#fff5f5", "height": "100%"}):
            solara.Markdown("## ⚠️ 峽谷之險與歷史記憶")
            solara.Markdown("燕子口不僅是壯麗的峽谷，也是地質最脆弱、歷史最沉重的路段。")
            
            solara.Markdown("---")
            
            # 歷史故事卡片
            with solara.Card("🕯️ 歷史記憶：靳珩段長", margin=0, elevation=2):
                solara.Markdown("""
                地圖右側的 **靳珩公園** (請點擊地圖上的標記)，見證了這條路的血淚史。
                
                1957 年的地震誘發了大規模落石，奪走了靳珩段長的性命。
                **這個位置絕非偶然**——它正是峽谷最窄、地質應力最集中的地方，也是地圖上顯示最容易發生崩塌（黃色區塊）的地點。
                """)
            
            solara.Markdown("<br>")

            with solara.Card("🌊 地理災害機制", margin=0, elevation=1):
                solara.Markdown("""
                * **黃色區 (天然壩)**：崩塌土石堆積熱點。
                * **藍色區 (堰塞湖)**：若天然壩形成，溪水回堵的淹沒範圍。
                
                透過 3D 視角，您可以清楚看見公路是如何「掛」在這些危險的岩壁之上。
                """)
            
            solara.Markdown("---")
            solara.Info("💡 互動提示：右鍵拖曳可旋轉 3D 視角，感受燕子口「一線天」的垂直壓迫感。")

        # --- 右側：地圖 (MapLibre 3D) ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()

Page()