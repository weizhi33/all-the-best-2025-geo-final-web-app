import solara
import leafmap.maplibregl as leafmap

def create_canyon_map():
    # 1. 視角中心
    CENTER = [121.555, 24.174]
    
    m = leafmap.Map(
        center=CENTER,
        zoom=15.8,
        pitch=75,    # 3D 傾斜
        bearing=-90, # 視角朝西
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

    # 3. 3D 地形
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
        "properties": {"name": "堰塞湖"}
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
        "properties": {"name": "天然壩"}
    }, layer_type="fill", paint={
        "fill-color": "#ffcc00", 
        "fill-opacity": 0.8,
        "fill-outline-color": "#ff0000"
    })

    # 6. 加入標記 (修正 Popup 格式)
    # 使用簡單的字典格式，確保 MapLibre 能正確渲染
    
    # 天然壩阻塞點 (紅色警示)
    m.add_marker(
        lng_lat=[121.559, 24.1732],
        popup={"content": "<b>⚠️ 天然壩阻塞點</b><br>燕子口最窄處，易被落石阻斷形成土石壩。"}
    )
    
    # 靳珩公園 (灰色紀念)
    m.add_marker(
        lng_lat=[121.561, 24.174], 
        popup={"content": "<b>🕯️ 靳珩公園</b><br>紀念民國46年殉職的靳珩段長。"}
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
            
            solara.Markdown("## ⚠️ 峽谷連鎖災害")
            solara.Markdown("透過 3D 模擬，觀察燕子口「深且窄」的地形如何導致災害擴大。")
            
            solara.Markdown("---")
            
            # 1. 重點：堰塞湖 (放最上面)
            with solara.Card("🔵 關鍵災害：堰塞湖 (Barrier Lake)", margin=0, elevation=2):
                solara.Markdown("""
                請觀察地圖左側的 **藍色區域**。
                
                當下游河道被堵住時，立霧溪水無法宣洩，會迅速在峽谷中回堵。
                由於峽谷縱深大，水位抬升極快，短時間內即可淹沒上游河階地與公路，形成巨大的水體壓力。
                """)

            solara.Markdown("<br>")

            # 2. 重點：天然壩
            with solara.Card("🟡 災害成因：天然壩 (Landslide Dam)", margin=0, elevation=1):
                solara.Markdown("""
                地圖中央的 **黃色區域** 為崩塌熱點。
                
                燕子口兩岸岩壁近乎垂直，地震時巨石崩落，卡在峽谷最窄處（天然壩阻塞點），是形成堰塞湖的主因。
                """)
            
            solara.Markdown("---")
            
            # 3. 補充：歷史記憶 (放下面，用 Details 收折)
            with solara.Details(summary="🕯️ 歷史記憶：靳珩段長"):
                solara.Markdown("""
                地圖右側的 **靳珩公園**，即為紀念民國 46 年在此殉職的靳珩段長。
                當年地震發生時，他正是在這地質最脆弱的燕子口路段巡視。
                這座公園見證了中橫公路「與天爭地」的艱辛歷史。
                """)
            
            solara.Markdown("---")
            solara.Info("💡 互動提示：請點擊地圖上的標記查看詳細資訊。按住滑鼠右鍵可旋轉 3D 視角。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()

Page()