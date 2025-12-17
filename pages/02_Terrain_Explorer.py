import solara
import leafmap.maplibregl as leafmap

# --- 定義觀察點位 ---
VIEW_POINTS = {
    "overview": {
        "center": [121.276, 24.137], "zoom": 11, "pitch": 60, "bearing": 30
    },
    "puli": { 
        "center": [121.05, 24.00], "zoom": 12, "pitch": 70, "bearing": 80
    },
    "liwu": { 
        "center": [121.50, 24.18], "zoom": 12, "pitch": 60, "bearing": -45
    },
    "hehuanshan": { 
        "center": [121.28, 24.14], "zoom": 14, "pitch": 75, "bearing": 160
    }
}

current_view = solara.reactive("overview")

def create_3d_map(view_key):
    view = VIEW_POINTS.get(view_key, VIEW_POINTS["overview"])
    
    m = leafmap.Map(
        center=view["center"],
        zoom=view["zoom"],
        pitch=view["pitch"],
        bearing=view["bearing"],
        style="liberty",
        height="700px"
    )

    # 1. 第一層：Google 純衛星圖 (底圖)
    # lyrs=s (Satellite only)
    m.add_source("google-satellite", {
        "type": "raster",
        "tiles": ["https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"],
        "tileSize": 256
    })
    m.add_layer({
        "id": "google-satellite-layer",
        "type": "raster",
        "source": "google-satellite",
        "paint": {"raster-opacity": 1.0}
    })

    # 2. [新增] 第二層：Google 純路網 (透明疊加層)
    # lyrs=h (Hybrid roads only) - 這層只有路和字，背景透明
    m.add_source("google-roads", {
        "type": "raster",
        "tiles": ["https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}"],
        "tileSize": 256
    })
    m.add_layer({
        "id": "google-roads-layer",
        "type": "raster",
        "source": "google-roads",
        "paint": {
            "raster-opacity": 0.8  # 設定 0.8 讓路網稍微柔和一點，不要蓋過山脈的質感
        }
    })

    # 3. 加入 3D 地形 (讓地圖凸起來)
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    m.set_terrain({
        "source": "aws-terrain", 
        "exaggeration": 1.5 
    })

    m.add_layer_control()
    return m

@solara.component
def Page():
    map_object = solara.use_memo(
        lambda: create_3d_map(current_view.value), 
        dependencies=[current_view.value]
    )

    solara.Title("3D 地形探索")

    with solara.Columns([1, 3]):
        
        # --- 左側：導覽控制 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f8f9fa", "height": "100%"}):
            solara.Markdown("## 🦅 雲端上的公路")
            solara.Markdown("這條路線穿越了台灣的屋脊。透過 3D 視角，我們可以觀察到劇烈的地形起伏。")
            
            solara.Markdown("---")
            solara.Markdown("### 🧐 點擊切換視角")
            
            with solara.Card(margin=0, elevation=1):
                with solara.Column(gap="10px"):
                    solara.Button("1. 全覽視角 (武嶺)", 
                                 on_click=lambda: current_view.set("overview"), 
                                 text=True, outlined=True)
                    
                    solara.Button("2. 埔里的爬升", 
                                 on_click=lambda: current_view.set("puli"), 
                                 text=True, outlined=True)
                    
                    solara.Button("3. 立霧溪峽谷", 
                                 on_click=lambda: current_view.set("liwu"), 
                                 text=True, outlined=True)
                    
                    solara.Button("4. 合歡山單面山", 
                                 on_click=lambda: current_view.set("hehuanshan"), 
                                 text=True, outlined=True)

            solara.Markdown("---")
            with solara.Details(summary="💡 地理小知識"):
                solara.Markdown("""
                * **單面山**：合歡東峰東側陡峭、西側平緩，是典型的單面山地形。
                * **向源侵蝕**：立霧溪強烈的下切力量，造就了太魯閣峽谷。
                """)

        # --- 右側：3D 地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                map_object.to_solara()

Page()