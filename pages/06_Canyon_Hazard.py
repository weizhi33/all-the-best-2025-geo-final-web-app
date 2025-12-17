import solara
import leafmap.maplibregl as leafmap

def create_canyon_map():
    # 燕子口座標
    YANZIKOU_CENTER = [121.568, 24.173]
    
    m = leafmap.Map(
        center=YANZIKOU_CENTER,
        
        # ▼▼▼ 修改這裡 ▼▼▼
        zoom=17.5     # 原本是 15，改成 16.8 (數字越大越近)
        # ▲▲▲ 修改這裡 ▲▲▲
        
        pitch=80,      # 維持這個仰角，才有抬頭看峽谷的感覺
        bearing=-80,   # 視角方向
        style="liberty",
        height="700px"
    )

    # 1. 加入 Google 混合衛星圖 (看清楚岩壁紋理)
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

    # 2. 加入超誇張地形 (Exaggeration = 2.0)
    # 為了凸顯 "V型谷" 的險峻，我們把山「拔高」兩倍
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    m.set_terrain({"source": "aws-terrain", "exaggeration": 3.0})

    # 3. [模擬] 繪製堰塞湖水域 (假設水位上升)
    # 這是一條沿著河道往上游延伸的粗線，代表積水區
    LAKE_COORDS = [
        [121.568, 24.173], # 堵塞點 (燕子口)
        [121.560, 24.175], # 靳珩橋附近
        [121.550, 24.178]  # 上游迴頭彎
    ]
    
    m.add_geojson({
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": LAKE_COORDS
        },
        "properties": {"name": "模擬堰塞湖範圍"}
    }, layer_type="line", paint={
        "line-color": "#00aaff",  # 警示藍
        "line-width": 40,         # 線畫很粗，模擬水面覆蓋河床
        "line-opacity": 0.5,      # 半透明，看得到底下的河床
        "line-blur": 5            # 邊緣模糊，更有水的感覺
    })

    # 4. 加入災害標記
    # 堵塞點 (紅色驚嘆號)
    marker_html = """
        <div style="font-size: 24px; text-shadow: 0 0 5px white;">
            ⚠️
        </div>
    """
    m.add_marker(
        lng_lat=[121.568, 24.173],
        popup={"content": "<b>堵塞熱點</b><br>燕子口最窄處，巨石易卡住河道"}
    )
    
    # 靳珩公園 (歷史災害點)
    m.add_marker(
        lng_lat=[121.561, 24.174], 
        popup={"content": "<b>靳珩公園</b><br>民國47年地震落石，靳珩段長殉職處"}
    )

    m.add_layer_control()
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_canyon_map, dependencies=[])

    solara.Title("峽谷災害模擬")

    with solara.Columns([1, 3]):
        
        # --- 左側：災害分析 ---
        with solara.Column(style={"padding": "20px", "background-color": "#fff0f0", "height": "100%"}): # 給它一個淡紅色背景，強調危險
            solara.Markdown("## ⚠️ 致命的美景：堰塞湖危機")
            solara.Markdown("燕子口是太魯閣峽谷最壯麗、也是最危險的路段。")
            
            solara.Markdown("---")
            
            with solara.Card("🔥 災害劇本模擬", margin=0, elevation=1):
                solara.Markdown("""
                **情境：** 當強震或豪雨導致大量落石崩塌。
                
                **1. 瓶頸效應 (⚠️)**
                請看地圖上的標記點。燕子口河道極窄，崩落的巨石很容易像塞子一樣堵住河口。
                
                **2. 堰塞湖形成 (🟦)**
                地圖上的 **藍色區域** 顯示了回水範圍。一旦河道受阻，溪水會迅速向上游回堵，淹沒靳珩橋甚至公路。
                
                **3. 潰壩瞬間**
                當水壓衝破土石壩，瞬間爆發的洪水(土石流)將對下游造成毀滅性打擊。
                """)
            
            solara.Markdown("---")
            solara.Markdown("### 🧐 地形觀察")
            solara.Markdown("地圖已開啟 **2.0倍地形誇張**。請旋轉視角，感受那種「插翅難飛」的垂直岩壁感。")

        # --- 右側：3D 地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()

Page()