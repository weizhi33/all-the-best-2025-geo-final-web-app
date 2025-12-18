import solara
import leafmap.leafmap as leafmap

# --- 定義地圖中心點 ---
# 視野拉大，涵蓋從北邊的起點到南邊的松雪樓
MAP_CENTER = [24.1420, 121.2830]
MAP_ZOOM = 15

# --- 互動開關狀態 ---
show_slopes = solara.reactive(True)
show_cable = solara.reactive(True)
show_markers = solara.reactive(True) # 新增：控制地標點顯示

# ==========================================
# 🏔️ 歷史資料數位化成果 (v5 用戶指定座標版)
# ==========================================

# 1. 歷史纜車線 (紅色線條) - 維持不變
# 從滑雪山莊旁直上東峰
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
        # --- B區：中級滑雪場 (依據新座標繪製) ---
        # 這是那條最長的，從公路邊一路滑下來
        {
            "type": "Feature", 
            "properties": {"name": "中級滑雪道 (主線)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.282121, 24.147126], # ★ 新起點 (上方)
                    [121.282800, 24.146800], # 寬度
                    [121.283500, 24.142000], # 中段
                    [121.284800, 24.140200], # 下方匯流處 (武嶺營區)
                    [121.284000, 24.140800], 
                    [121.282000, 24.142500],
                    [121.281468, 24.146519], # 連接到左側起點附近
                    [121.282121, 24.147126]
                ]]
            }
        },
        # --- B-2區：左側支線 ---
        {
            "type": "Feature", 
            "properties": {"name": "中級滑雪道 (左側起點)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.281468, 24.146519], # ★ 新起點 (左側)
                    [121.282000, 24.146000], 
                    [121.282500, 24.142500], # 匯入主線
                    [121.281500, 24.143000], 
                    [121.281468, 24.146519]
                ]]
            }
        },
        # --- C區：初級滑雪場 ---
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
        google_map="HYBRID", 
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
    
    # 3. 關鍵地標點 (包含用戶指定的新座標)
    if show_markers_bool:
        # 既有點位
        m.add_marker([24.140924, 121.285825], title="松雪樓 (基地)")
        m.add_marker([24.138199, 121.283547], title="纜車站遺址")
        
        # ★ 新增用戶指定點位 (使用不同顏色或標註)
        m.add_marker([24.147126, 121.282121], title="📍 中級滑雪場起點 (上)")
        m.add_marker([24.146519, 121.281468], title="📍 中級滑雪場起點 (左)")
        
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
            solara.Markdown("根據精確座標，我們重建了那條從高處公路旁一路滑進山谷的傳奇滑雪道。")
            
            solara.Markdown("---")
            solara.Markdown("### 🗺️ 圖層控制")
            
            with solara.Card(margin=0, elevation=1):
                solara.Checkbox(label="顯示滑雪道 (黃色)", value=show_slopes)
                solara.Checkbox(label="顯示纜車線 (紅色)", value=show_cable)
                solara.Checkbox(label="顯示地標點 (藍色)", value=show_markers)
            
            solara.Markdown("---")
            
            with solara.Details(summary="📍 座標更新說明"):
                solara.Markdown("""
                新增了兩個關鍵的歷史滑雪道起點座標：
                * **上方起點** (24.1471, 121.2821)：位於公路北側高點，是中級滑雪道的主線起點。
                * **左側起點** (24.1465, 121.2814)：位於西側的支線起點。
                
                這兩條滑道最終都會匯入下方的武嶺營區山谷。
                """)

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    key=f"ski-map-v5-{show_slopes.value}-{show_cable.value}-{show_markers.value}"
                )

Page()