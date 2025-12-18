import solara
import leafmap.leafmap as leafmap

# --- 定義地圖中心點 (合歡山莊/松雪樓一帶) ---
MAP_CENTER = [24.1365, 121.2805]
MAP_ZOOM = 15

# --- 互動開關狀態 (Reactive Variables) ---
# 預設開啟，讓使用者一進來就看到
show_slopes = solara.reactive(True)
show_cable = solara.reactive(True)

# ==========================================
# 🏔️ 歷史資料數位化成果 (GeoJSON Data)
# 根據使用者提供的圖片 手動描繪的概略位置
# ==========================================

# 1. 歷史滑雪道 (黃色區塊 - Polygon)
HISTORIC_SLOPES_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        # 下方初級場
        {"type": "Feature", "properties": {"name": "初級滑雪場", "color": "#FFD700"}, "geometry": {"type": "Polygon", "coordinates": [[[121.2782, 24.1351], [121.2798, 24.1348], [121.2803, 24.1356], [121.2788, 24.1359], [121.2782, 24.1351]]]}},
        # 中段中級場
        {"type": "Feature", "properties": {"name": "中級滑雪場", "color": "#FFD700"}, "geometry": {"type": "Polygon", "coordinates": [[[121.2798, 24.1358], [121.2808, 24.1363], [121.2812, 24.1371], [121.2802, 24.1367], [121.2798, 24.1358]]]}},
        # 上方高級場 (東峰坡面)
        {"type": "Feature", "properties": {"name": "高級滑雪場", "color": "#FFD700"}, "geometry": {"type": "Polygon", "coordinates": [[[121.2810, 24.1370], [121.2828, 24.1381], [121.2835, 24.1376], [121.2818, 24.1365], [121.2810, 24.1370]]]}},
         # 靠近松雪樓的緩坡
        {"type": "Feature", "properties": {"name": "初級練習區", "color": "#FFD700"}, "geometry": {"type": "Polygon", "coordinates": [[[121.2815, 24.1352], [121.2830, 24.1350], [121.2835, 24.1358], [121.2820, 24.1360], [121.2815, 24.1352]]]}}
    ]
}

# 2. 歷史纜車線 (紅色線條 - LineString)
HISTORIC_CABLE_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "雪場纜車 (已拆除)"},
            "geometry": {
                "type": "LineString",
                # 從台14甲路邊往東峰方向延伸
                "coordinates": [
                    [121.2800, 24.1353], [121.2815, 24.1365], [121.2830, 24.1378]
                ]
            }
        }
    ]
}

# ==========================================
# 🗺️ 地圖建立函式
# ==========================================
def create_ski_map(show_slopes_bool, show_cable_bool):
    m = leafmap.Map(
        center=MAP_CENTER,
        zoom=MAP_ZOOM,
        height="700px",
        google_map="HYBRID", # 使用混合衛星圖，比較好辨識道路和地形
        toolbar_control=False,
        layers_control=True
    )

    # 1. 加入歷史滑雪道圖層 (如果開關開啟)
    if show_slopes_bool:
        m.add_geojson(
            HISTORIC_SLOPES_GEOJSON,
            layer_name="歷史滑雪道",
            style={
                "color": "#FFD700", # 金黃色邊框
                "weight": 2,
                "opacity": 1,
                "fillColor": "#FFD700", # 金黃色填充
                "fillOpacity": 0.4  # 半透明
            },
            hover_style={"fillOpacity": 0.7},
            info_mode="on_hover" # 滑鼠移上去顯示資訊
        )

    # 2. 加入歷史纜車線圖層 (如果開關開啟)
    if show_cable_bool:
        m.add_geojson(
            HISTORIC_CABLE_GEOJSON,
            layer_name="雪場纜車線(舊址)",
            style={
                "color": "#FF0000", # 紅色
                "weight": 4,        # 粗線條
                "opacity": 0.8
            }
        )
        
    return m

@solara.component
def Page():
    # 監聽開關變化，重新繪製地圖
    map_object = solara.use_memo(
        lambda: create_ski_map(show_slopes.value, show_cable.value),
        dependencies=[show_slopes.value, show_cable.value]
    )

    solara.Title("亞熱帶的雪國傳說")

    with solara.Columns([1, 3]):
        
        # --- 左側：故事與控制 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f4faff", "height": "100%"}): # 雪白藍背景
            solara.Markdown("## ❄️ 曾經的滑雪勝地")
            solara.Markdown("在 1960-1980 年代，合歡山曾經有全台灣唯一的天然滑雪場。")
            
            solara.Markdown("---")
            solara.Markdown("### 🗺️ 歷史遺跡復原")
            solara.Markdown("我們根據歷史資料與老照片，在地圖上標示出了當年的設施位置。")
            
            # ★★★ 互動圖層控制 Checkboxes ★★★
            with solara.Card(margin=0, elevation=1):
                solara.Checkbox(label="顯示歷史滑雪道 (黃色區域)", value=show_slopes)
                solara.Checkbox(label="顯示雪場纜車線 (紅色線條)", value=show_cable)
            
            solara.Markdown("---")
            
            with solara.Details(summary="📖 雪國歷史小故事"):
                solara.Markdown("""
                * **國軍訓練基地**：最早其實是為了軍事用途，訓練國軍具備寒地作戰能力。
                * **松雪樓**：現在的高級山莊，以前其實是滑雪場的管制中心兼器材室。
                * **纜車**：以前真的有纜車！從公路邊一路拉到東峰半山腰，可惜後來因為損壞和雪況不佳而拆除了。
                * **現在**：由於暖冬效應，積雪不夠深厚，現在已轉型為賞雪與登山健行活動為主。
                """)
            
            solara.Info("💡 操作：勾選上方圖層，對照現代衛星地圖，尋找雪場的歷史痕跡。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                # 使用 key 強制刷新，確保圖層切換順暢
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    key=f"ski-map-{show_slopes.value}-{show_cable.value}"
                )

Page()