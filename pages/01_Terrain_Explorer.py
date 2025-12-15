import solara
import leafmap.maplibregl as leafmap

# 武嶺座標
WULING_CENTER = [121.276, 24.137]

def create_3d_map():
    # 建立地圖
    m = leafmap.Map(
        center=WULING_CENTER,
        zoom=11,
        pitch=60,       # 傾斜 60 度，強調立體感
        bearing=30,     # 旋轉 30 度，順著中央山脈走向
        style="positron",
        height="100%"
    )

    # 加入地形
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    
    # 設定地形誇張係數 (讓山看起來更陡)
    m.set_terrain({
        "source": "aws-terrain", 
        "exaggeration": 1.5 
    })

    m.add_layer_control()
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_3d_map, dependencies=[])

    solara.Title("3D 地形探索")

    # 使用兩欄式佈局：左邊是導覽，右邊是大地圖
    with solara.Columns([1, 3]):
        
        # --- 左側：導覽資訊 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f8f9fa", "height": "100%"}):
            solara.Markdown("## 🦅 雲端上的公路")
            solara.Markdown("這條路線穿越了台灣的屋脊——中央山脈。透過 3D 視角，我們可以觀察到劇烈的地形起伏。")
            
            solara.Markdown("---")
            
            # 操作教學
            with solara.Card("🎮 如何操作", margin=0, elevation=1):
                solara.Markdown("""
                * **旋轉**：按住 `滑鼠右鍵` 拖曳
                * **平移**：按住 `滑鼠左鍵` 拖曳
                * **縮放**：滾動滑鼠滾輪
                """)
            
            solara.Markdown("---")
            
            # 觀察重點
            solara.Markdown("### 🧐 觀察重點")
            
            with solara.ExpansionPanel("1. 劇烈的爬升"):
                solara.Markdown("從埔里(450m) 到 武嶺(3275m)，短短 50 公里內爬升了近 3000 公尺，造就了豐富的植被垂直變化。")
                
            with solara.ExpansionPanel("2. 立霧溪的襲奪"):
                solara.Markdown("往東看，可以看到立霧溪向源侵蝕造成的險峻峽谷（太魯閣），與西部平緩的合歡山台地形成強烈對比。")
                
            with solara.ExpansionPanel("3. 單面山地形"):
                solara.Markdown("合歡山東峰與主峰呈現明顯的單面山地形，東側陡峭、西側平緩，這是板塊擠壓與差異侵蝕的見證。")

        # --- 右側：3D 地圖 ---
        with solara.Column(style={"height": "800px", "padding": "0"}):
            # 這裡我們用一個 Card 把地圖包起來，更有質感
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()

Page()