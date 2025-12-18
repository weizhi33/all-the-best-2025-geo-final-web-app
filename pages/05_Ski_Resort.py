import solara
import leafmap.leafmap as leafmap

# --- 定義地圖中心點 (松雪樓/合歡山莊) ---
# 稍微往北移一點，讓視野更集中在東峰坡面
MAP_CENTER = [24.1375, 121.2810]
MAP_ZOOM = 16

# --- 互動開關狀態 ---
show_slopes = solara.reactive(True)
show_cable = solara.reactive(True)

# ==========================================
# 🏔️ 歷史資料數位化成果 (修正版 v2)
# 整體向北位移，使其貼近松雪樓與東峰步道
# ==========================================

# 1. 歷史滑雪道 (黃色區塊)
HISTORIC_SLOPES_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        # 靠近松雪樓下方的緩坡 (初級/練習場)
        {
            "type": "Feature", 
            "properties": {"name": "初級練習區", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2808, 24.1368], # 起點靠近日治時期石碑/松雪樓
                    [121.2818, 24.1365], 
                    [121.2822, 24.1372], 
                    [121.2812, 24.1375], 
                    [121.2808, 24.1368]
                ]]
            }
        },
        # 中段山谷 (中級滑雪場) - 沿著山凹處
        {
            "type": "Feature", 
            "properties": {"name": "中級滑雪道", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2815, 24.1372], 
                    [121.2825, 24.1370], 
                    [121.2835, 24.1382], # 往上延伸
                    [121.2825, 24.1385], 
                    [121.2815, 24.1372]
                ]]
            }
        },
        # 東峰陡坡 (高級滑雪場) - 纜車旁
        {
            "type": "Feature", 
            "properties": {"name": "高級滑雪道 (東峰坡面)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2825, 24.1380], 
                    [121.2840, 24.1395], # 更高的地方
                    [121.2845, 24.1390], 
                    [121.2830, 24.1375], 
                    [121.2825, 24.1380]
                ]]
            }
        }
    ]
}

# 2. 歷史纜車線 (紅色線條)
# 修正：起點應該在松雪樓下方馬路邊，直上東峰
HISTORIC_CABLE_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "雪場纜車 (已拆除)"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [121.2810, 24.1365], # 起點：松雪樓旁馬路邊
                    [121.2825, 24.1380], # 中途點
                    [121.2842, 24.1392]  # 終點：東峰半山腰
                ]
            }
        }
    ]
}

def create_ski_map(show_slopes_bool, show_cable_bool):
    m = leafmap.Map(
        center=MAP_CENTER,
        zoom=MAP_ZOOM,
        height="700px",
        google_map="HYBRID", 
        toolbar_control=False,
        layers_control=True
    )

    if show_slopes_bool:
        m.add_geojson(
            HISTORIC_SLOPES_GEOJSON,
            layer_name="歷史滑雪道",
            style={
                "color": "#FFD700", 
                "weight": 2,
                "opacity": 1,
                "fillColor": "#FFD700", 
                "fillOpacity": 0.4
            },
            hover_style={"fillOpacity": 0.7},
            info_mode="on_hover"
        )

    if show_cable_bool:
        m.add_geojson(
            HISTORIC_CABLE_GEOJSON,
            layer_name="雪場纜車線(舊址)",
            style={
                "color": "#FF0000", 
                "weight": 5, # 線條加粗一點更明顯
                "opacity": 0.9
            }
        )
        
    return m

@solara.component
def Page():
    map_object = solara.use_memo(
        lambda: create_ski_map(show_slopes.value, show_cable.value),
        dependencies=[show_slopes.value, show_cable.value]
    )

    solara.Title("亞熱帶的雪國傳說")

    with solara.Columns([1, 3]):
        
        # --- 左側：故事與控制 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f4faff", "height": "100%"}):
            solara.Markdown("## ❄️ 曾經的滑雪勝地")
            solara.Markdown("透過歷史考證，我們還原了 1960 年代合歡山滑雪場的設施分佈。")
            
            solara.Markdown("---")
            solara.Markdown("### 🗺️ 圖層控制")
            
            with solara.Card(margin=0, elevation=1):
                solara.Checkbox(label="顯示滑雪道 (黃色)", value=show_slopes)
                solara.Checkbox(label="顯示纜車線 (紅色)", value=show_cable)
            
            solara.Markdown("---")
            
            with solara.Details(summary="📍 位置校正說明"):
                solara.Markdown("""
                * **校正依據**：松雪樓與合歡山東峰登山步道。
                * **纜車起點**：位於松雪樓下方之道路旁，向東峰方向延伸。
                * **滑雪道**：分佈於纜車北側之山谷緩坡。
                """)
            
            solara.Info("💡 提示：現在地圖上的紅色纜車線，基本上就是沿著現在登山客走的「合歡東峰步道」旁上山的。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    key=f"ski-map-v2-{show_slopes.value}-{show_cable.value}"
                )

Page()