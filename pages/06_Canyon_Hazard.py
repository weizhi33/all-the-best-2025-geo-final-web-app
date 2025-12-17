import solara
import leafmap.maplibregl as leafmap

def create_canyon_map():
    # 視角中心：稍微往東移一點，讓壩體和湖都能看到
    YANZIKOU_CENTER = [121.557, 24.173]
    
    m = leafmap.Map(
        center=YANZIKOU_CENTER,
        zoom=16,
        pitch=75,
        bearing=-85, # 視角稍微轉一下，看這兩個物體的相對關係
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

    # 3. 堰塞湖 (藍色水域) - 位於上游
    LAKE_POLYGON = [
        [
            [121.558641, 24.173954], # 下游 (壩體後方)
            [121.556225, 24.175016],
            [121.550570, 24.174189],
            [121.549654, 24.173071],
            [121.553420, 24.170589],
            [121.558215, 24.173396],
            [121.558641, 24.173954]  # 閉合
        ]
    ]
    m.add_geojson({
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": LAKE_POLYGON},
        "properties": {"name": "堰塞湖"}
    }, layer_type="fill", paint={
        "fill-color": "#0099ff",  # 水藍色
        "fill-opacity": 0.6,
        "fill-outline-color": "#ffffff"
    })

    # 4. [新增] 天然壩 (黃色崩塌地) - 位於下游擋水處
    # 座標已經幫您轉好了 [Lon, Lat]
    DAM_POLYGON = [
        [
            [121.558502, 24.173547], # 點 1
            [121.558858, 24.173786], # 點 2
            [121.559375, 24.173142], # 點 3
            [121.559111, 24.172841], # 點 4
            [121.558502, 24.173547]  # 閉合
        ]
    ]
    m.add_geojson({
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": DAM_POLYGON},
        "properties": {"name": "天然壩/崩塌地"}
    }, layer_type="fill", paint={
        "fill-color": "#ffcc00",  # 警示黃/土石顏色
        "fill-opacity": 0.7,      # 稍微不透明一點，更有實體感
        "fill-outline-color": "#ff0000" # 紅色邊框加強警示
    })

    # 5. 標記
    # 靳珩段長紀念標記
    popup_jinheng = """
        <div style="width: 200px;">
            <h3 style="margin:0;">🕯️ 靳珩段長殉職處</h3>
            <p style="font-size:13px; margin:5px 0;">民國46年，中橫建設期間發生大地震。段長在此處巡視時，不幸被落石擊中殉職。後人將此橋改名為「靳珩橋」以資紀念。</p>
        </div>
    """
    m.add_marker(
        lng_lat=[121.561, 24.174], 
        popup={"html": popup_jinheng}
    )
    
    # 天然壩標記
    m.add_marker(
        lng_lat=[121.559, 24.1732],
        popup={"content": "<b>天然壩 (崩塌熱點)</b><br>造成河道阻塞的主因"}
    )

    m.add_layer_control()
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_canyon_map, dependencies=[])

    solara.Title("峽谷災害模擬")

    with solara.Columns([1, 3]):
        # --- 左側：詳細解說 ---
        with solara.Column(style={"padding": "20px", "background-color": "#fff5f5", "height": "100%"}):
            solara.Markdown("## ⚠️ 致命的連鎖反應")
            solara.Markdown("這裡展示了太魯閣峽谷最典型的災害模式：**崩塌 -> 堵塞 -> 堰塞湖**。")
            
            solara.Markdown("---")
            
            with solara.Card("🟡 成因：天然壩 (Landslide Dam)", margin=0, elevation=1):
                solara.Markdown("""
                地圖上的 **黃色區域** 代表崩塌落石堆積處。
                
                燕子口岩壁陡峭，一旦發生地震（如 1957 年、2024 年），大量巨石崩落，瞬間形成一道「天然土石壩」，切斷立霧溪水流。
                """)

            solara.Markdown("<br>")

            with solara.Card("🔵 結果：堰塞湖 (Barrier Lake)", margin=0, elevation=1):
                solara.Markdown("""
                地圖上的 **藍色區域** 代表回水淹沒區。
                
                水流被擋住後，水位迅速抬升，淹沒上游河谷。這對公路地基是極大的威脅。
                """)
            
            solara.Markdown("---")
            
            with solara.Details(summary="🕯️ 歷史記憶：靳珩段長"):
                solara.Markdown("""
                **只要有路，就有他們的故事。**
                
                就在這張地圖的右側（靳珩公園），是紀念 **段靳珩** 段長的地方。
                
                民國 46 年 10 月，中橫開拓期間發生強震。段長在視察災情時，正是在這險峻的燕子口路段，不幸被落石擊中殉職。這座「靳珩橋」與旁邊的隧道，就是為了感念他與工程人員的犧牲。
                """)

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()