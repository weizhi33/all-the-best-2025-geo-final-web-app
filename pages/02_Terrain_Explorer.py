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

# 地形誇張度變數 (預設 1.5)
terrain_exaggeration = solara.reactive(1.5)
current_view = solara.reactive("overview")

def create_3d_map(view_key, exaggeration_value):
    view = VIEW_POINTS.get(view_key, VIEW_POINTS["overview"])
    
    m = leafmap.Map(
        center=view["center"],
        zoom=view["zoom"],
        pitch=view["pitch"],
        bearing=view["bearing"],
        style="liberty",
        height="700px"
    )

    # 1. 衛星圖層
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

    # 2. 路網圖層
    m.add_source("google-roads", {
        "type": "raster",
        "tiles": ["https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}"],
        "tileSize": 256
    })
    m.add_layer({
        "id": "google-roads-layer",
        "type": "raster",
        "source": "google-roads",
        "paint": {"raster-opacity": 0.8}
    })

    # 3. [修正重點] 地形來源設定
    # 這裡是最容易出錯的地方，參數必須完全精準
    m.add_source("aws-terrain-source", {
        "type": "raster-dem",
        # 注意：對於 XYZ 連結，必須使用 'tiles' (陣列)，不能用 'url'
        "tiles": ["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"],
        # 注意：AWS 必須指定 encoding 為 'terrarium'，否則高度會算錯
        "encoding": "terrarium",
        "tileSize": 256,
        "maxzoom": 15
    })
    
    # 4. 設定地形 (exaggeration)
    m.set_terrain({
        "source": "aws-terrain-source", 
        "exaggeration": float(exaggeration_value) # 強制轉成 float 確保相容
    })

    m.add_layer_control()
    return m

@solara.component
def Page():
    # 建立地圖物件
    map_object = solara.use_memo(
        lambda: create_3d_map(current_view.value, terrain_exaggeration.value), 
        dependencies=[current_view.value, terrain_exaggeration.value]
    )

    solara.Title("3D 地形探索")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f8f9fa", "height": "100%"}):
            solara.Markdown("## 🦅 雲端上的公路")
            solara.Markdown("這條路線穿越了台灣的屋脊。")
            
            solara.Markdown("---")
            
            with solara.Card("🧪 GIS 實驗室：地形誇張", margin=0, elevation=1):
                solara.Markdown("調整山脈的「垂直誇張度」，看看地形有什麼變化！")
                
                solara.SliderFloat(
                    label="地形倍率", 
                    value=terrain_exaggeration, 
                    min=0.0, 
                    max=5.0, 
                    step=0.5
                )
                
                solara.Markdown(f"目前倍率：**{terrain_exaggeration.value}x**")
                
                if terrain_exaggeration.value > 2.5:
                    solara.Warning("小心！這已經比喜馬拉雅山還陡了！")
                if terrain_exaggeration.value == 0:
                    solara.Info("現在是完全平坦的 2D 模式。")

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

        # --- 右側：3D 地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                # 使用 solara.Div + key 強制刷新
                solara.Div(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"},
                    # key 的作用是讓 React 認為這是一個全新的元件，進而強制重繪
                    key=f"map-{terrain_exaggeration.value}-{current_view.value}"
                )

Page()