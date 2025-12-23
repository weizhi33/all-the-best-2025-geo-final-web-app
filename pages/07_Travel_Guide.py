import solara
import leafmap.foliumap as leafmap
import io

# ==========================================
# 1. 定義關鍵地點資料
# ==========================================
POINTS = [
    {
        "name": "⛽ 清境加油站 (最後補給)", 
        "coords": [24.045, 121.162], 
        "desc": "上山前最後一個大型加油站，建議在此加滿。",
        "icon": "tint", 
        "color": "blue"
    },
    {
        "name": "🏪 全家富嘉門市 (最高超商)", 
        "coords": [24.050, 121.168], 
        "desc": "海拔2050m，補充熱食、暖暖包的最後據點。",
        "icon": "shopping-cart",
        "color": "green"
    },
    {
        "name": "❄️ 翠峰管制站 (雪季檢查)", 
        "coords": [24.110, 121.220], 
        "desc": "雪季期間(1-3月)的車輛檢查點。若武嶺積雪，無雪鏈車輛禁止通行，且常實施夜間預警性封閉。",
        "icon": "ban-circle", # 禁止/檢查圖示
        "color": "black"
    },
    {
        "name": "🚑 合歡山管理站 (雪季醫療)", 
        "coords": [24.145, 121.291], 
        "desc": "位於小風口，雪季期間常駐有醫療團隊。",
        "icon": "plus-sign",
        "color": "red"
    },
    {
        "name": "⛽ 關原加油站 (肉粽聖地)", 
        "coords": [24.182, 121.343], 
        "desc": "全台最高加油站(2374m)。必吃雲端肉粽！(營業時間 09:00-18:00)",
        "icon": "cutlery", 
        "color": "purple"
    },
    {
        "name": "🚧 關原災害段 (管制熱點)", 
        "coords": [24.175, 121.355], 
        "desc": "台8線117k附近，大規模坍方修復中，採時段性放行。",
        "icon": "warning-sign",
        "color": "orange"
    },
    {
        "name": "🚩 太魯閣牌樓 (終點)", 
        "coords": [24.156, 121.622], 
        "desc": "東西橫貫公路入口，旅程的終點。",
        "icon": "flag",
        "color": "cadetblue"
    }
]

@solara.component
def Page():
    
    def get_guide_map():
        # 定位在整條路線的中心
        CENTER = [24.13, 121.30]
        
        m = leafmap.Map(
            center=CENTER,
            zoom=10,
            draw_control=False,
            measure_control=False,
        )
        
        # 使用 OpenStreetMap 街道圖，看路名比較清楚
        m.add_basemap("OpenStreetMap")
        
        # 加入所有標記
        for p in POINTS:
            # 建立 Popup 內容
            popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
            
            m.add_marker(
                location=p["coords"],
                popup=popup_html,
                tooltip=p["name"],
                icon=leafmap.folium.Icon(color=p["color"], icon=p["icon"])
            )
            
        return m

    # 記憶體輸出 (io.BytesIO) - 穩定不報錯
    m = get_guide_map()
    fp = io.BytesIO()
    m.save(fp, close_file=False)
    fp.seek(0)
    map_html_str = fp.read().decode('utf-8')

    solara.Title("行前攻略")

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        # --- 標題區 ---
        with solara.Row(style={"padding": "20px", "background-color": "#fffbf0", "align-items": "center"}):
             solara.HTML(tag="h2", unsafe_innerHTML="🎒 07. 行前攻略：補給與路況", style="margin: 0;")
             solara.Success("💡 出發前請務必檢查：油量（山區僅2站）、輪胎與煞車、保暖衣物，並確認當日交通管制資訊。", icon="mdi-car-convertible")

        # --- 內容區 ---
        with solara.Columns([1, 3], style={"height": "calc(100vh - 100px)"}):
            
            # 左側：實用資訊
            with solara.Column(style={"padding": "20px", "background-color": "white", "height": "100%", "overflow-y": "auto"}):
                
                # 1. 交通管制 (最重要的放上面)
                with solara.Card("🚧 交通管制", margin=0, elevation=2):
                    solara.Markdown("""
                    **關原災害路段 (117k)**：
                    * 受地震與坍方影響，該路段通常實施**每日定時放行**（例如：07:00~08:00, 12:00~13:00, 17:00 等）。
                    * **注意**：非放行時段人車無法通過，請務必至 [公路總局智慧化省道即時資訊網](https://168.thb.gov.tw/) 查詢最新公告。
                    """)
                
                solara.Markdown("<br>")

                # 2. 雪季管制
                with solara.Card("❄️ 冬季/雪季管制 (Snow Season)", margin=0, elevation=2):
                    solara.Markdown("""
                    **時間**：通常為每年 1月 ~ 3月 (合歡山雪季)。
                    **管制路段**：台14甲線 翠峰(18k) 至 大禹嶺(41k)。
                    **管制措施**：
                    * **雪鏈**：路面結冰時，限加掛雪鏈車輛通行 (四輪驅動車輛建議也備妥)。
                    * **預警性封閉**：若氣象預報夜間降雪或結冰，將於 **17:00 至 隔日 07:00** 全線封閉，禁止過夜。
                    """)

                solara.Markdown("---")
                
                # 3. 補給資訊
                with solara.Card("⛽ 補給站點", margin=0, elevation=1):
                    solara.Markdown("""
                    **1. 關原加油站 (2374m)**
                    * **營業時間**：09:00 - 18:00 (請注意晚上沒開！)
                    * **必吃**：雲端肉粽。
                    
                    **2. 商店**
                    * **全家富嘉門市**：位於清境最高點，最後的熱食補給站。過了這裡直到太魯閣天祥前都沒有超商。
                    """)
                
                solara.Markdown("---")
                solara.Info("🚑 高山症提醒：武嶺海拔 3275m，若出現頭痛、噁心症狀，請立即降低高度 (往清境或天祥方向下山)。")

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
                    key="guide-map-folium"
                )

Page()