import solara
import leafmap.foliumap as leafmap
import pandas as pd
import duckdb
import io
import datetime

# ==========================================
# 1. 資料準備：USGS 台灣專屬歷史查詢
# ==========================================
def get_taiwan_earthquake_data():
    # 動態產生今天的日期，確保資料永遠最新
    today = datetime.date.today()
    end_date = today.strftime("%Y-%m-%d")
    
    # --- USGS API 參數設定 (這就是抓多一點資料的關鍵) ---
    # format=csv: 格式
    # starttime=2000-01-01: 從 2000 年開始抓 (25年數據！)
    # minmagnitude=4.0: 只抓規模 4 以上 (避免資料量爆掉，且太小的地震沒感覺)
    # min/max lat/lon: 鎖定台灣周邊方框 (Taiwan Bounding Box)
    api_url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
        f"&starttime=2000-01-01&endtime={end_date}"
        f"&minmagnitude=4.0"
        f"&minlatitude=21.0&maxlatitude=26.0"
        f"&minlongitude=119.0&maxlongitude=123.0"
    )
    
    print(f"正在下載台灣 25 年地震大數據: {api_url} ...")
    
    try:
        df = pd.read_csv(api_url)
        
        # 資料清理
        df['time'] = pd.to_datetime(df['time'])
        df['year'] = df['time'].dt.year
        df = df.dropna(subset=['latitude', 'longitude', 'mag', 'depth'])
        
        print(f"下載成功！取得 {len(df)} 筆台灣真實地震資料。")
        return df
        
    except Exception as e:
        print(f"下載失敗: {e}")
        return pd.DataFrame(columns=['latitude', 'longitude', 'mag', 'depth', 'year', 'place'])

# 下載資料 (只執行一次)
df_earthquakes = get_taiwan_earthquake_data()

# ==========================================
# 2. DuckDB 查詢
# ==========================================
def query_earthquakes(min_mag, selected_year_range):
    if df_earthquakes.empty:
        return df_earthquakes

    # 解包年份範圍 (例如: [2010, 2020])
    start_year, end_year = selected_year_range

    # SQL 篩選：使用年份範圍查詢
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

# 設定年份範圍 (預設看最近 5 年)
current_year = 2025 # 暫定
if not df_earthquakes.empty:
    max_y = int(df_earthquakes['year'].max())
    min_y = int(df_earthquakes['year'].min())
    # 預設選取範圍
    year_range = solara.reactive([max_y - 5, max_y])
else:
    min_y, max_y = 2000, 2025
    year_range = solara.reactive([2020, 2025])

# ==========================================
# 4. 頁面元件
# ==========================================
@solara.component
def Page():
    
    def calculate_map_html():
        df = query_earthquakes(min_magnitude.value, year_range.value)
        count = len(df)
        
        # 中心點設在台灣 (南投)
        m = leafmap.Map(
            center=[23.8, 121.0],
            zoom=7,
            google_map="HYBRID",
            draw_control=False,
            measure_control=False,
        )

        def get_color(depth):
            if depth < 20: return "#FF3333"      # 極淺層 (紅)
            elif depth < 50: return "#FF8800"    # 淺層 (橘)
            elif depth < 100: return "#FFFF00"   # 中層 (黃)
            else: return "#00CC00"               # 深層 (綠)

        if not df.empty:
            # 為了效能，如果點太多 (>1000)，稍微縮小半徑
            radius_scale = 1.0 if count < 1000 else 0.8
            
            for _, row in df.iterrows():
                leafmap.folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    # 規模越大圈越大
                    radius=(row['mag'] ** 2) * 0.15 * radius_scale, 
                    color=None,
                    fill=True,
                    fill_color=get_color(row['depth']),
                    fill_opacity=0.6,
                    popup=f"<b>{row['place']}</b><br>年份: {row['year']}<br>規模: {row['mag']}<br>深度: {row['depth']}km"
                ).add_to(m)

        # 記憶體輸出 (避開 Read-only error)
        fp = io.BytesIO()
        m.save(fp, close_file=False)
        fp.seek(0)
        map_html_str = fp.read().decode('utf-8')
        
        return map_html_str, count

    map_html, count = solara.use_memo(
        calculate_map_html,
        dependencies=[min_magnitude.value, year_range.value]
    )

    solara.Title("台灣震災史：USGS 大數據")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#222", "color": "#eee", "height": "100%"}):
            solara.Markdown("## 🇹🇼 台灣震災大數據")
            solara.Markdown("透過 USGS API，我們撈取了 **2000 年至今**，發生在台灣周邊規模 4.0 以上的真實地震紀錄。")
            
            solara.Markdown("---")
            
            with solara.Card(margin=0, elevation=1, style={"background-color": "#333", "color": "white"}):
                solara.Markdown("### 📊 數據統計")
                solara.Markdown(f"時間跨度：**{year_range.value[0]} - {year_range.value[1]}**")
                solara.Markdown(f"篩選筆數：**{count}** 筆")
                
            solara.Markdown("---")
            
            # 雙頭滑桿 (Range Slider)
            solara.Markdown("### 📅 年份範圍")
            solara.SliderRangeInt(
                label="", 
                value=year_range, 
                min=min_y, 
                max=max_y, 
                thumb_label="always"
            )
            
            solara.Markdown("### 📉 最小規模")
            solara.SliderFloat(
                label="", 
                value=min_magnitude, 
                min=4.0, 
                max=7.5, 
                step=0.1, 
                thumb_label="always"
            )
            
            solara.Markdown("---")
            solara.Markdown("### 🎨 深度圖例")
            solara.Markdown("* <span style='color:#FF3333'>■</span> **極淺層 (<20km)**：破壞力最強")
            solara.Markdown("* <span style='color:#FF8800'>■</span> **淺層 (20-50km)**")
            solara.Markdown("* <span style='color:#FFFF00'>■</span> **中層 (50-100km)**")
            solara.Markdown("* <span style='color:#00CC00'>■</span> **深層 (>100km)**")

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
                    key=f"tw-quake-v1-{year_range.value}-{min_magnitude.value}"
                )

Page()