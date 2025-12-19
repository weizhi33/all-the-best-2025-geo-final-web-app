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
    today = datetime.date.today()
    end_date = today.strftime("%Y-%m-%d")
    
    # 抓取 2000 年至今，台灣周邊 (包含花蓮外海) 的地震
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
        
        df['time'] = pd.to_datetime(df['time'])
        df['year'] = df['time'].dt.year
        df = df.dropna(subset=['latitude', 'longitude', 'mag', 'depth'])
        
        print(f"下載成功！取得 {len(df)} 筆台灣真實地震資料。")
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
current_year = 2025
if not df_earthquakes.empty:
    max_y = int(df_earthquakes['year'].max())
    min_y = int(df_earthquakes['year'].min())
    year_range = solara.reactive([max_y - 5, max_y]) # 預設看最近5年
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
        
        # ★★★ 關鍵修改：聚焦立霧溪出海口/中橫東段 ★★★
        m = leafmap.Map(
            center=[24.14, 121.6], # 立霧溪口附近 (新城/崇德)
            zoom=9,                # 拉近到可以看到花蓮縣與周邊海域
            google_map="HYBRID",
            draw_control=False,
            measure_control=False,
        )

        # 顏色分層：強調隱沒帶結構
        def get_color(depth):
            if depth < 20: return "#FF3333"      # 極淺層 (紅) - 破壞力大
            elif depth < 50: return "#FF8800"    # 淺層 (橘)
            elif depth < 100: return "#FFFF00"   # 中層 (黃)
            else: return "#00CC00"               # 深層 (綠) - 隱沒帶深處

        if not df.empty:
            radius_scale = 1.0 if count < 1000 else 0.8
            
            for _, row in df.iterrows():
                leafmap.folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=(row['mag'] ** 2) * 0.15 * radius_scale, 
                    color=None,
                    fill=True,
                    fill_color=get_color(row['depth']),
                    fill_opacity=0.6,
                    popup=f"<b>{row['place']}</b><br>年份: {row['year']}<br>規模: {row['mag']}<br>深度: {row['depth']}km"
                ).add_to(m)
        
        # 加上一個標記，標示立霧溪口位置，作為參考點
        leafmap.folium.Marker(
            location=[24.138, 121.655],
            popup="立霧溪出海口",
            icon=leafmap.folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

        # 記憶體輸出 HTML
        fp = io.BytesIO()
        m.save(fp, close_file=False)
        fp.seek(0)
        map_html_str = fp.read().decode('utf-8')
        
        return map_html_str, count

    map_html, count = solara.use_memo(
        calculate_map_html,
        dependencies=[min_magnitude.value, year_range.value]
    )

    solara.Title("中橫震災史：USGS 大數據")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#222", "color": "#eee", "height": "100%"}):
            solara.Markdown("## 🇹🇼 中橫震災大數據")
            solara.Markdown("聚焦 **立霧溪出海口** 與 **中橫公路** 周邊，觀察板塊交界處的劇烈活動。")
            
            solara.Markdown("---")
            
            with solara.Card(margin=0, elevation=1, style={"background-color": "#333", "color": "white"}):
                solara.Markdown("### 📊 區域統計")
                solara.Markdown(f"時間：**{year_range.value[0]} - {year_range.value[1]}**")
                solara.Markdown(f"地震數：**{count}** 筆")
                
            solara.Markdown("---")
            
            solara.Markdown("### 📅 年份範圍")
            solara.SliderRangeInt(label="", value=year_range, min=min_y, max=max_y, thumb_label="always")
            
            solara.Markdown("### 📉 最小規模")
            solara.SliderFloat(label="", value=min_magnitude, min=4.0, max=7.5, step=0.1, thumb_label="always")
            
            solara.Markdown("---")
            solara.Markdown("### 🎨 深度構造")
            solara.Markdown("* <span style='color:#FF3333'>■</span> **極淺層 (<20km)**")
            solara.Markdown("* <span style='color:#FF8800'>■</span> **淺層 (20-50km)**")
            solara.Markdown("* <span style='color:#FFFF00'>■</span> **中層 (50-100km)**")
            solara.Markdown("* <span style='color:#00CC00'>■</span> **深層 (>100km)**")
            solara.Info("💡 觀察重點：注意看立霧溪口外海（右側）到內陸（左側），地震深度是否由淺變深？這就是菲律賓海板塊向西隱沒的證據！")

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
                    key=f"tw-focus-v2-{year_range.value}-{min_magnitude.value}"
                )

Page()