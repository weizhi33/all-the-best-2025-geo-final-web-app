import solara
import leafmap.foliumap as leafmap
import io

@solara.component
def Page():
    
    def get_wujie_map():
        # 1. 計算中心點 (武界壩 與 日月潭 的中間)
        # 武界壩: 23.918, 121.048
        # 日月潭: 23.860, 120.940
        CENTER_LAT = (23.918 + 23.860) / 2
        CENTER_LON = (121.048 + 120.940) / 2
        
        m = leafmap.Map(
            center=[CENTER_LAT, CENTER_LON],
            zoom=13,
            draw_control=False,
            measure_control=False,
        )
        
        # 2. 設定 Google Hybrid 衛星底圖 (最適合看山脈與水域)
        m.add_tile_layer(
            url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            name="Google Hybrid",
            attribution="Google"
        )

        # 3. 繪製「引水隧道」示意線 (虛線代表地下)
        tunnel_coords = [
            [23.918, 121.048], # 起點：武界壩
            [23.860, 120.940]  # 終點：日月潭 (大竹湖進水口)
        ]
        
        leafmap.folium.PolyLine(
            locations=tunnel_coords,
            color="#00ffff", # 亮青色
            weight=5,
            opacity=0.8,
            dash_array='10, 10', # 虛線效果
            tooltip="新武界引水隧道 (地下段)"
        ).add_to(m)

        # 4. 加入起終點標記
        leafmap.folium.Marker(
            location=[23.918, 121.048],
            popup="<b>起點：武界壩</b><br>攔截濁水溪水源",
            icon=leafmap.folium.Icon(color="blue", icon="tint")
        ).add_to(m)

        leafmap.folium.Marker(
            location=[23.860, 120.940],
            popup="<b>終點：日月潭</b><br>大竹湖進水口 (日月湧泉)",
            icon=leafmap.folium.Icon(color="green", icon="flag")
        ).add_to(m)

        return m

    # 5. 記憶體輸出 (io.BytesIO) - 避開 HF 唯讀權限問題
    m = get_wujie_map()
    fp = io.BytesIO()
    m.save(fp, close_file=False)
    fp.seek(0)
    map_html_str = fp.read().decode('utf-8')

    solara.Title("武界引水工程")

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        # --- 標題區 ---
        with solara.Row(style={"padding": "20px", "background-color": "#f0f2f6", "align-items": "center"}):
             solara.HTML(tag="h2", unsafe_innerHTML="🌊 04. 穿山越嶺：看不見的地下河流", style="margin: 0;")
             solara.Success("💡 本頁展示濁水溪如何透過「越域引水」工程，穿過中央山脈注入日月潭。地圖上的虛線即為長達 16.5 公里的引水隧道。", icon="mdi-water-pump")

        # --- 內容區 ---
        with solara.Columns([1, 3], style={"height": "calc(100vh - 100px)"}):
            
            # 左側：文字介紹
            with solara.Column(style={"padding": "20px", "background-color": "white", "height": "100%", "overflow-y": "auto"}):
                
                solara.Markdown("### 🏞️ 濁水溪的「分身」")
                solara.Markdown("濁水溪的水並不是全部流向大海，有一大部分在這裡被「攔截」了。")
                
                solara.Markdown("---")
                
                with solara.Card("🏗️ 工程奇蹟：新舊傳承", margin=0, elevation=2):
                    solara.Markdown("""
                    **越域引水 (Transbasin Diversion)**
                    這條隧道直接穿過山脈，將濁水溪的水送往**日月潭**。這也是為什麼日月潭雖然沒有大河注入，水位卻能終年保持穩定的秘密。
                    
                    **歷史軌跡**：
                    * **1934 年 (日治時期)**：日本人興建了第一條「舊武界引水隧道」，奠定了台灣水力發電的基礎。
                    * **2006 年 (現代)**：因舊隧道老化，台電耗資 90 億興建了「新武界引水隧道」（地圖虛線處），總長 16.5 公里，是當時台灣最長的引水隧道。
                    """)
                
                solara.Markdown("---")
                solara.Markdown("#### 📍 地圖圖例")
                with solara.Column(gap="5px"):
                    solara.Text("🟦 虛線：新武界引水隧道 (地下)")
                    solara.Text("📍 藍標：武界壩 (攔河堰)")
                    solara.Text("📍 綠標：日月潭 (大竹湖出水口)")

            # 右側：地圖 (iframe)
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
                    key="wujie-tunnel-map"
                )

Page()