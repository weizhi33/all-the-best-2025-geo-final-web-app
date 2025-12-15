import solara
import leafmap.maplibregl as leafmap

# 武嶺座標 (經度, 緯度) -> 這是 maplibregl 的正確順序！
WULING_CENTER = [121.276, 24.137]

def create_3d_map():
    # 建立地圖物件
    m = leafmap.Map(
        center=WULING_CENTER,
        zoom=11, 
        pitch=60,      # 傾斜 60 度，展現立體感
        bearing=30,    # 旋轉 30 度，視角更佳
        style="positron", # 使用與成功案例相同的穩定底圖
        height="700px" # 明確指定高度
    )
    
    # 加入 3D 地形來源 (使用 AWS 免費地形圖磚)
    m.add_terrain(
        source="aws", 
        exaggeration=1.5 # 地形誇張倍率
    )
    
    # 加入導航控制項 (右上角的縮放按鈕)
    m.add_layer_control()
    
    return m

@solara.component
def Page():
    # 使用 use_memo 快取地圖，避免每次重繪都重新載入 (參考你的 04_story.py)
    # dependencies=[] 代表只建立一次
    map_object = solara.use_memo(create_3d_map, dependencies=[])

    with solara.Column(style={"padding": "20px"}):
        solara.Title("3D 地形探索")
        solara.Markdown("# 🦅 雲端上的公路：3D 視角")
        
        with solara.Card(elevation=2):
            solara.Markdown("""
            **操作說明：**
            * **旋轉**：按住 `滑鼠右鍵` 拖曳
            * **平移**：按住 `滑鼠左鍵` 拖曳
            * **縮放**：滾動滑鼠滾輪
            """)

    # 顯示地圖
    with solara.Column(style={"height": "750px"}):
        # 這是最關鍵的一行！使用 maplibregl 專用的渲染方法
        map_object.to_solara()

Page()