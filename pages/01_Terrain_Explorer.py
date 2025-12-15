import solara
import leafmap.maplibregl as leafmap

# 武嶺座標 (經度 Lon, 緯度 Lat)
WULING_CENTER = [121.276, 24.137]

def create_3d_map():
    # 1. 建立地圖 (關鍵修正：height 改成固定的 "700px")
    m = leafmap.Map(
        center=WULING_CENTER,
        zoom=11,
        pitch=60,
        bearing=30,
        style="positron",
        height="700px"  # <--- 修正這裡：不要用 100%，用固定高度
    )

    # 2. 加入地形來源 (手動加入 AWS 地形)
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    
    # 3. 設定地形效果
    m.set_terrain({
        "source": "aws-terrain", 
        "exaggeration": 1.5 
    })

    m.add_layer_control()
    return m

@solara.component
def Page():
    # 使用 use_memo 快取地圖
    map_object = solara.use_memo(create_3d_map, dependencies=[])

    with solara.Column(style={"padding": "20px"}):
        solara.Title("3D 地形探索")
        solara.Markdown("# 🦅 雲端上的公路：3D 視角")
        solara.Markdown("請使用 **滑鼠右鍵** 旋轉視角。如果地圖未顯示，請稍後或是重新整理頁面。")

    # 顯示地圖
    with solara.Column(style={"min-height": "700px"}):
        map_object.to_solara()

Page()