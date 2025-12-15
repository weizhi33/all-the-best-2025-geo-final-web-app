import solara
import leafmap.maplibregl as leafmap

# 定義關鍵地點的 GeoJSON 資料
# 這樣寫比用 add_marker 更穩定，且支援 3D 後端
POINTS_DATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [120.981, 23.976]},
            "properties": {"name": "起點：台灣地理中心碑 (450m)", "color": "#00aa00"} # 綠色
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [121.276, 24.137]},
            "properties": {"name": "最高點：武嶺 (3275m)", "color": "#ff0000"} # 紅色
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [121.611, 24.151]},
            "properties": {"name": "終點：太魯閣 (60m)", "color": "#0000aa"} # 藍色
        }
    ]
}

def create_home_map():
    # 1. 建立地圖 (全覽視角)
    m = leafmap.Map(
        center=[24.05, 121.3], # 定位在路線中間
        zoom=9,
        style="positron",      # 乾淨底圖
        height="600px",
        pitch=0,               # 首頁用 2D 平視角比較清楚
        bearing=0
    )

    # 2. 加入關鍵點圖層
    # 使用 circle-layer 來畫圓點
    m.add_geojson(
        POINTS_DATA,
        layer_type="circle",
        paint={
            "circle-radius": 8,
            "circle-color": ["get", "color"], # 讀取 properties 裡的 color
            "circle-stroke-width": 2,
            "circle-stroke-color": "#ffffff"
        },
        name="關鍵地點"
    )
    
    # 3. 加入互動控制
    m.add_layer_control()
    
    return m

@solara.component
def Page():
    # 使用 use_memo 確保地圖不重複載入
    map_object = solara.use_memo(create_home_map, dependencies=[])

    with solara.Column(style={"padding": "20px"}):
        solara.Title("橫貫台灣：從平地到雲端") 
        
        solara.Markdown(r"""
        # 🏔️ 橫貫台灣：中橫與台14甲的地理探索
        
        歡迎來到我們的 GIS 期末報告！這是一個基於 **Solara** 與 **MapLibre** 建構的互動式系統。
        我們將帶領你穿越台灣最壯麗的公路——**中部橫貫公路 (台8線)** 與 **合歡山公路 (台14甲)**。
        """)

    # --- 關鍵地點展示 (卡片區) ---
    with solara.Column(style={"padding": "0 20px"}):
        solara.Markdown("### 📍 路線亮點")
        with solara.Row(gap="20px"):
            with solara.Card("起點：台灣地理中心碑", margin=0, elevation=1):
                solara.Markdown("**海拔 450m** - 位於南投埔里，是台灣地理幾何中心。")
            
            with solara.Card("最高點：武嶺", margin=0, elevation=1):
                solara.Markdown("**海拔 3275m** - 台灣公路最高點，單車騎士聖地。")
                
            with solara.Card("終點：太魯閣", margin=0, elevation=1):
                solara.Markdown("**海拔 60m** - 世界級峽谷景觀，立霧溪切穿大理岩。")

    # --- 互動地圖區 ---
    with solara.Column(style={"padding": "20px", "height": "650px"}):
        solara.Markdown("### 🗺️ 路線概覽")
        # 這裡現在放回了真正的地圖！
        with solara.Card(elevation=2, margin=0, style={"padding": "0"}):
            map_object.to_solara()

    # --- 頁尾 ---
    with solara.Column(style={"padding": "20px", "border-top": "1px solid #ddd"}):
        solara.Markdown("""
        **組員名單**：地理系 114級
        *本專案使用 GitHub Codespaces 開發，部署於 Hugging Face Spaces。*
        """)

Page()