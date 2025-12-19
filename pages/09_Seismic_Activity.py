import solara
import leafmap.foliumap as leafmap
import pandas as pd
import duckdb
import io  # <--- 新增這個工具：專門處理記憶體內的檔案流

# ==========================================
# 1. 資料準備：直接從 USGS 網址讀取 (不存檔)
# ==========================================
# 真實資料源：過去 30 天全球規模 2.5+ 地震
CSV_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv"

def get_real_earthquake_data():
    print(f"正在連線 USGS 下載真實地震資料: {CSV_URL} ...")
    try:
        # 讀取 CSV 到記憶體 DataFrame
        df = pd.read_csv(CSV_URL)
        
        # 資料清理
        df['time'] = pd.to_datetime(df['time'])
        df['year'] = df['time'].dt.year
        df = df.dropna(subset=['latitude', 'longitude', 'mag', 'depth'])
        
        print(f"成功下載！共 {len(df)} 筆地震資料。")
        return df
        
    except Exception as e:
        print(f"下載失敗: {e}")
        return pd.DataFrame(columns=['latitude', 'longitude', 'mag', 'depth', 'year', 'place'])

# App 啟動時下載一次
df_earthquakes = get_real_earthquake_data()

# ==========================================
# 2. DuckDB 查詢
# ==========================================
def query_earthquakes(min_mag, selected_year):
    # 如果資料下載失敗，回傳空表
    if df_earthquakes.empty:
        return df_earthquakes

    # SQL 篩選
    query = f"""
        SELECT latitude, longitude, mag, depth, place, year
        FROM df_earthquakes 
        WHERE mag >= {min_mag} 
        AND year = {selected_year}
    """
    return duckdb.query(query).to_df()

# ==========================================
# 3. 變數設定
# ==========================================
min_magnitude = solara.reactive(4.0) 

# 自動判斷資料年份 (通常是 2024 或 2025)
default_year = 2024
if not df_earthquakes.empty:
    default_year = int(df_earthquakes['year'].max())
current_year = solara.reactive(default_year) 

# ==========================================
# 4. 頁面元件
# ==========================================
@solara.component
def Page():
    
    def calculate_map_html():
        df = query_earthquakes(min_magnitude.value, current_year.value)
        count = len(df)
        
        m = leafmap.Map(
            center=[24.15, 121.4],
            zoom=6,
            google_map="HYBRID",
            draw_control=False,
            measure_control=False,
        )

        def get_color(depth):
            if depth < 15: return "red"
            elif depth < 70: return "orange"
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
                    popup=f"<b>{row['place']}</b><br>規模: {row['mag']}<br>深度: {row['depth']}km"
                ).add_to(m)

        # ★★★ 關鍵修復：使用 io.BytesIO 取代 m.to_html() ★★★
        # 這段程式碼會把地圖存進 RAM (fp) 而不是硬碟，避開 Permission Error
        fp = io.BytesIO()
        m.save(fp, close_file=False)
        fp.seek(0)
        
        # 讀取並轉成字串
        map_html_str = fp.read().decode('utf-8')
        
        return map_html_str, count

    # 執行運算
    map_html, count = solara.use_memo(
        calculate_map_html,
        dependencies=[min_magnitude.value, current_year.value]
    )
    
    # 計算年份範圍供滑桿使用
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
            solara.Markdown("直接串接 **USGS** 即時資料流，並解決雲端存取權限問題。")
            
            solara.Markdown("---")
            
            with solara.Card(margin=0, elevation=1, style={"background-color": "#424242", "color": "white"}):
                solara.Markdown("### 📡 系統狀態")
                solara.Markdown(f"資料來源：**USGS Live Feed**")
                solara.Markdown(f"篩選筆數：**{count}** 筆")
                solara.Markdown(f"儲存模式：**In-Memory (RAM)**")
                
            solara.Markdown("---")
            
            solara.SliderInt(label="年份", value=current_year, min=min_year, max=max_year, thumb_label="always")
            solara.SliderFloat(label="最小規模", value=min_magnitude, min=2.5, max=7.5, step=0.1, thumb_label="always")
            
            solara.Markdown("---")
            with solara.Details(summary="🛠️ 技術解密"):
                 solara.Markdown("""
                 **權限錯誤修復 (Permission Error Fix)**：
                 
                 原本的 `to_html()` 會嘗試寫入暫存檔導致失敗。
                 此版本改用 `io.BytesIO` 將地圖 HTML 直接寫入記憶體緩衝區，
                 成功繞過 Hugging Face 的唯讀檔案系統限制。
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
                    key=f"seismic-fix-v4-{current_year.value}-{min_magnitude.value}"
                )

Page()