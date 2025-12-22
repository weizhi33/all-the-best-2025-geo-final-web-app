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
    
    # 抓取 2000 年至今，台灣東部與花蓮外海的地震
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
        # 回傳空 DataFrame 避免報錯
        return pd.DataFrame(columns=['latitude', 'longitude', 'mag', 'depth', 'year', 'place'])

# 下載資料 (全域變數，只下載一次)
df_earthquakes = get_taiwan_earthquake_data()

# ==========================================
# 2. DuckDB 查詢引擎
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
# 3. 響應式變數
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
        
        # 建立地圖：中心鎖定立霧溪口
        m = leafmap.Map(
            center=[24.14, 121.6], 
            zoom=9,                
            google_map="HYBRID",
            draw_control=False,
            measure_control=False,
        )

        # ★★★ 顏色分層優化：強調隱沒帶深度結構 ★★★
        def get_color(depth):
            if depth < 20: return "#FF0000"      # 極淺層 (紅) - 破壞力最強
            elif depth < 60: return "#FF8800"    # 淺層 (橘)
            elif depth < 150: return "#FFFF00"   # 中層 (黃)
            else: return "#0000FF"               # 深層 (藍) - 隱沒帶深處

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
        
        # 標記：立霧溪出海口 (參考點)
        leafmap.folium.Marker(
            location=[24.138, 121.655],
            popup="立霧溪出海口",
            tooltip="中橫公路終點",
            icon=leafmap.folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

        # 記憶體輸出 (io.BytesIO) - 穩定不報錯
        fp = io.BytesIO()
        m.save(fp, close_file=False)
        fp.seek(0)
        map_html_str = fp.read().decode('utf-8')
        
        return map_html_str, count

    # 使用 use_memo 優化效能
    map_html, count = solara.use_memo(
        calculate_map_html,
        dependencies=[min_magnitude.value, year_range.value]
    )

    solara.Title("台灣東部地震分布")

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        # --- 標題區 ---
        with solara.Row(style={"padding": "20px", "background-color": "#2c3e50", "align-items": "center"}):
             solara.HTML(tag="h2", unsafe_innerHTML="🌋 09. 震災大數據：板塊運動見證", style="color: white; margin: 0;")
             solara.Success("💡 本頁串接 USGS 即時地震資料庫，將過去 25 年台灣東部的地震活動視覺化。請觀察不同深度的地震顏色分布，見證板塊隱沒的軌跡。", icon="mdi-pulse")

        # --- 內容區 ---
        with solara.Columns([1, 3], style={"height": "calc(100vh - 100px)"}):
            
            # 左側：控制面板
            with solara.Column(style={"padding": "20px", "background-color": "#34495e", "color": "#ecf0f1", "height": "100%", "overflow-y": "auto"}):
                
                # 統計數據
                with solara.Card(margin=0, elevation=2, style={"background-color": "#2c3e50", "color": "white"}):
                    solara.Markdown("### 📊 區域統計")
                    solara.Markdown(f"**年份**：{year_range.value[0]} - {year_range.value[1]}")
                    solara.Markdown(f"**地震總數**：{count} 筆")
                
                solara.Markdown("---")
                
                # 滑桿控制
                solara.Markdown("### 📅 時間軸篩選")
                solara.SliderRangeInt(label="", value=year_range, min=min_y, max=max_y, thumb_label="always")
                
                solara.Markdown("### 📉 最小規模 (Magnitude)")
                solara.SliderFloat(label="", value=min_magnitude, min=4.0, max=7.5, step=0.1, thumb_label="always")
                
                solara.Markdown("---")
                
                # 圖例說明
                with solara.Card("🎨 深度構造 (Depth)", margin=0, elevation=1, style={"background-color": "#2c3e50", "color": "white"}):
                    solara.Markdown("* <span style='color:#FF0000'>■</span> **極淺層 (<20km)**：破壞力最大，如 0403 花蓮地震。")
                    solara.Markdown("* <span style='color:#FF8800'>■</span> **淺層 (20-60km)**")
                    solara.Markdown("* <span style='color:#FFFF00'>■</span> **中層 (60-150km)**")
                    solara.Markdown("* <span style='color:#0000FF'>■</span> **深層 (>150km)**：隱沒帶深處。")
                
                solara.Info("💡 觀察技巧：試著比較海域（右側）與陸地（左側）的顏色差異。您會發現海邊多為紅色淺層震，往內陸走則逐漸出現黃色與藍色深層震，這就是菲立普海板塊向西隱沒到歐亞大陸板塊底下的證據！")

            # 右側：地圖
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
                    key=f"tw-quake-map-{year_range.value}-{min_magnitude.value}"
                )

Page()