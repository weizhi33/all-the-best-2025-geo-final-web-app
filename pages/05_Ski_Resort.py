import solara
import leafmap.leafmap as leafmap

# --- 定義地圖中心點 ---
# 調整中心點以涵蓋更廣的北側與西側區域
MAP_CENTER = [24.1440, 121.2830]
MAP_ZOOM = 15

# --- 互動開關狀態 ---
show_slopes = solara.reactive(True)
show_cable = solara.reactive(True)
show_markers = solara.reactive(True)

# ==========================================
# 🏔️ 歷史資料數位化成果 (v6 座標完全制霸版)
# 整合起點與終點座標，精確繪製滑雪道
# ==========================================

# 1. 歷史纜車線 (紅色線條) - 基準不變
HISTORIC_CABLE_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "雪場纜車 (已拆除)"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [121.2862, 24.1405], # 起點：滑雪山莊旁
                    [121.283547, 24.138199] # 終點：纜車遺址
                ]
            }
        }
    ]
}

# 2. 歷史滑雪道 (黃色區塊)
HISTORIC_SLOPES_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        # --- A區：高級滑雪場 (東峰坡面) ---
        {
            "type": "Feature", 
            "properties": {"name": "高級滑雪場", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2862, 24.1405], 
                    [121.2870, 24.1398], 
                    [121.2850, 24.1375], 
                    [121.2836, 24.1381], 
                    [121.2862, 24.1405]
                ]]
            }
        },
        # --- B區：中級滑雪場 (上方主線) ---
        # 起點: 24.147126, 121.282121 -> 終點: 24.146016, 121.283990
        {
            "type": "Feature", 
            "properties": {"name": "中級滑雪道 (主線)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.282121, 24.147126], # 起點 (上)
                    [121.282500, 24.147200], # 寬度擴張
                    [121.284200, 24.146200], # 往東南延伸
                    [121.283990, 24.146016], # 終點 (上)
                    [121.283500, 24.145800], 
                    [121.281800, 24.146900],
                    [121.282121, 24.147126]
                ]]
            }
        },
        # --- B-2區：中級滑雪場 (左側長滑道) ---
        # 起點: 24.146519, 121.281468 -> 終點: 24.142618, 121.280295
        # 這是一條很長的滑道，沿著西側山坡滑下來
        {
            "type": "Feature", 
            "properties": {"name": "中級滑雪道 (西側長滑道)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.281468, 24.146519], # 起點 (左)
                    [121.281900, 24.146400], 
                    [121.281000, 24.144500], # 中段
                    [121.280600, 24.142500], 
                    [121.280295, 24.142618], # 終點 (左)
                    [121.280500, 24.144800], 
                    [121.281000, 24.146600],
                    [121.281468, 24.146519]
                ]]
            }
        },
        # --- C區：初級滑雪場 (松雪樓前) ---
        {
            "type": "Feature", 
            "properties": {"name": "初級練習場", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2858, 24.1409], 
                    [121.2845, 24.1405], 
                    [121.2850, 24.1400], 
                    [121.2860, 24.1405], 
                    [121.2858, 24.1409]
                ]]
            }
        }
    ]
}

def create_ski_map(show_slopes_bool, show_cable_bool, show_markers_bool):
    m = leafmap.Map(
        center=MAP_CENTER,
        zoom=MAP_ZOOM,
        height="700px",
        # 依照指示：改回純衛星圖，看地形紋理最清楚
        google_map="SATELLITE", 
        toolbar_control=False,
        layers_control=True
    )

    # 1. 滑雪道
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

    # 2. 纜車線
    if show_cable_bool:
        m.add_geojson(
            HISTORIC_CABLE_GEOJSON,
            layer_name="雪場纜車線(舊址)",
            style={
                "color": "#FF0000", 
                "weight": 5, 
                "opacity": 0.9
            }
        )
    
    # 3. 關鍵地標點 (包含用戶指定的起點與終點)
    if show_markers_bool:
        # 既有
        m.add_marker([24.140924, 121.285825], title="松雪樓")
        m.add_marker([24.138199, 121.283547], title="纜車站遺址")
        
        # 上方滑雪道
        m.add_marker([24.147126, 121.282121], title="📍 上方滑雪道 (起點)")
        m.add_marker([24.146016, 121.283990], title="🏁 上方滑雪道 (終點)")
        
        # 左側滑雪道
        m.add_marker([24.146519, 121.281468], title="📍 左側滑雪道 (起點)")
        m.add_marker([24.142618, 121.280295], title="🏁 左側滑雪道 (終點)")
        
    return m

@solara.component
def Page():
    map_object = solara.use_memo(
        lambda: create_ski_map(show_slopes.value, show_cable.value, show_markers.value),
        dependencies=[show_slopes.value, show_cable.value, show_markers.value]
    )

    solara.Title("亞熱帶的雪國傳說")

    with solara.Columns([1, 3]):
        
        # --- 左側：故事與控制 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f4faff", "height": "100%"}):
            solara.Markdown("## ❄️ 曾經的滑雪勝地")
            solara.Markdown("透過多點座標校正，我們精確還原了合歡山滑雪場的全貌，包含兩條主要的中級滑道。")
            
            solara.Markdown("---")
            solara.Markdown("### 🗺️ 圖層控制")
            
            with solara.Card(margin=0, elevation=1):
                solara.Checkbox(label="顯示滑雪道 (黃色)", value=show_slopes)
                solara.Checkbox(label="顯示纜車線 (紅色)", value=show_cable)
                solara.Checkbox(label="顯示地標點 (藍色)", value=show_markers)
            
            solara.Markdown("---")
            
            with solara.Details(summary="📍 座標更新說明"):
                solara.Markdown("""
                我們已標註四個關鍵點位來定義滑雪場範圍：
                * **上方主線**：起點 (24.1471, 121.2821) -> 終點 (24.1460, 121.2839)。這條路線坡度適中，視野開闊。
                * **左側長滑道**：起點 (24.1465, 121.2814) -> 終點 (24.1426, 121.2802)。這條路線沿著西側山谷一路向南，距離最長。
                """)
            
            solara.Info("💡 地圖模式已切換為「衛星影像」，您可以更清楚地觀察山脈的植被與地形紋理。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    key=f"ski-map-v6-{show_slopes.value}-{show_cable.value}-{show_markers.value}"
                )

Page()