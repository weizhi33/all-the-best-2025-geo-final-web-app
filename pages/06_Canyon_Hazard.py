def create_Canyon_Hazard():
    # 燕子口座標
    YANZIKOU_CENTER = [121.568, 24.173]
    
    m = leafmap.Map(
        center=YANZIKOU_CENTER,
        zoom=16.5,     # 距離稍微拉近一點，比較有臨場感
        pitch=75,      # 仰角
        bearing=-80,   # 視角方向
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

    # 3. [修正] 使用 "Polygon" (多邊形) 繪製符合河道的堰塞湖
    # 這是手動沿著燕子口河道描繪的 S 型座標
    LAKE_POLYGON = [
        [
            [121.5695, 24.1728], # 堵塞點 (下游)
            [121.5680, 24.1735], # 往上游繞
            [121.5660, 24.1725], # 轉彎處
            [121.5640, 24.1730], # 靳珩橋附近
            [121.5620, 24.1745], # 更上游
            [121.5610, 24.1750], # 湖尾端 (迴頭彎)
            
            # --- 以下是河對岸 (繞回來) ---
            [121.5615, 24.1740], 
            [121.5630, 24.1725],
            [121.5655, 24.1718],
            [121.5675, 24.1728],
            [121.5690, 24.1722],
            [121.5695, 24.1728]  # 閉合回到原點
        ]
    ]
    
    # 加入水域 (使用 fill-extrusion 讓水有一點厚度，或者用單純的 fill)
    m.add_geojson({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": LAKE_POLYGON
        },
        "properties": {"name": "模擬堰塞湖"}
    }, layer_type="fill", paint={
        "fill-color": "#0099ff",  # 鮮豔的藍色
        "fill-opacity": 0.6,      # 半透明，看得到底下的石頭
        "fill-outline-color": "#ffffff" # 白色邊框
    })

    # 4. 加入災害標記
    # 堵塞點
    popup_html = """<div style="font-size: 16px; font-weight: bold;">⛔ 堵塞點</div>"""
    m.add_marker(
        lng_lat=[121.5695, 24.1725],
        popup={"html": popup_html}
    )
    
    # 靳珩公園
    m.add_marker(
        lng_lat=[121.561, 24.174], 
        popup={"content": "靳珩公園 (淹沒區)"}
    )

    m.add_layer_control()
    return m