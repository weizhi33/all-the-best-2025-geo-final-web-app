import solara
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np # 用來做線性插值計算座標

# ==========================================
# 1. 數據準備：中橫公路關鍵節點
# ==========================================
route_data = [
    {"name": "埔里", "lat": 23.9700, "lon": 120.9700, "elev": 450, "dist": 0},
    {"name": "霧社", "lat": 24.0237, "lon": 121.1275, "elev": 1148, "dist": 22},
    {"name": "清境", "lat": 24.0560, "lon": 121.1620, "elev": 1750, "dist": 29},
    {"name": "鳶峰", "lat": 24.1100, "lon": 121.2200, "elev": 2750, "dist": 45},
    {"name": "武嶺", "lat": 24.1370, "lon": 121.2760, "elev": 3275, "dist": 53}, 
    {"name": "大禹嶺", "lat": 24.1812, "lon": 121.3120, "elev": 2565, "dist": 60},
    {"name": "碧綠神木", "lat": 24.1812, "lon": 121.4055, "elev": 2150, "dist": 75},
    {"name": "天祥", "lat": 24.1820, "lon": 121.4945, "elev": 480, "dist": 95},
    {"name": "太魯閣", "lat": 24.1565, "lon": 121.6225, "elev": 60, "dist": 114},
]
df_route = pd.DataFrame(route_data)

# 計算總長度
TOTAL_DIST = df_route['dist'].max()

# --- 輔助函式：根據公里數(km)計算目前的經緯度 ---
def get_location_at_km(current_km):
    # 找到目前的公里數介於哪兩個站點之間
    for i in range(len(df_route) - 1):
        p1 = df_route.iloc[i]
        p2 = df_route.iloc[i+1]
        
        if p1['dist'] <= current_km <= p2['dist']:
            # 進行線性插值 (Linear Interpolation)
            ratio = (current_km - p1['dist']) / (p2['dist'] - p1['dist'])
            lat = p1['lat'] + (p2['lat'] - p1['lat']) * ratio
            lon = p1['lon'] + (p2['lon'] - p1['lon']) * ratio
            elev = p1['elev'] + (p2['elev'] - p1['elev']) * ratio
            
            # 判斷這段路的名字 (例如：霧社 -> 清境)
            section_name = f"{p1['name']} 往 {p2['name']}"
            return lat, lon, elev, section_name
            
    # 如果超過範圍，就回傳終點
    last = df_route.iloc[-1]
    return last['lat'], last['lon'], last['elev'], "抵達終點"

# ==========================================
# 2. 響應式變數
# ==========================================
# 預設從 0km (埔里) 開始
current_km = solara.reactive(0.0)

