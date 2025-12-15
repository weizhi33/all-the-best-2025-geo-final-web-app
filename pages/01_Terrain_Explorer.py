import solara
import leafmap.maplibregl as leafmap

# 武嶺座標 (經度 Lon, 緯度 Lat) - MapLibre 的順序
WULING_CENTER = [121.276, 24.137]

def create_3d_map():
    # 1. 建立基礎地圖
    m = leafmap.Map(
        center=WULING_CENTER,
        zoom=11,
        pitch=60,       # 傾斜視角
        bearing=30,     # 旋轉視角
        style="positron", # 乾淨的底圖
        height="100%"
    )

    # 2. [修正] 手動加入 AWS 免費地形來源 (避開 add_terrain 報錯)
    # 定義地形來源 (RGB Encoded DEM)
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    
    # 3. [修正] 啟用地形 (設定誇張係數)
    # 這裡直接告訴地圖使用剛剛定義的 'aws-terrain' 來源
    m.set_terrain({
        "source": "aws-terrain", 
        "exaggeration": 1.5 
    })

    # 4. 加入控制項
    m.add_layer_control()
    
    return m

@solara.component
def Page():
    # 使用 use_memo 確保地圖只建立一次，切換頁面不會重跑
    map_object = solara.use_memo(create_3d_map, dependencies=[])

    with solara.Column(style={"padding": "20px"}):
        solara.Title("3D 地形探索")
        solara.Markdown("# 🦅 雲端上的公路：3D 視角")
        solara.Markdown("請使用 **滑鼠右鍵** 旋轉視角，體驗從埔里一路爬升至武嶺的劇烈高差。")

    # 顯示地圖容器
    with solara.Column(style={"height": "700px"}):
        # 關鍵：使用 maplibregl 專用的渲染方法
        map_object.to_solara()

Page()