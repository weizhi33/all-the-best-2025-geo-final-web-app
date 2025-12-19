import solara
import leafmap.foliumap as leafmap
import pandas as pd
import duckdb
import io
import datetime

# ==========================================
# 1. 資料準備：USGS 台灣 25 年地震大數據
# ==========================================
def get_taiwan_earthquake_data():
    today = datetime.date.today()
    end_date = today.strftime("%Y-%m-%d")
    
    # 鎖定台灣周邊 (規模 4.0+)
    api_url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
        f"&starttime=2000-01-01&endtime={end_date}"
        f"&minmagnitude=4.0"
        f"&minlatitude=21.0&maxlatitude=26.0"
        f"&minlongitude=119.0&maxlongitude=123.0"
    )
    
    print(f"正在下載台灣歷史地震數據: {api_url} ...")
    
    try:
        df = pd.read_csv(api_url)
        df['time'] = pd.to_datetime(df['time'])
        df['year'] = df['time'].dt.year
        df = df.dropna(subset=['latitude', 'longitude', 'mag', 'depth'])
        print(f"下載成功！共 {len(df)} 筆資料。")
        return df
    except Exception as e:
        print(f"下載失敗: {e}")
        return pd.DataFrame(columns=['latitude', 'longitude', 'mag', 'depth', 'year', 'place'])

# 下載資料
df_earthquakes = get_taiwan_earthquake_data()

# ==========================================
# 2. DuckDB 查詢
# ==========================================
def query_earthquakes(min_mag, selected_year_range):
    if df_earthquakes.empty:
        return df_earthquakes

    start_year, end_year = selected_year_range
    query = f"""
        SELECT latitude, longitude, mag, depth, place, year
        FROM df_earthquakes 
        WHERE mag >= {min_mag} 
        AND year >= {start_year} AND year <= {end_year}
    """
    return duckdb.query(query).to_df()

# ==========================================
# 3. 變數設定
# ==========================================
min_magnitude = solara.reactive(4.0) 

# 設定年份範圍
if not df_earthquakes.empty:
    max_y = int(df_earthquakes['year'].max())
    min_y = int(df_earthquakes['year'].min())
    year_range = solara.reactive([max_y - 10, max_y]) # 預設看最近 10 年
else:
    min_y, max_y = 2000, 2025
    year_range = solara.reactive([2015, 2025])

# ==========================================
# 4. 頁面元件
# ==========================================
@solara.component
def Page():
    
    def calculate_map_html():
        df = query_earthquakes(min_magnitude.value, year_range.value)
        count = len(df)
        
        # ★★★ 關鍵修改：中心點移到立霧溪出海口 (24.16, 121.62) ★★★
        m = leafmap.Map(
            center=[24.16, 121.62],
            zoom=9, # Zoom 9 剛好可以涵蓋中橫山區與外海地震帶
            google_map="HYBRID",
            draw_control=False,
            measure_control=False,
        )

        # 定義顏色 (深度)
        def get_color(depth):
            if depth < 20: return "#FF3333"      # 極淺 (紅)
            elif depth < 50: return "#FF8800"    # 淺 (橘)
            elif depth < 100: return "#FFFF00"   # 中 (黃)
            else: return "#00CC00"               # 深 (綠)

        if not df.empty:
            # 點太多時稍微縮小一點，避免糊成一團
            radius_scale = 0.8 if count > 2000 else 1.2
            
            for _, row in df.iterrows():
                leafmap.folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=(row['mag'] ** 2) * 0.15 * radius_scale,
                    color=None, # 無邊框
                    fill=True,
                    fill_color=get_color(row['depth']),
                    fill_opacity=0.6,
                    popup=f"<b>{row['place']}</b><br>年份: {row['year']}<br>規模: {row['mag']}<br>深度: {row['depth']}km"
                ).add_to(m)
        
        # 加上一個明顯的標記：立霧溪出海口
        leafmap.folium.Marker(
            location=[24.138, 121.655],
            popup="<b>立霧溪出海口</b>",
            icon=leafmap.folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

        # 記憶體輸出
        fp = io.BytesIO()
        m.save(fp, close_file=False)
        fp.seek(0)
        map_html_str = fp.read().decode('utf-8')
        
        return map_html_str, count

    map_html, count = solara.use_memo(
        calculate_map_html,
        dependencies=[min_magnitude.value, year_range.value]
    )

    solara.Title("台灣震災史：中橫視角")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#222", "color": "#eee", "height": "100%"}):
            solara.Markdown("## 🇹🇼 震央分布：立霧溪視角")
            solara.Markdown("鏡頭鎖定 **花蓮立霧溪出海口**。請觀察外海（和平海盆）高密度的地震分布，這正是板塊隱沒帶的直接證據。")
            
            solara.Markdown("---")
            
            with solara.Card(margin=0, elevation=1, style={"background-color": "#333", "color": "white"}):
                solara.Markdown("### 📊 統計儀表板")
                solara.Markdown(f"時間範圍：**{year_range.value[0]} - {year_range.value[1]}**")
                solara.Markdown(f"地震總數：**{count}** 筆")
                
            solara.Markdown("---")
            
            solara.Markdown("### 📅 年份範圍")
            solara.SliderRangeInt(label="", value=year_range, min=min_y, max=max_y, thumb_label="always")
            
            solara.Markdown("### 📉 最小規模")
            solara.SliderFloat(label="", value=min_magnitude, min=4.0, max=7.5, step=0.1, thumb_label="always")
            
            solara.Markdown("---")
            solara.Markdown("### 🎨 深度圖例")
            solara.Markdown("* <span style='color:#FF3333'>■</span> **極淺層 (<20km)**：主要分布於陸地與近海")
            solara.Markdown("* <span style='color:#FF8800'>■</span> **淺層 (20-50km)**")
            solara.Markdown("* <span style='color:#00CC00'>■</span> **深層 (>100km)**：隨板塊隱沒向西延伸")

        # --- 右側：地圖 ---
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
                    key=f"tw-quake-v2-{year_range.value}-{min_magnitude.value}"
                )

Page()