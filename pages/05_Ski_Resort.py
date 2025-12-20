import solara
import leafmap.foliumap as leafmap
import io

# ==========================================
# 1. 歷史 GIS 資料 (GeoJSON)
# ==========================================

# 纜車線 (紅色)
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

# 滑雪道 (金色區塊)
HISTORIC_SLOPES_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        # A區：東峰坡面 (高級)
        {
            "type": "Feature", 
            "properties": {"name": "高級滑雪場 (東峰)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2862, 24.1405], [121.2870, 24.1398], 
                    [121.2850, 24.1375], [121.2836, 24.1381], 
                    [121.2862, 24.1405]
                ]]
            }
        },
        # B區：主線 (中級)
        {
            "type": "Feature", 
            "properties": {"name": "中級滑雪道 (主線)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.282121, 24.147126], [121.282500, 24.147200], 
                    [121.284200, 24.146200], [121.283990, 24.146016], 
                    [121.283500, 24.145800], [121.281800, 24.146900],
                    [121.282121, 24.147126]
                ]]
            }
        },
        # B-2區：西側長滑道 (中級)
        {
            "type": "Feature", 
            "properties": {"name": "中級滑雪道 (西側長滑道)", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.281468, 24.146519], [121.281900, 24.146400], 
                    [121.281000, 24.144500], [121.280600, 24.142500], 
                    [121.280295, 24.142618], [121.280500, 24.144800], 
                    [121.281000, 24.146600], [121.281468, 24.146519]
                ]]
            }
        },
        # C區：初級練習場 (松雪樓前)
        {
            "type": "Feature", 
            "properties": {"name": "初級練習場", "color": "#FFD700"}, 
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[
                    [121.2858, 24.1409], [121.2845, 24.1405], 
                    [121.2850, 24.1400], [121.2860, 24.1405], 
                    [121.2858, 24.1409]
                ]]
            }
        }
    ]
}

# ==========================================
# 2. 響應式控制
# ==========================================
show_slopes = solara.reactive(True)
show_cable = solara.reactive(True)
show_markers = solara.reactive(True)

@solara.component
def Page():
    
    def get_ski_map():
        # 定義地圖 (使用 Google Hybrid 衛星圖)
        m = leafmap.Map(
            center=[24.1420, 121.2830],
            zoom=15,
            draw_control=False,
            measure_control=False,
        )
        m.add_tile_layer(
            url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            name="Google Hybrid",
            attribution="Google"
        )

        # 1. 繪製滑雪道 (黃色)
        if show_slopes.value:
            m.add_geojson(
                HISTORIC_SLOPES_GEOJSON,
                layer_name="歷史滑雪道",
                style_function=lambda x: {
                    "color": "#FFD700", "weight": 2, "fillOpacity": 0.4, "fillColor": "#FFD700"
                }
            )

        # 2. 繪製纜車線 (紅色)
        if show_cable.value:
            leafmap.folium.PolyLine(
                locations=[(24.1405, 121.2862), (24.138199, 121.283547)],
                color="red", weight=5, opacity=0.8, tooltip="歷史纜車線"
            ).add_to(m)

        # 3. 繪製地標 (Marker)
        if show_markers.value:
            # 既有地標
            m.add_marker([24.1409, 121.2858], popup="<b>松雪樓</b><br>昔日蔣公行館", icon=leafmap.folium.Icon(color="blue", icon="home"))
            m.add_marker([24.138199, 121.283547], popup="<b>纜車站遺址</b><br>軍方寒訓中心旁", icon=leafmap.folium.Icon(color="gray", icon="info-sign"))
            
            # ★★★ 新增地標 ★★★
            m.add_marker([24.1370, 121.2760], popup="<b>武嶺</b><br>海拔3275m 公路最高點", icon=leafmap.folium.Icon(color="orange", icon="star"))
            m.add_marker([24.1445, 121.2860], popup="<b>合歡山遊客中心</b><br>舊合歡山莊", icon=leafmap.folium.Icon(color="green", icon="user"))

            # 滑雪道起終點 (小圓點)
            slopes_points = [
                ([24.1471, 121.2821], "上方起點"), ([24.1460, 121.2839], "上方終點"),
                ([24.1465, 121.2814], "左側起點"), ([24.1426, 121.2802], "左側終點")
            ]
            for loc, title in slopes_points:
                leafmap.folium.CircleMarker(
                    location=loc, radius=3, color="yellow", fill=True, fill_color="yellow", tooltip=title
                ).add_to(m)

        return m

    # 4. 記憶體輸出 (io.BytesIO) - 確保穩定性
    m = get_ski_map()
    fp = io.BytesIO()
    m.save(fp, close_file=False)
    fp.seek(0)
    map_html_str = fp.read().decode('utf-8')

    solara.Title("亞熱帶的雪國傳說")

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        # --- 標題區 ---
        with solara.Row(style={"padding": "20px", "background-color": "#f0f2f6", "align-items": "center"}):
             solara.HTML(tag="h2", unsafe_innerHTML="🏔️ 05. 亞熱帶的雪國傳說 (1960s)", style="margin: 0;")
             solara.Success("💡 本頁透過歷史地圖與 GPS 定位，重現了台灣唯一、且已消失的「合歡山滑雪場」遺址。", icon="mdi-snowflake")

        # --- 內容區 ---
        with solara.Columns([1, 3], style={"height": "calc(100vh - 100px)"}):
            
            # 左側：歷史故事與控制
            with solara.Column(style={"padding": "20px", "background-color": "white", "height": "100%", "overflow-y": "auto"}):
                
                # 控制面板
                with solara.Card("🗺️ 圖層控制", margin=0, elevation=1):
                    solara.Checkbox(label="顯示歷史滑雪道 (黃色)", value=show_slopes)
                    solara.Checkbox(label="顯示纜車線 (紅色)", value=show_cable)
                    solara.Checkbox(label="顯示關鍵地標 (地標)", value=show_markers)

                solara.Markdown("---")

                # 歷史介紹
                solara.Markdown("### 📜 消失的歷史")
                with solara.Card(elevation=0):
                    solara.Markdown("""
                    **1. 遠東最高的滑雪場**
                    1960年代中橫通車後，因冷戰時期軍事需求，政府在此設立「陸軍寒訓中心」。
                    後來為了推廣觀光，興建了松雪樓，並引進了長達 400 公尺的纜車系統。
                    
                    **2. 纜車與滑道**
                    地圖上的**紅色直線**即為當年的纜車路線，從松雪樓旁直通下方的軍營。
                    **黃色區塊**則是當時開闢的滑雪道，包含了長達數百公尺的中級滑道。
                    
                    **3. 為何消失？**
                    隨著全球暖化導致積雪期縮短，加上國家公園成立後重視生態保育，纜車設施於 1985 年廢除，滑雪場也正式走入歷史。
                    """)
                
                solara.Markdown("---")
                solara.Info("🔍 探索提示：您可以在地圖上找到「武嶺」與「遊客中心」，藉此判斷當時滑雪場的相對位置。")

            # 右側：地圖
            with solara.Column(style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[
                         solara.HTML(
                            tag="iframe",
                            attributes={
                                "srcdoc": map_html_str,
                                "width": "100%",
                                "height": "100%",
                                "style": "border: none; width: 100%; height: 750px;" 
                            }
                        )
                    ],
                    style={"height": "100%", "width": "100%"},
                    key=f"ski-final-map-{show_slopes.value}-{show_cable.value}"
                )

Page()