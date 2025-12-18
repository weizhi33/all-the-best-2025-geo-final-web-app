import solara
import leafmap.leafmap as leafmap
from ipyleaflet import Polyline

# --- 模擬海岸線數據 (根據地理文獻趨勢推估) ---
# 格式：[緯度, 經度]
COASTLINE_DATA = {
    1904: [ # 日治時期：最飽滿的扇形
        [24.155, 121.650], [24.150, 121.655], [24.140, 121.662], 
        [24.130, 121.665], [24.120, 121.663]
    ],
    1950: [ # 早期：稍微退縮，但還算完整
        [24.155, 121.650], [24.150, 121.654], [24.140, 121.660], 
        [24.130, 121.663], [24.120, 121.662]
    ],
    1990: [ # 工業化後：開始顯著退縮
        [24.155, 121.649], [24.150, 121.653], [24.140, 121.658], 
        [24.130, 121.661], [24.120, 121.661]
    ],
    2024: [ # 現代：退縮最嚴重 (目前的海岸線)
        [24.155, 121.648], [24.150, 121.652], [24.140, 121.656], 
        [24.130, 121.660], [24.120, 121.660]
    ]
}

# 響應式變數：選中的年份
selected_year = solara.reactive(1904)

def create_time_machine_map(year):
    # 立霧溪出海口
    ESTUARY_CENTER = [24.135, 121.655]
    
    m = leafmap.Map(
        center=ESTUARY_CENTER,
        zoom=14,
        height="700px",
        google_map="SATELLITE" # 底圖固定用衛星
    )

    # 1. 基準線：2024年 (白色細線) - 用來當作比較基準
    line_now = Polyline(
        locations=COASTLINE_DATA[2024],
        color="white", weight=2, opacity=0.6,
        name="2024 基準線"
    )
    m.add_layer(line_now)

    # 2. 歷史線：選中年份 (彩色粗線) - 這是會動的！
    # 根據年份給不同顏色，增加視覺區別
    colors = {1904: "#ffcc00", 1950: "#ff9900", 1990: "#ff5050", 2024: "#00ccff"}
    current_color = colors.get(year, "red")
    
    line_history = Polyline(
        locations=COASTLINE_DATA[year],
        color=current_color, 
        weight=5, # 粗一點才明顯
        opacity=1.0,
        name=f"{year} 海岸線"
    )
    m.add_layer(line_history)
    
    return m

@solara.component
def Page():
    # 當滑桿年份改變時，重新計算地圖
    map_object = solara.use_memo(
        lambda: create_time_machine_map(selected_year.value), 
        dependencies=[selected_year.value]
    )

    solara.Title("終點：海岸線時光機")

    with solara.Columns([1, 3]):
        
        # --- 左側：控制面板 ---
        with solara.Column(style={"padding": "20px", "background-color": "#2c3e50", "color": "white", "height": "100%"}):
            solara.Markdown("## ⏳ 海岸線時光機")
            solara.Markdown("透過衛星影像與歷史數據，重建消失的國土。")
            
            solara.Markdown("---")
            
            # ★★★ 核心功能：年份滑桿 ★★★
            solara.Markdown(f"### 📅 目前年份：{selected_year.value}")
            solara.SliderInt(
                label="年份選擇",
                value=selected_year,
                min=1904, # 起始年份
                max=2024, # 結束年份
                step=None, # 設定為 None 表示只能選特定的 tick
                tick_labels=["1904", "1950", "1990", "2024"],
                thumb_label="always"
            )
            
            solara.Markdown("---")
            
            # 動態解說文字
            if selected_year.value == 1904:
                solara.Markdown("### 🟡 1904 (日治明治時期)")
                solara.Markdown("這是最原始的狀態。你可以看到**黃色線**離現在的白色海岸線非常遠，當時的沙灘非常寬廣，扇狀地發育完整。")
            elif selected_year.value == 1950:
                solara.Markdown("### 🟠 1950 (戰後初期)")
                solara.Markdown("中橫公路開通前。海岸線開始有些微變化，但仍維持自然的弧度。")
            elif selected_year.value == 1990:
                solara.Markdown("### 🔴 1990 (工業發展期)")
                solara.Markdown("亞洲水泥港口擴建，加上上游水壩攔砂效應浮現。**紅色線**已經大幅向內退縮，許多沙灘消失。")
            else:
                solara.Markdown("### 🔵 2024 (現代)")
                solara.Markdown("現在的海岸線。為了保護不再退縮的陸地，岸邊堆滿了消波塊。藍線與白線重合。")

            solara.Info("💡 觀察技巧：白色細線是現在的海岸。請嘗試快速切換 1904 與 2024，感受那段「消失的距離」。")

        # --- 右側：地圖 ---
        with solara.Column(style={"height": "750px", "padding": "0"}):
            with solara.Card(elevation=2, margin=0, style={"height": "100%", "padding": "0"}):
                # 使用 Div + key 強制刷新地圖，確保線條切換流暢
                solara.Div(
                    children=[map_object],
                    style={"width": "100%", "height": "700px"},
                    key=f"coast-map-{selected_year.value}"
                )

Page()