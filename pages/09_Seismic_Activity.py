import solara
import leafmap.foliumap as leafmap
import pandas as pd
import duckdb

# ==========================================
# 1. 資料準備：直接從 USGS 網址讀取 (不存檔)
# ==========================================
# 這是您指定的 USGS 真實資料源
CSV_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv"

def get_real_earthquake_data():
    print(f"正在連線 USGS 下載真實地震資料: {CSV_URL} ...")
    try:
        # 直接從 URL 讀取 CSV 到記憶體，不存入硬碟，避免 Read-only 錯誤
        df = pd.read_csv(CSV_URL)
        
        # --- 資料清理與整理 ---
        # 1. USGS 的時間格式是字串，轉成 datetime 物件以便抓出年份
        df['time'] = pd.to_datetime(df['time'])
        df['year'] = df['time'].dt.year
        
        # 2. 處理空值 (有些地震可能沒有深度或規模)
        df = df.dropna(subset=['latitude', 'longitude', 'mag', 'depth'])
        
        print(f"成功下載！共 {len(df)} 筆全球地震資料。")
        return df
        
    except Exception as e:
        print(f"下載失敗，請檢查網路連線。錯誤訊息: {e}")
        # 萬一 USGS 網站掛了，回傳一個空的 DataFrame 避免程式崩潰
        return pd.DataFrame(columns=['latitude', 'longitude', 'mag', 'depth', 'year', 'place'])

# 全域變數：App 啟動時下載一次
df_earthquakes = get_real_earthquake_data()

# ==========================================
# 2. DuckDB 查詢 (針對真實欄位名稱調整)
# ==========================================
def query_earthquakes(min_mag, selected_year):
    # USGS 的欄位名稱是 'mag' (規模) 和 'depth' (深度)
    # 我們在這裡用 SQL 進行篩選
    # 為了避免資料太多，我們也可以限制範圍在台灣附近 (緯度 21-26, 經度 119-123)
    
    query = f"""
        SELECT latitude, longitude, mag, depth, place, year
        FROM df_earthquakes 
        WHERE mag >= {min_mag} 
        AND year = {selected_year}
        -- 下面這行可以打開，如果只想看台灣附近的地震
        -- AND latitude BETWEEN 20 AND 27 AND longitude BETWEEN 118 AND 124
    """
    
    # 如果資料是空的(下載失敗)，回傳空表
    if df_earthquakes.empty:
        return df_earthquakes
        
    return duckdb.query(query).to_df()

# ==========================================
# 3. 變數
# ==========================================
min_magnitude = solara.reactive(4.0) 
# 因為 USGS 這個網址只給「最近 30 天」的資料，所以年份通常只有今年(2025)或去年(2024)
# 我們自動抓資料裡有的年份
default_year = 2024
if not df_earthquakes.empty:
    default_year = int(df_earthquakes['year'].max())

current_year = solara.reactive(default_year) 

# ==========================================
# 4. 頁面
# ==========================================
@solara.component
def Page():
    
    def calculate_map_html():
        df = query_earthquakes(min_magnitude.value, current_year.value)
        count = len(df)
        
        m = leafmap.Map(
            center=[24.15, 121.4],
            zoom=6, # 拉遠一點看大範圍
            google_map="HYBRID",
            draw_control=False,
            measure_control=False,
        )

        def get_color(depth):
            if depth < 15: return "red"
            elif depth < 70: return "orange" # USGS 對淺層/深層的定義稍微不同
            else: return "blue"

        if not df.empty:
            for _, row in df.iterrows():
                leafmap.folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=row['mag'] * 1.5,
                    color=get_color(row['depth']),
                    fill=True,
                    fill_color=get_color(row['depth']),
                    fill_opacity=0.6,
                    popup=f"<b>{row['place']}</b><br>規模(Mag): {row['mag']}<br>深度: {row['depth']}km<br>時間: {row['year']}"
                ).add_to(m)

        return m.to_html(), count

    map_html, count = solara.use_memo(
        calculate_map_html,
        dependencies=[min_magnitude.value, current_year.value]
    )
    
    # 取得資料庫裡有的年份範圍，用來設定滑桿
    years = [2024, 2025]
    if not df_earthquakes.empty:
        years = sorted(df_earthquakes['year'].unique().tolist())
    min_year = min(years) if years else 2024
    max_year = max(years) if years else 2025

    solara.Title("大地的心跳：USGS 真實數據")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#2b2b2b", "color": "#e0e0e0", "height": "100%"}):
            solara.Markdown("## 💓 大地的心跳 (Real-Time)")
            solara.Markdown("直接串接 **USGS (美國地質調查局)** 即時資料流。")
            
            solara.Markdown("---")
            
            with solara.Card(margin=0, elevation=1, style={"background-color": "#424242", "color": "white"}):
                solara.Markdown("### 📡 數據來源狀態")
                solara.Markdown(f"來源：**USGS Feed (2.5+ Month)**")
                solara.Markdown(f"資料年份：**{min_year} - {max_year}**")
                solara.Markdown(f"篩選後筆數：**{count}** 筆")
                
            solara.Markdown("---")
            
            # 如果資料只有一年，滑桿會有點怪，但還是可以用
            solara.SliderInt(label="年份", value=current_year, min=min_year, max=max_year, thumb_label="always")
            solara.SliderFloat(label="最小規模", value=min_magnitude, min=2.5, max=7.5, step=0.1, thumb_label="always")
            
            solara.Markdown("---")
            with solara.Details(summary="ℹ️ 資料說明"):
                 solara.Markdown("""
                 **真實資料來源**：
                 `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv`
                 
                 此頁面展示最近 30 天內，全球規模 2.5 以上的真實地震紀錄。
                 資料由 Python 直接載入記憶體進行 DuckDB 運算，確保資料即時性。
                 """)

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
                    key=f"seismic-real-v1-{current_year.value}-{min_magnitude.value}"
                )

Page()