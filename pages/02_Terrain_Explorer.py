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

# 1. 新增：地形誇張度變數 (預設 1.5)
terrain_exaggeration = solara.reactive(1.5)

current_view = solara.reactive("overview")

# 接收 exaggeration 參數
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

    # 衛星圖層
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

    # 路網圖層
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

    # 2. 地形來源
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    
    # 3. 設定地形 (使用滑桿傳進來的數值!)
    m.set_terrain({
        "source": "aws-terrain", 
        "exaggeration": exaggeration_value  # <--- 這裡是關鍵
    })

    m.add_layer_control()
    return m

@solara.component
def Page():
    # 當 slider 拉動時，地圖會重新計算
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
            
            # ★★★ 新增：GIS 實驗室 (God Mode) ★★★
            with solara.Card("🧪 GIS 實驗室：地形誇張", margin=0, elevation=1):
                solara.Markdown("調整山脈的「垂直誇張度」，看看地形有什麼變化！")
                
                # 滑桿：從 0 (平地) 到 4 (超誇張高山)
                solara.SliderFloat(
                    label="地形倍率", 
                    value=terrain_exaggeration, 
                    min=0.0, 
                    max=4.0, 
                    step=0.1
                )
                
                # 顯示目前的數值
                solara.Markdown(f"目前倍率：**{terrain_exaggeration.value:.1f}x**")
                
                if terrain_exaggeration.value > 2.5:
                    solara.Warning("小心！這已經比喜馬拉雅山還陡了！")

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
                map_object.to_solara()

Page()