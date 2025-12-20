import solara
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt
import io

# ==========================================
# 1. 數據準備：中橫公路關鍵節點與海拔
# ==========================================
# 這是為了繪製剖面圖與地圖路線用的數據
route_data = [
    {"name": "埔里", "lat": 23.9700, "lon": 120.9700, "elev": 450, "dist": 0},
    {"name": "霧社", "lat": 24.0237, "lon": 121.1275, "elev": 1148, "dist": 22},
    {"name": "清境", "lat": 24.0560, "lon": 121.1620, "elev": 1750, "dist": 29},
    {"name": "鳶峰", "lat": 24.1100, "lon": 121.2200, "elev": 2750, "dist": 45},
    {"name": "武嶺", "lat": 24.1370, "lon": 121.2760, "elev": 3275, "dist": 53}, # 最高點
    {"name": "大禹嶺", "lat": 24.1812, "lon": 121.3120, "elev": 2565, "dist": 60},
    {"name": "碧綠神木", "lat": 24.1812, "lon": 121.4055, "elev": 2150, "dist": 75},
    {"name": "天祥", "lat": 24.1820, "lon": 121.4945, "elev": 480, "dist": 95},
    {"name": "太魯閣", "lat": 24.1565, "lon": 121.6225, "elev": 60, "dist": 114},
]

df_route = pd.DataFrame(route_data)

# ==========================================
# 2. 繪製高度剖面圖 (Matplotlib)
# ==========================================
def get_elevation_chart():
    # 設定圖表大小與風格
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#ffffff') # 背景色
    
    # 繪製區域圖 (Area Chart) 來展現山體的厚重感
    ax.fill_between(df_route['dist'], df_route['elev'], color='#2E8B57', alpha=0.6) # 森林綠
    ax.plot(df_route['dist'], df_route['elev'], color='#006400', linewidth=2) # 稜線
    
    # 標示關鍵點
    for _, row in df_route.iterrows():
        # 只標示幾個重點，避免太擠
        if row['name'] in ["埔里", "武嶺", "太魯閣"]:
            ax.annotate(f"{row['name']}\n{row['elev']}m", 
                        (row['dist'], row['elev']),
                        textcoords="offset points", 
                        xytext=(0, 10), 
                        ha='center',
                        fontsize=9,
                        fontweight='bold')
            ax.scatter(row['dist'], row['elev'], color='red', zorder=5)

    # 設定標題與軸標籤
    ax.set_title("中橫公路垂直剖面圖 (Vertical Profile)", fontsize=12, fontweight='bold')
    ax.set_xlabel("距離 (km)", fontsize=10)
    ax.set_ylabel("海拔高度 (m)", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_ylim(0, 3600) # 讓山頂不要頂到天花板
    
    plt.tight_layout()
    
    # 轉成 HTML 圖片字串 (避免寫檔權限問題)
    s = io.BytesIO()
    plt.savefig(s, format='png', dpi=100)
    plt.close()
    s.seek(0)
    import base64
    return f'<img src="data:image/png;base64,{base64.b64encode(s.read()).decode()}" style="width: 100%;">'

# 預先生成圖表
chart_html = get_elevation_chart()

# ==========================================
# 3. 頁面元件
# ==========================================
@solara.component
def Page():
    
    def get_map():
        # 1. 使用 Google Terrain 地形底圖 (展現立體感)
        m = leafmap.Map(
            center=[24.05, 121.35],
            zoom=10,
            google_map="TERRAIN", # 關鍵：地形模式
            draw_control=False,
            measure_control=False,
        )
        
        # 2. 繪製路線 (LineString)
        points = [(row['lat'], row['lon']) for _, row in df_route.iterrows()]
        leafmap.folium.PolyLine(
            locations=points,
            color="red",
            weight=4,
            opacity=0.8,
            tooltip="中橫公路示意路線"
        ).add_to(m)

        # 3. 標示起點、最高點、終點
        for _, row in df_route.iterrows():
            if row['name'] == "武嶺":
                icon_name = "star"
                color = "orange"
            elif row['name'] in ["埔里", "太魯閣"]:
                icon_name = "flag"
                color = "blue"
            else:
                continue # 其他點不標，保持地圖乾淨

            leafmap.folium.Marker(
                location=[row['lat'], row['lon']],
                popup=f"<b>{row['name']}</b><br>海拔: {row['elev']}m",
                icon=leafmap.folium.Icon(color=color, icon=icon_name)
            ).add_to(m)
            
        return m

    # 處理地圖輸出 (記憶體大法)
    m = get_map()
    fp = io.BytesIO()
    m.save(fp, close_file=False)
    fp.seek(0)
    map_html_str = fp.read().decode('utf-8')

    solara.Title("中橫地形探索")

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        # --- 標題區 ---
        with solara.Row(style={"padding": "20px", "background-color": "#f0f2f5", "align-items": "center"}):
             solara.HTML(tag="h2", unsafe_innerHTML="⛰️ 02. 地形探索：穿越中央山脈", style="margin: 0;")
             solara.Success("💡 本頁面使用地形圖層 (Terrain Layer) 搭配垂直剖面分析，展示中橫公路如何從平地拔起，跨越海拔 3,275 公尺的武嶺。", icon="mdi-terrain")

        # --- 內容區 (左圖表、右地圖) ---
        with solara.Columns([1, 2], style={"height": "calc(100vh - 100px)"}):
            
            # 左側：剖面圖與地理資訊
            with solara.Column(style={"padding": "20px", "background-color": "white", "height": "100%", "overflow-y": "auto"}):
                
                solara.Markdown("### 📈 垂直剖面 (Elevation Profile)")
                solara.HTML(tag="div", unsafe_innerHTML=chart_html)
                
                solara.Markdown("---")
                
                with solara.Card("地理數據分析", margin=0, elevation=0):
                    solara.Markdown("""
                    **地形特徵：**
                    * **劇烈爬升**：從埔里 (450m) 到武嶺 (3275m)，短短 53 公里內爬升了近 3000 公尺。
                    * **分水嶺**：武嶺不僅是公路最高點，也是 **濁水溪** (西流) 與 **立霧溪** (東流) 的分水嶺。
                    * **地形不對稱**：
                        * *西側 (左半部)*：坡度較緩，多為高山草原 (合歡山)。
                        * *東側 (右半部)*：坡度極陡，立霧溪向源侵蝕強烈，形成壯觀的峽谷地形 (太魯閣)。
                    """)
                    
                solara.Markdown("---")
                solara.Info("👆 提示：對照上方的剖面圖與右側的地圖，您可以發現東側（太魯閣端）的等高線明顯比西側（埔里端）密集，這就是「差異侵蝕」的證據。", icon="mdi-magnify")

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
                    key="terrain-map"
                )

Page()