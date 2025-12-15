import solara
import leafmap.maplibregl as leafmap

@solara.component
def Page():
    # 標題區
    with solara.Column(style={"padding": "20px"}):
        solara.Title("3D 地形探索")
        solara.Markdown("# 🦅 雲端上的公路：3D 視角")
        solara.Markdown("""
        這是利用 **MapLibre GL** 技術渲染的 3D 地形圖。
        
        **操作說明：**
        * **旋轉視角**：按住 `滑鼠右鍵` 拖曳，或按住 `Ctrl + 左鍵` 拖曳。
        * **縮放**：滾動滑鼠滾輪。
        """)

    # 建立地圖物件
    # style="positron" 是一個帶有地形陰影的乾淨底圖
    m = leafmap.Map(
        center=[24.137, 121.276], # 中心點設在武嶺
        zoom=11, 
        pitch=60, # 關鍵：傾斜 60 度，這樣才有 3D 立體感 [cite: 3083]
        bearing=30, # 旋轉 30 度，讓山脈走向比較好看
        style="positron"
    )
    
    # 這是關鍵！加入 3D 地形來源 (使用 AWS 免費地形圖磚) 
    m.add_terrain(
        source="aws", 
        exaggeration=1.5 # 地形誇張倍率，設大一點(1.5倍)山會看起來更陡峭、更壯觀
    )

    # 顯示地圖
    with solara.Column(style={"height": "700px"}):
        # 注意：這裡一定要用 to_solara()，不能用 element() [cite: 2862]
        m.to_solara()

Page()