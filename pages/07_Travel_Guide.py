import solara
import leafmap.leafmap as leafmap
import ipywidgets as widgets
from ipyleaflet import AwesomeIcon

def create_guide_map():
    # 定位在整條路線的中心
    CENTER = [24.16, 121.32]
    
    # 建立 2D 地圖
    m = leafmap.Map(
        center=CENTER,
        zoom=10,
        height="700px"
    )
    
    # 1. 加入 OSM 街道圖
    m.add_basemap("OpenStreetMap")
    
    # 2. 定義關鍵地點
    points = [
        {
            "name": "⛽ 清境加油站 (最後補給)", 
            "coords": [24.045, 121.162], 
            "desc": "上山前最後一個大型加油站，建議在此加滿。",
            "icon": "tachometer", 
            "color": "red"
        },
        {
            "name": "🏪 全家富嘉門市 (最高超商)", 
            "coords": [24.050, 121.168], 
            "desc": "海拔2050m，補充熱食、暖暖包的最後據點。",
            "icon": "shopping-cart",
            "color": "orange"
        },
        {
            "name": "🚑 合歡山管理站 (雪季醫療)", 
            "coords": [24.145, 121.291], 
            "desc": "位於小風口，雪季期間常駐有醫療團隊。",
            "icon": "ambulance",
            "color": "green"
        },
        {
            "name": "⛽ 關原加油站 (肉粽聖地)", 
            "coords": [24.182, 121.343], 
            "desc": "全台最高加油站(2374m)。必吃雲端肉粽！(09:00-18:00)",
            "icon": "cutlery", 
            "color": "red"
        },
        {
            "name": "🚧 關原災害段 (管制熱點)", 
            "coords": [24.175, 121.355], 
            "desc": "台8線117k附近，大規模坍方修復中，常有整點放行管制。",
            "icon": "exclamation-triangle",
            "color": "black"
        },
        {
            "name": "🚩 太魯閣牌樓 (終點)", 
            "coords": [24.156, 121.622], 
            "desc": "東西橫貫公路入口，旅程的終點。",
            "icon": "flag",
            "color": "blue"
        }
    ]
    
    # 3. 迴圈加入標記
    for p in points:
        # [修正 1] 建立 HTML Widget (解決 TraitError)
        popup_widget = widgets.HTML(
            value=f"<b>{p['name']}</b><br>{p['desc']}"
        )
        
        # [修正 1] 建立 Icon 物件
        icon_obj = AwesomeIcon(
            name=p["icon"], 
            marker_color=p["color"], 
            icon_color='white'
        )
        
        m.add_marker(
            location=p["coords"],
            draggable=False,
            popup=popup_widget,
            icon=icon_obj,
            title=p["name"]
        )
        
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_guide_map, dependencies=[])

    solara.Title("行前攻略")

    with solara.Columns([1, 3]):
        
        # --- 左側：實用建議 ---
        with solara.Column(style={"padding": "20px", "background-color": "#fffbf0", "height": "100%"}):
            solara.Markdown("## 🎒 中橫行前攻略")
            solara.Markdown("出發前請務必檢查：油量、煞車、輪胎、保暖衣物。")
            
            solara.Markdown("---")
            
            with solara.Card("⛽ 加油站注意！", margin=0, elevation=1):
                solara.Markdown("""
                山區僅有兩處加油站，錯過就麻煩了：
                
                1.  **清境加油站**：上山前最後堡壘。
                2.  **關原加油站** (全台最高)：
                    * **營業時間**：09:00 - 18:00 (晚上沒開！)
                    * **名產**：燒肉粽 (很多人專程騎車上去吃)。
                """)
            
            solara.Markdown("---")
            
            with solara.Card("🤢 高山症預防", margin=0, elevation=1):
                solara.Markdown("""
                武嶺海拔 3275m，氣壓僅平地的 70%。
                * **症狀**：頭痛、噁心、想吐。
                * **對策**：動作放慢、不要在山上劇烈跑跳。若不舒服請**立刻下山**，高度下降是唯一解藥。
                """)
                
            solara.Markdown("---")
            
            with solara.Card("🚧 路況查詢", margin=0, elevation=1):
                solara.Markdown("""
                台8線（關原-太魯閣）受地震影響，常有施工管制（例如整點放行 10 分鐘）。
                建議出發前查詢 **公路總局省道即時路況**。
                """)

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                # [修正 2] 關鍵！使用 solara.Column 包覆地圖 widget，解決跑版問題
                # 參考 pages/02 的成功解法
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()