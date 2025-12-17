import solara
import leafmap.leafmap as leafmap

def create_water_map():
    # 霧社水庫 (碧湖) 座標
    WUSHE_CENTER = [24.018, 121.148] # 稍微往北一點，看得到大壩和淤積尾端
    
    # 建立捲簾地圖
    # 左邊：Google 衛星 (lyrs=s) -> 看得到真實的水色(混濁/淤積)
    # 右邊：Google 地形 (lyrs=p) -> 看得到 V 型河谷與等高線
    m = leafmap.split_map(
        left_layer="GOOGLE_SATELLITE",
        right_layer="GOOGLE_TERRAIN",
        left_label="衛星：泥沙與水色",
        right_label="地形：縱谷地形",
        center=WUSHE_CENTER,
        zoom=14,
        control_position="bottomleft"
    )
    
    # 強制設定高度
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_water_map, dependencies=[])

    solara.Title("水的旅程")

    with solara.Columns([1, 3]):
        
        # --- 左側：地理故事 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f0f2f6", "height": "100%"}):
            solara.Markdown("## 💧 水的旅程：霧社與武界")
            solara.Markdown("在中橫霧社支線(台14甲)的起點，這座水庫不僅是風景，更是台灣水力發電的心臟。")
            
            solara.Markdown("---")
            
            # 案例 1: 霧社水庫
            with solara.Card("🛑 霧社水庫 (碧湖)", margin=0, elevation=1):
                solara.Markdown("""
                請觀察左側 **衛星影像**：
                * **土黃色水域**：萬大發電廠附近的泥沙淤積嚴重，這是濁水溪上游地質破碎的證明。
                * **功能**：它其實是日月潭的「調節池」，負責攔截泥沙，盡量讓乾淨的水流往下游。
                """)
            
            solara.Markdown("---")
            
            # 案例 2: 武界引水 (你的興趣點!)
            with solara.Details(summary="🌊 秘境：武界引水隧道"):
                solara.Markdown("""
                **你看不到的地下河流！**
                
                在水庫下游的「武界壩」，有一條長達 **15 公里** 的地底隧道（新武界引水隧道）。
                
                它直接穿過中央山脈，把濁水溪的水「越域引水」送到 **日月潭** 儲存發電。這就是為什麼日月潭水位能維持，以及武界被稱為「雲之故鄉」的原因。
                """)
            
            solara.Markdown("---")
            solara.Info("💡 地圖操作：拖曳中間滑桿。右邊的地形圖可以清楚看到河流切出的深谷。")

        # --- 右側：捲簾地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                # 再次使用 Column 包覆大法，確保地圖不會跑版
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()