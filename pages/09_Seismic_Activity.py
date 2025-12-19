import solara
import leafmap.foliumap as leafmap  # 使用 Folium 引擎 (靜態渲染)
import pandas as pd
import duckdb
import random
import os

# ==========================================
# 1. 資料準備：生成模擬地震數據
# ==========================================
DB_FILE = "earthquakes_sim.csv" # 改個檔名避免衝突

def generate_fake_earthquakes():
    if os.path.exists(DB_FILE):
        return

    print("正在生成地震資料庫...")
    data = []
    # 範圍：涵蓋整個中橫公路與周邊山區
    lat_min, lat_max = 23.8, 24.5
    lon_min, lon_max = 120.8, 121.9

    for _ in range(3500): # 生成 3500 筆
        lat = random.uniform(lat_min, lat_max)
        lon = random.uniform(lon_min, lon_max)
        magnitude = round(random.uniform(3.0, 7.5), 1)
        depth = round(random.uniform(2, 80), 1)
        year = random.randint(1990, 2024)
        
        # 模擬地理標籤
        if lon > 121.6: place = "東部海域"
        elif lon > 121.4: place = "太魯閣/立霧溪"
        elif lon > 121.1: place = "中央山脈/合歡山"
        else: place = "南投/埔里"

        data.append({
            "latitude": lat,
            "longitude": lon,
            "magnitude": magnitude,
            "depth": depth,
            "year": year,
            "place": place
        })
    
    df = pd.DataFrame(data)
    df.to_csv(DB_FILE, index=False)
    print("地震資料庫生成完畢！")

# 初始化資料
generate_fake_earthquakes()

# ==========================================
# 2. DuckDB 查詢引擎
# ==========================================
def query_earthquakes(min_mag, selected_year):
    con = duckdb.connect()
    # SQL 秒殺查詢
    query = f"""
        SELECT latitude, longitude, magnitude, depth, place
        FROM '{DB_FILE}' 
        WHERE magnitude >= {min_mag} 
        AND year = {selected_year}
    """
    df_result = con.execute(query).df()
    con.close()
    return df_result

# ==========================================
# 3. 響應式變數
# ==========================================
min_magnitude = solara.reactive(4.0) 
current_year = solara.reactive(2024) 

# ==========================================
# 4. 頁面元件
# ==========================================
@solara.component
def Page():
    
    # 計算並生成 HTML 字串
    def calculate_map_html():
        df = query_earthquakes(min_magnitude.value, current_year.value)
        count = len(df)
        
        # 建立地圖 (Folium)
        m = leafmap.Map(
            center=[24.15, 121.4], # 以太魯閣為中心
            zoom=9,
            google_map="HYBRID",
            draw_control=False,
            measure_control=False,
        )

        # 根據深度給顏色 (淺=紅, 深=藍)
        def get_color(depth):
            if depth < 15: return "red"
            elif depth < 30: return "orange"
            else: return "blue"

        if not df.empty:
            # 必須把 pandas series 轉成 list 才能跑迴圈 (Folium 要求)
            lats = df['latitude'].tolist()
            lons = df['longitude'].tolist()
            mags = df['magnitude'].tolist()
            depths = df['depth'].tolist()
            places = df['place'].tolist()

            for lat, lon, mag, depth, place in zip(lats, lons, mags, depths, places):
                m.add_circle_marker(
                    location=[lat, lon],
                    radius=mag * 1.5, # 規模越大圈圈越大
                    color=get_color(depth),
                    fill=True,
                    fill_color=get_color(depth),
                    fill_opacity=0.6,
                    popup=f"<b>{place}</b><br>規模: {mag}<br>深度: {depth}km"
                )
        
        return m.to_html(), count

    # 效能優化
    map_html, count = solara.use_memo(
        calculate_map_html,
        dependencies=[min_magnitude.value, current_year.value]
    )

    solara.Title("大地的心跳：地震時光機")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#2b2b2b", "color": "#e0e0e0", "height": "100%"}): # 深色主題
            solara.Markdown("## 💓 大地的心跳")
            solara.Markdown("中橫公路穿越了劇烈的造山運動帶。")
            solara.Markdown("透過 **DuckDB** 引擎，我們能瞬間回顧過去 30 年的地殼脈動。")
            
            solara.Markdown("---")
            
            with solara.Card(margin=0, elevation=1, style={"background-color": "#424242", "color": "white"}):
                solara.Markdown("### 📊 數據儀表板")
                solara.Markdown(f"年份：**{current_year.value}**")
                solara.Markdown(f"偵測地震數：**{count}** 筆")
                
            solara.Markdown("---")
            solara.Markdown("### 🎛️ 參數控制")
            
            solara.SliderInt(
                label="年份選擇",
                value=current_year,
                min=1990, max=2024,
                thumb_label="always"
            )
            
            solara.SliderFloat(
                label="最小規模 (Magnitude)",
                value=min_magnitude,
                min=3.0, max=7.0, step=0.1,
                thumb_label="always"
            )
            
            solara.Markdown("---")
            solara.Markdown("### 🔴 圖例說明")
            solara.Markdown("* **紅色**：極淺層地震 (<15km) - 破壞力最強")
            solara.Markdown("* **橘色**：淺層地震 (15-30km)")
            solara.Markdown("* **藍色**：深層地震 (>30km)")

        # --- 右側：地圖 (Iframe 渲染) ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[
                        solara.HTML(
                            tag="iframe",
                            attributes={
                                "srcdoc": map_html,
                                "width": "100%",
                                "height": "700px",
                                "style": "border: none;"
                            }
                        )
                    ],
                    style={"width": "100%", "height": "700px"},
                    key=f"seismic-map-{current_year.value}-{min_magnitude.value}"
                )

Page()