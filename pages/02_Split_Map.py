import solara
import leafmap.leafmap as leafmap

def create_split_map():
    # 建立地圖，定位在霧社水庫
    m = leafmap.Map(
        center=[24.015, 121.145], 
        zoom=13,
        height="700px",
        control_scale=True
    )
    
    # 加入捲簾功能 (Split Map)
    # 左邊：Google 衛星影像
    # 右邊：Google 街道地圖
    m.split_map(
        left_layer="SATELLITE", 
        right_layer="ROADMAP"
    )
    
    # 加入文字標記
    m.add_text("衛星影像", position="bottomleft")
    m.add_text("街道地圖", position="bottomright")
    
    return m

@solara.component
def Page():
    # 使用 use_memo 避免重複渲染
    map_object = solara.use_memo(create_split_map, dependencies=[])

    solara.Title("環境變遷對比")

    with solara.Columns([1, 3]):
        
        # --- 左側：導覽資訊 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f0f2f6", "height": "100%"}):
            solara.Markdown("## ⚔️ 環境今昔對照")
            solara.Markdown("透過左右滑動的捲簾(Split Map)，比較不同圖層下的地景差異。")
            
            solara.Markdown("---")
            
            # 案例介紹
            with solara.Card("💧 案例：霧社水庫", margin=0, elevation=1):
                solara.Markdown("""
                又稱碧湖，是台14甲線前往清境與武嶺的必經之地。
                
                **觀察重點：**
                1. **水庫淤積**：透過衛星影像，可觀察濁水溪上游帶來的泥沙淤積情形。
                2. **開發邊界**：比較右側地圖上的道路與左側衛星圖中的開墾地。
                """)
                
            solara.Markdown("---")
            solara.Info("💡 提示：拖曳地圖中央的「分隔線」來切換視野。")

        # --- 右側：捲簾地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                # ★★★ 關鍵修正：2D 地圖要用 element() ★★★
                map_object.element()

Page()