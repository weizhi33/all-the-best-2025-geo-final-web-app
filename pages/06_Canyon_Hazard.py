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
    LAKE_POLYGON = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.558641, 24.173954], [121.556225, 24.175016],
                    [121.550570, 24.174189], [121.549654, 24.173071],
                    [121.553420, 24.170589], [121.558215, 24.173396],
                    [121.558641, 24.173954]
                ]]
            },
            "properties": {"名稱": "堰塞湖 (淹沒區)", "描述": "回水淹沒公路與河階地"}
        }]
    }
    m.add_geojson(LAKE_POLYGON, layer_type="fill", paint={"fill-color": "#0099ff", "fill-opacity": 0.6})

    # 5. 天然壩 (黃色)
    DAM_POLYGON = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.558502, 24.173547], [121.558858, 24.173786], 
                    [121.559375, 24.173142], [121.559111, 24.172841], 
                    [121.558502, 24.173547]
                ]]
            },
            "properties": {"名稱": "天然壩 (崩塌熱點)", "描述": "土石堆積阻斷河道"}
        }]
    }
    m.add_geojson(DAM_POLYGON, layer_type="fill", paint={"fill-color": "#ffcc00", "fill-opacity": 0.8})

    # 6. ★★★ 改用 GeoJSON 圓點 (保證點擊有反應) ★★★
    
    # 點 A: 靳珩公園 (白色圓點)
    JINHENG_POINT = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [121.561, 24.174]},
            "properties": {
                "地點": "靳珩公園",
                "歷史": "紀念民國46年殉職的靳珩段長，見證開路艱辛。"
            }
        }]
    }
    m.add_geojson(
        JINHENG_POINT, 
        layer_type="circle", 
        paint={
            "circle-color": "white", 
            "circle-radius": 8, 
            "circle-stroke-width": 2, 
            "circle-stroke-color": "black"
        },
        name="靳珩公園點位"
    )

    # 點 B: 天然壩阻塞點 (紅色圓點)
    BLOCK_POINT = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [121.559, 24.1732]},
            "properties": {
                "地點": "天然壩阻塞點",
                "風險": "峽谷最窄處，極易形成土石壩。"
            }
        }]
    }
    m.add_geojson(
        BLOCK_POINT, 
        layer_type="circle", 
        paint={
            "circle-color": "red", 
            "circle-radius": 8, 
            "circle-stroke-width": 2, 
            "circle-stroke-color": "yellow"
        },
        name="阻塞點點位"
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
                
                燕子口兩岸岩壁近乎垂直，地震時巨石崩落，卡在峽谷最窄處（請點擊地圖上的 **🔴紅點**），是形成堰塞湖的主因。
                """)
            
            solara.Markdown("---")
            
            # 3. 補充：歷史記憶
            with solara.Details(summary="🕯️ 歷史記憶：靳珩段長"):
                solara.Markdown("""
                地圖右側的 **靳珩公園**（請點擊地圖上的 **⚪白點**），即為紀念民國 46 年在此殉職的靳珩段長。
                
                當年地震發生時，他正是在這地質最脆弱的燕子口路段巡視。
                這座公園見證了中橫公路「與天爭地」的艱辛歷史。
                """)
            
            solara.Markdown("---")
            solara.Info("💡 互動提示：請點擊地圖上的「紅點」與「白點」查看詳細資訊。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()

Page()