# ==========================================
# 3. 繪圖函式 (動態版)
# ==========================================
def get_elevation_chart(current_pos_km):
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#ffffff')
    
    # 背景山形
    ax.fill_between(df_route['dist'], df_route['elev'], color='#2E8B57', alpha=0.5)
    ax.plot(df_route['dist'], df_route['elev'], color='#006400', linewidth=2)
    
    # 標示起終點與最高點文字
    for _, row in df_route.iterrows():
        if row['name'] in ["埔里", "武嶺", "太魯閣"]:
            ax.text(row['dist'], row['elev'] + 100, row['name'], ha='center', fontsize=8, fontweight='bold')

    # ★★★ 動態紅線：顯示目前位置 ★★★
    ax.axvline(x=current_pos_km, color='red', linestyle='--', linewidth=2)
    
    # 取得目前高度並標示紅點
    _, _, curr_elev, _ = get_location_at_km(current_pos_km)
    ax.scatter(current_pos_km, curr_elev, color='red', s=50, zorder=5)
    ax.text(current_pos_km + 2, curr_elev, f"{int(curr_elev)}m", color='red', fontsize=9, fontweight='bold')

    ax.set_title("中橫公路垂直剖面 (拖曳下方滑桿移動)", fontsize=10, fontweight='bold')
    ax.set_xlabel("距離 (km)")
    ax.set_ylabel("海拔 (m)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_ylim(0, 3600)
    
    plt.tight_layout()
    
    s = io.BytesIO()
    plt.savefig(s, format='png', dpi=100)
    plt.close()
    s.seek(0)
    import base64
    return f'<img src="data:image/png;base64,{base64.b64encode(s.read()).decode()}" style="width: 100%;">'

# ==========================================
# 4. 頁面元件
# ==========================================
@solara.component
def Page():
    
    # 計算目前的座標與資訊
    lat, lon, elev, section_name = get_location_at_km(current_km.value)
    
    # 產生對應的地圖
    def calculate_map():
        # 地圖中心跟隨目前的座標 (模擬開車視角)
        m = leafmap.Map(
            center=[lat, lon],
            zoom=12, # 稍微拉近一點，看清楚地形紋理
            google_map="TERRAIN",
            draw_control=False,
            measure_control=False,
        )
        
        # 畫整條路線
        points = [(row['lat'], row['lon']) for _, row in df_route.iterrows()]
        leafmap.folium.PolyLine(locations=points, color="blue", weight=3, opacity=0.5).add_to(m)

        # ★★★ 畫出一台「車」或「人」的位置 ★★★
        leafmap.folium.Marker(
            location=[lat, lon],
            popup=f"目前位置: {section_name}<br>海拔: {int(elev)}m",
            icon=leafmap.folium.Icon(color="red", icon="car", prefix="fa") # 使用車子圖示
        ).add_to(m)
        
        # 標示固定地標
        for _, row in df_route.iterrows():
            if row['name'] in ["武嶺", "埔里", "太魯閣"]:
                leafmap.folium.Marker(
                    location=[row['lat'], row['lon']],
                    tooltip=row['name'],
                    icon=leafmap.folium.Icon(color="green", icon="info-sign")
                ).add_to(m)
                
        # 記憶體輸出
        fp = io.BytesIO()
        m.save(fp, close_file=False)
        fp.seek(0)
        return fp.read().decode('utf-8')

    # 使用 use_memo 優化效能，只有當 current_km 改變時才重畫地圖
    map_html = solara.use_memo(calculate_map, dependencies=[current_km.value])
    chart_html = get_elevation_chart(current_km.value)

    solara.Title("中橫地形探索")

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        # 標題區
        with solara.Row(style={"padding": "15px", "background-color": "#f0f2f5", "align-items": "center"}):
             solara.HTML(tag="h2", unsafe_innerHTML="⛰️ 02. 地形飛覽：虛擬駕駛", style="margin: 0;")
             solara.Success("💡 請拖曳左側的「里程滑桿」，地圖與剖面圖將同步移動，帶您體驗從海平面爬升至 3000 公尺的垂直地形變化。", icon="mdi-car-side")

        # 內容區
        with solara.Columns([1, 2], style={"height": "calc(100vh - 80px)"}):
            
            # --- 左側：控制面板與剖面圖 ---
            with solara.Column(style={"padding": "20px", "background-color": "white", "height": "100%", "overflow-y": "auto"}):
                
                # 儀表板
                with solara.Card(elevation=2, style={"background-color": "#e3f2fd"}):
                    solara.Markdown("### 🚗 即時路況")
                    solara.Markdown(f"**路段**：{section_name}")
                    solara.Markdown(f"**海拔**：{int(elev)} m")
                    solara.Markdown(f"**里程**：{int(current_km.value)} km")
                
                solara.Markdown("---")
                
                # ★★★ 控制滑桿 ★★★
                solara.Markdown("### 🎚️ 里程推進 (Drag Me)")
                solara.SliderFloat(
                    label="與埔里的距離 (km)",
                    value=current_km,
                    min=0,
                    max=TOTAL_DIST,
                    step=1.0,
                    thumb_label="always"
                )
                
                solara.Markdown("---")
                
                # 剖面圖
                solara.Markdown("### 📈 垂直位置")
                solara.HTML(tag="div", unsafe_innerHTML=chart_html)
                
                solara.Info("觀察重點：注意看當滑桿通過「武嶺 (53km)」時，剖面圖達到最高點，隨後進入東段急速下降，這就是立霧溪強烈侵蝕造成的險峻地形。")

            # --- 右側：地圖 ---
            with solara.Column(style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[
                         solara.HTML(
                            tag="iframe",
                            attributes={
                                "srcdoc": map_html,
                                "width": "100%",
                                "height": "100%",
                                "style": "border: none; width: 100%; height: 750px;" 
                            }
                        )
                    ],
                    style={"height": "100%", "width": "100%"},
                    # key 加上 current_km 確保每次移動都強制更新 iframe
                    key=f"drive-map-{current_km.value}"
                )

Page()