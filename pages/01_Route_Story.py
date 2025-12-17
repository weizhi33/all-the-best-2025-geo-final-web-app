import solara
import leafmap.maplibregl as leafmap

# --- 1. 定義故事資料 ---
STORY_STEPS = [
    {
        "title": "1. 起點：台灣地理中心",
        "text": "旅程從南投埔里開始。這裡是台灣的地理幾何中心，海拔約 450m。我們將從這裡沿著台 14 線往東，開始挑戰中央山脈。",
        "location": [120.981, 23.976], 
        "zoom": 13,
        "pitch": 45,
        "marker_text": "埔里盆地"
    },
    {
        "title": "2. 碧湖水色：霧社水庫",
        "text": "進入山區後，首先映入眼簾的是「碧湖」。這是日治時期興建的水庫，負責調節濁水溪上游的水量。雖然美麗，但近年來面臨嚴重的淤積問題。",
        "location": [121.145, 24.015],
        "zoom": 13.5,
        "pitch": 60,
        "marker_text": "霧社水庫"
    },
    {
        "title": "3. 歷史秘境：消失的滑雪場",
        "text": "你相信台灣曾經能滑雪嗎？在合歡山東峰與合歡尖山之間的這片谷地，60 年代曾設有滑雪纜車。這裡獨特的「圈谷地形」能留住積雪，是台灣罕見的冰河遺跡。",
        "location": [121.282, 24.139],
        "zoom": 15,
        "pitch": 70, 
        "marker_text": "舊滑雪場遺址"
    },
    {
        "title": "4. 公路巔峰：武嶺",
        "text": "海拔 3275 公尺，全台灣公路的最高點！站上觀景台，腳下是台 14 甲線最著名的蜿蜒路段。這裡是無數騎士與遊客挑戰自我的終極目標。",
        "location": [121.276, 24.137],
        "zoom": 15,
        "pitch": 50,
        "marker_text": "武嶺亭 (3275m)"
    },
    {
        "title": "5. 峽谷驚奇：燕子口",
        "text": "翻過中央山脈一路下切，我們來到了太魯閣峽谷最精華的「燕子口」。立霧溪在這裡切穿大理岩，形成深邃的「V型谷」。這裡也是落石風險最高的區域之一。",
        "location": [121.565, 24.173],
        "zoom": 16,
        "pitch": 80,
        "marker_text": "燕子口步道"
    }
]

# --- 2. Solara 狀態管理 ---
current_step = solara.reactive(0)

# --- 3. 地圖創建函數 (更新版：純淨衛星地圖) ---
def create_story_map(step_index):
    step_data = STORY_STEPS[step_index]
    
    # 建立地圖
    m = leafmap.Map(
        center=step_data["location"],
        zoom=step_data["zoom"],
        pitch=step_data["pitch"],
        bearing=0,
        style="liberty", 
        height="600px"
    )
    
    # 1. [修正] 改用 Google Satellite (純衛星，無標籤)
    # 關鍵參數：lyrs=s (原本是 y)
    m.add_source("google-satellite", {
        "type": "raster",
        "tiles": ["https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"],
        "tileSize": 256
    })
    
    # 2. 加入圖層
    m.add_layer({
        "id": "google-satellite-layer",
        "type": "raster",
        "source": "google-satellite",
        "paint": {"raster-opacity": 1.0}
    })
    
    # 3. 加入地形
    m.add_source("aws-terrain", {
        "type": "raster-dem",
        "url": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
        "tileSize": 256,
        "encoding": "terrarium"
    })
    m.set_terrain({"source": "aws-terrain", "exaggeration": 1.5})
    
    # 4. 加入標記 (維持我們設計好的樣式)
    popup_html = f"""
        <div style="font-weight: bold; font-size: 15px; color: #333; font-family: sans-serif;">
            📍 {step_data['marker_text']}
        </div>
    """
    m.add_marker(
        lng_lat=step_data["location"],
        popup={"html": popup_html}
    )
    
    m.add_layer_control()
    return m

# --- 4. 頁面組件 ---
@solara.component
def Page():
    step_data = STORY_STEPS[current_step.value]
    
    map_object = solara.use_memo(
        lambda: create_story_map(current_step.value),
        dependencies=[current_step.value]
    )

    solara.Title("中橫故事地圖")

    with solara.Column(style={"padding": "20px"}):
        solara.Markdown("# 🛤️ 穿越中橫：從平地到雲端的旅程")
        
        with solara.Columns([2, 1]):
            # 左側：地圖
            with solara.Column():
                with solara.Card(elevation=2, margin=0, style={"padding": "0"}):
                    map_object.to_solara()
            
            # 右側：故事控制
            with solara.Column(style={"padding-left": "20px"}):
                solara.Text(f"場景 {current_step.value + 1} / {len(STORY_STEPS)}", style={"font-weight": "bold", "color": "#666"})
                
                solara.Markdown(f"## {step_data['title']}")
                solara.Markdown("---")
                solara.Markdown(f"{step_data['text']}")
                
                solara.Markdown("---")
                
                with solara.Row(justify="center", gap="10px", style={"margin-top": "20px"}):
                    solara.Button(
                        "⬅️ 上一站", 
                        on_click=lambda: current_step.set(max(0, current_step.value - 1)),
                        disabled=(current_step.value == 0),
                        outlined=True
                    )
                    solara.Button(
                        "下一站 ➡️", 
                        on_click=lambda: current_step.set(min(len(STORY_STEPS) - 1, current_step.value + 1)),
                        disabled=(current_step.value == len(STORY_STEPS) - 1),
                        color="primary"
                    )

Page()