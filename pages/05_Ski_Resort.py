import solara
import leafmap.leafmap as leafmap

# --- 定義地圖中心點 ---
# 視野涵蓋松雪樓到武嶺營區
MAP_CENTER = [24.1390, 121.2835]
MAP_ZOOM = 16

# --- 互動開關狀態 ---
show_slopes = solara.reactive(True)
show_cable = solara.reactive(True)

# ==========================================
# 🏔️ 歷史資料數位化成果 (v4 終極復原版)
# 依據使用者提供的詳細分區圖 (image_e6e794) 重繪
# ==========================================

# 1. 歷史纜車線 (紅色線條)
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
                    [121.2862, 24.1405], # 起點：滑雪山莊旁登山口
                    [121.283547, 24.138199] # 終點：纜車遺址 (山上)
                ]
            }
        }
    ]
}

# 2. 歷史滑雪道 (黃色區塊 - 分區繪製)
HISTORIC_SLOPES_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        # --- A區：高級滑雪場 (東峰坡面) ---
        # 位於纜車線的「右側」(東側)，面積最大
        {
            "type": "Feature", 
            "properties": {"name": "高級滑雪場 (東峰大陡坡)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2862, 24.1405], # 滑雪山莊
                    [121.2870, 24.1398], # 往東邊延伸
                    [121.2850, 24.1375], # 山上右側邊界
                    [121.2836, 24.1381], # 貼著纜車遺址
                    [121.2862, 24.1405]
                ]]
            }
        },
        # --- B區：中級滑雪場 (山谷長滑道) ---
        # 位於纜車線「左側」，從武嶺方向蜿蜒下來到寒訓中心
        {
            "type": "Feature", 
            "properties": {"name": "中級滑雪道 (武嶺山谷線)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2848, 24.1402], # 下方匯流處
                    [121.2835, 24.1395], # 中段
                    [121.2810, 24.1375], # 上游 (靠近武嶺/道路)
                    [121.2815, 24.1385], # 上游寬度
                    [121.2840, 24.1408], # 下方寬度
                    [121.2848, 24.1402]
                ]]
            }
        },
        # --- C區：初級滑雪場 (松雪樓/營區旁) ---
        # 最下方的緩坡練習區
        {
            "type": "Feature", 
            "properties": {"name": "初級練習場", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2858, 24.1409], # 松雪樓
                    [121.2845, 24.1405], # 營區方向
                    [121.2850, 24.1400], 
                    [121.2860, 24.1405], 
                    [121.2858, 24.1409]
                ]]
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
                "weight": 5, 
                "opacity": 0.9
            }
        )
    
    # 關鍵地標
    m.add_marker([24.140924, 121.285825], title="松雪樓")
    m.add_marker([24.138199, 121.283547], title="纜車站遺址")
    m.add_marker([24.1400, 121.2865], title="滑雪山莊")
        
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
            solara.Markdown("根據 1980 年代空拍圖與設施遺址，我們完整復原了合歡山滑雪場的三大區域。")
            
            solara.Markdown("---")
            solara.Markdown("### 🗺️ 歷史分區")
            
            with solara.Card(margin=0, elevation=1):
                solara.Checkbox(label="顯示滑雪道 (分區)", value=show_slopes)
                solara.Checkbox(label="顯示纜車線 (紅色)", value=show_cable)
            
            solara.Markdown("---")
            
            with solara.Details(summary="🏔️ 滑雪場分區導覽"):
                solara.Markdown("""
                * **🔴 纜車線**：連接滑雪山莊與東峰半山腰，是全區的核心。
                * **🟡 高級滑雪場**：位於纜車線**右側**（東側），坡度最陡，直面合歡東峰。
                * **🟡 中級滑雪場**：位於纜車線**左側**（西側），是一條沿著山谷蜿蜒而下的長滑道（靠近現在的武嶺寒訓基地）。
                * **🟡 初級練習場**：位於松雪樓與滑雪山莊前方的平緩區域。
                """)
            
            solara.Info("💡 比對：請注意看纜車線左右兩側截然不同的滑道設計，這與現代登山步道的路徑有著有趣的重疊！")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    key=f"ski-map-v4-{show_slopes.value}-{show_cable.value}"
                )

Page()