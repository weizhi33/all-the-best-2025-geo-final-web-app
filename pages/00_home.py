import solara
import leafmap.maplibregl as leafmap

# 定義關鍵地點的 GeoJSON 資料
POINTS_DATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [120.981, 23.976]},
            "properties": {"name": "起點：台灣地理中心碑", "color": "#00aa00"} 
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [121.276, 24.137]},
            "properties": {"name": "最高點：武嶺", "color": "#ff0000"} 
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [121.611, 24.151]},
            "properties": {"name": "終點：太魯閣", "color": "#0000aa"} 
        }
    ]
}

def create_home_map():
    # 1. 建立基礎地圖
    m = leafmap.Map(
        center=[121.3, 24.05], # [經度, 緯度] 
        zoom=9,
        style="positron",
        height="600px",
        pitch=0,
        bearing=0
    )

    # 2. [修正] 手動加入資料來源 (避開 add_geojson 可能的 Bug)
    m.add_source("route_points", {
        "type": "geojson",
        "data": POINTS_DATA
    })

    # 3. [修正] 手動加入圖層 (畫圓點)
    m.add_layer({
        "id": "points-layer",
        "type": "circle",
        "source": "route_points",
        "paint": {
            "circle-radius": 8,
            "circle-color": ["get", "color"], # 從 properties 讀取顏色
            "circle-stroke-width": 2,
            "circle-stroke-color": "#ffffff"
        }
    })
    
    # 4. [修正] 手動加入文字標籤圖層
    m.add_layer({
        "id": "points-label",
        "type": "symbol",
        "source": "route_points",
        "layout": {
            "text-field": ["get", "name"], # 顯示 properties 裡的 name
            "text-offset": [0, 1.2],       # 文字稍微往上位移
            "text-size": 14,
            "text-anchor": "top"
        },
        "paint": {
            "text-color": "#333333",
            "text-halo-color": "#ffffff",
            "text-halo-width": 2
        }
    })

    m.add_layer_control()
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_home_map, dependencies=[])

    with solara.Column(style={"padding": "20px"}):
        solara.Title("橫貫台灣：從平地到雲端") 
        
        solara.Markdown(r"""
        # 🏔️ 橫貫台灣：中橫與台14甲的地理探索
        
        歡迎來到我們的 GIS 期末報告！這是一個基於 **Solara** 與 **MapLibre** 建構的互動式系統。
        我們將帶領你穿越台灣最壯麗的公路——**中部橫貫公路 (台8線)** 與 **合歡山公路 (台14甲)**。
        """)

    # 卡片區
    with solara.Column(style={"padding": "0 20px"}):
        solara.Markdown("### 📍 路線亮點")
        with solara.Row(gap="20px"):
            with solara.Card("起點：台灣地理中心碑", margin=0, elevation=1):
                solara.Markdown("**海拔 450m** - 位於南投埔里。")
            
            with solara.Card("最高點：武嶺", margin=0, elevation=1):
                solara.Markdown("**海拔 3275m** - 台灣公路最高點。")
                
            with solara.Card("終點：太魯閣", margin=0, elevation=1):
                solara.Markdown("**海拔 60m** - 世界級峽谷景觀。")

    # 地圖區
    with solara.Column(style={"padding": "20px", "height": "650px"}):
        solara.Markdown("### 🗺️ 路線概覽")
        with solara.Card(elevation=2, margin=0, style={"padding": "0"}):
            map_object.to_solara()

    # 頁尾
    with solara.Column(style={"padding": "20px", "border-top": "1px solid #ddd"}):
        solara.Markdown("**組員名單**：地理系 114級")

Page()