import solara
import leafmap.foliumap as leafmap
import io

@solara.component
def Page():
    
    def get_wushe_map():
        # 1. 定義地圖中心 (霧社水庫)
        WUSHE_CENTER = [24.018, 121.148]
        
        m = leafmap.Map(
            center=WUSHE_CENTER, 
            zoom=14,
            draw_control=False,
            measure_control=False,
        )
        
        # 2. 定義圖磚網址 (直接用 URL 最穩，不再依賴關鍵字)
        # Google Satellite (衛星) - 用於看淤積水色
        url_sat = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        
        # Google Terrain (地形) - 用於看等高線與暈渲
        url_ter = "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}"
        
        # 3. 建立捲簾 (Split Map)
        # 這裡直接傳入網址字串
        m.split_map(
            left_layer=url_sat, 
            right_layer=url_ter,
            left_label="衛星：淤積水色",
            right_label="地形：河谷等高線"
        )
        
        # 加入圖例 (選擇性)
        m.add_legend(title="捲簾對照：衛星 vs 地形", position="bottomright")

        return m

    # 4. 記憶體輸出 HTML (最穩定的寫法)
    m = get_wushe_map()
    fp = io.BytesIO()
    m.save(fp, close_file=False)
    fp.seek(0)
    map_html_str = fp.read().decode('utf-8')

    solara.Title("霧社水庫：淤積觀測")

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        # --- 標題區 ---
        with solara.Row(style={"padding": "20px", "background-color": "#f0f2f6", "align-items": "center"}):
             solara.HTML(tag="h2", unsafe_innerHTML="🛑 03. 霧社水庫的哀愁", style="margin: 0;")
             solara.Success("💡 操作說明：請拖曳中間的捲簾，觀察左側「混濁水色」與右側「陡峭地形」的關係。", icon="mdi-arrow-split-vertical")

        # --- 內容區 ---
        with solara.Columns([1, 3], style={"height": "calc(100vh - 100px)"}):
            
            # 左側：地理分析
            with solara.Column(style={"padding": "20px", "background-color": "white", "height": "100%", "overflow-y": "auto"}):
                
                solara.Markdown("### 碧湖之下隱藏的危機")
                solara.Markdown("台14甲線起點旁的碧湖（霧社水庫），美景之下隱藏著嚴重的淤積危機。")
                
                solara.Markdown("---")
                
                with solara.Card("🔍 觀察重點", margin=0, elevation=1):
                    solara.Markdown("""
                    **1. 水色差異 (左圖：衛星)**
                    * 請拖曳捲簾，觀察靠近上游（地圖上方/萬大溪匯入處）的水色呈現**混濁的土黃色**。
                    * 這顯示了上游集水區帶來的巨量泥沙，是水庫壽命的殺手。
                    
                    **2. 縱谷地形 (右圖：地形)**
                    * 切換到右側地形圖，觀察密集的**等高線**。
                    * 霧社水庫位於狹窄的 V 型谷中，兩岸坡度極陡，這雖然利於蓄水，但也代表集水區地質脆弱，容易發生崩塌與淤積。
                    """)
                
                solara.Markdown("---")
                solara.Info("💡 地圖圖層說明：右側使用了 Google Terrain 地形圖層，帶有立體暈渲 (Hillshade) 效果，能清楚呈現山谷的立體感。")

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
                    key="wushe-split-map-v2"
                )

Page()