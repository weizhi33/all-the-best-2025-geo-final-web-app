import solara
import leafmap.leafmap as leafmap

def create_ski_map():
    # 合歡山舊滑雪場座標 (合歡東峰與合歡尖山之間的谷地，松雪樓旁)
    SKI_CENTER = [24.140, 121.283]
    
    # 定義圖磚網址 (暴力法確保穩定)
    # 左：純衛星 (lyrs=s) -> 看現在的地貌(箭竹林)
    # 右：地形圖 (lyrs=p) -> 看等高線與暈渲(圈谷地形)
    URL_SATELLITE = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
    URL_TERRAIN = "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}"

    m = leafmap.split_map(
        left_layer=URL_SATELLITE,
        right_layer=URL_TERRAIN,
        left_label="現在：箭竹林",
        right_label="地形：冰河圈谷",
        center=SKI_CENTER,
        zoom=16, # 拉近一點看細節
        control_position="bottomleft"
    )
    
    m.layout.height = "700px"
    return m

@solara.component
def Page():
    map_object = solara.use_memo(create_ski_map, dependencies=[])

    solara.Title("消失的滑雪場")

    with solara.Columns([1, 3]):
        
        # --- 左側：故事區 ---
        with solara.Column(style={"padding": "20px", "background-color": "#f0f2f6", "height": "100%"}):
            solara.Markdown("## ⛷️ 亞熱帶的滑雪夢")
            solara.Markdown("你沒看錯，台灣曾經有滑雪場。就在合歡山東峰的坡面上，甚至還有長達 400 公尺的纜車。")
            
            solara.Markdown("---")
            
            with solara.Card("🏔️ 地理偵探：為什麼是這裡？", margin=0, elevation=1):
                solara.Markdown("""
                請仔細觀察右側的 **地形圖**：
                
                1.  **U型圈谷**：你會發現等高線呈現半圓形的「碗狀」。這是冰河時期留下的遺跡。
                2.  **避風積雪**：這種凹陷的地形可以擋住強風，讓雪留得住，不會被吹走。
                
                這就是為什麼在 1960 年代，這裡被選為陸軍寒訓中心與滑雪場的原因。
                """)
            
            solara.Markdown("---")
            
            with solara.Details(summary="📅 歷史變遷"):
                solara.Markdown("""
                * **1963年**：中華民國滑雪協會成立，開始推廣滑雪。
                * **1970年代**：合歡山松雪樓是滑雪俱樂部的大本營。
                * **1980年代後**：隨著氣候暖化與出國滑雪普及，這裡的纜車廢棄，最終拆除。
                """)
                
            solara.Info("💡 提示：雖然現在只剩下箭竹林(左圖)，但地形(右圖)永遠記住了那段歷史。")

        # --- 右側：地圖區 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                solara.Column(
                    children=[map_object], 
                    style={"width": "100%", "height": "700px"}
                )

Page()