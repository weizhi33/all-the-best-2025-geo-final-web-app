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
        
        # 2. 定義圖磚網址 (Direct URL)
        # Google Satellite (衛星)
        url_sat = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        # Google Terrain (地形)
        url_ter = "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}"
        
        # 3. 建立捲簾
        m.split_map(
            left_layer=url_sat, 
            right_layer=url_ter,
            left_label="衛星：淤積水色",
            right_label="地形：河谷等高線"
        )
        
        m.add_legend(title="捲簾對照：衛星 vs 地形", position="bottomright")
        return m

    # 4. 記憶體輸出
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
                
                # ★★★ 新增：水庫小檔案 ★★★
                with solara.Card("💧 關於霧社水庫", margin=0, elevation=2):
                    solara.Markdown("""
                    **別名**：碧湖
                    **完工年份**：1957 年
                    **功能**：攔截濁水溪上游水源，調節水量傳送至日月潭發電。
                    
                    因群山環繞、水色青碧，蔣介石曾以此命名為「碧湖」。它是台灣高山水庫的先驅，卻也因地質年輕，長年飽受淤積之苦。
                    """)
                
                solara.Markdown("---")
                
                # 原有的觀察重點
                with solara.Card("🔍 衛星觀察重點", margin=0, elevation=1):
                    solara.Markdown("""
                    **1. 混濁的水色 (左圖)**
                    * 請注意地圖上方（萬大溪匯入處），水面呈現**土黃色**。
                    * 這不是污染，而是上游崩塌帶來的巨量懸浮泥沙，顯示水庫正面臨淤積危機。
                    
                    **2. 險峻的 V 型谷 (右圖)**
                    * 切換到右側地形圖，可見兩岸等高線極度密集。
                    * 這種高山峽谷地形雖然能蓄水，但也代表集水區坡度極陡，只要大雨一來，土石便直衝水庫。
                    """)
                
                solara.Markdown("---")
                solara.Info("💡 下一頁 (Page 04)，我們將追蹤這些水是如何穿過山脈，透過「武界引水隧道」送往日月潭的。")

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
                    key="wushe-split-map-final"
                )

Page()