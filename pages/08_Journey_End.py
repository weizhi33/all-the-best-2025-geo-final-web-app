import solara
import leafmap.foliumap as leafmap
import io

# ==========================================
# 1. 定義時光機圖源 (Sentinel-2 哨兵衛星)
# ==========================================
TIMELAPSE_LAYERS = {
    2016: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2016 (起點)：哨兵二號最早的完整年度影像。請觀察河口沙洲的原始形狀。"
    },
    2017: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2017_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2017 年：觀察北側海岸線是否有變化。"
    },
    2018: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2018_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2018 年：注意陰陽海 (混濁海水) 的擴散範圍。"
    },
    2019: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2019_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2019 年：颱風較多的一年，輸沙量增加，河口可能較混濁。"
    },
    2020: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2020_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2020 年：台灣大旱年。河川流量極少，輸沙量減低，海水可能較清澈。"
    },
    2021: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2021_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2021 年：乾旱緩解。觀察沙洲形狀是否因水量恢復而改變。"
    },
    2022: {
        "url": "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2022_3857/default/g/{z}/{y}/{x}.jpg",
        "desc": "2022 (最新)：目前的海岸線狀態。"
    }
}

# 年份列表
AVAILABLE_YEARS = sorted(TIMELAPSE_LAYERS.keys())
year_index = solara.reactive(len(AVAILABLE_YEARS) - 1)

@solara.component
def Page():
    
    current_year = AVAILABLE_YEARS[year_index.value]
    layer_info = TIMELAPSE_LAYERS[current_year]
    
    def get_sentinel_map():
        # 立霧溪出海口中心
        ESTUARY_CENTER = [24.138, 121.655]
        
        m = leafmap.Map(
            center=ESTUARY_CENTER,
            zoom=13,
            draw_control=False,
            measure_control=False,
        )
        
        # 加入 Sentinel-2 衛星圖層
        m.add_tile_layer(
            url=layer_info["url"],
            name=f"Sentinel-2 {current_year}",
            attribution="Sentinel-2 cloudless - https://s2maps.eu"
        )
        
        # 標記出海口位置
        m.add_marker(
            location=ESTUARY_CENTER,
            popup="<b>立霧溪出海口</b><br>山與海的交界",
            icon=leafmap.folium.Icon(color="blue", icon="tint")
        )
        
        return m

    # 記憶體輸出 (io.BytesIO) - 穩定不報錯
    m = get_sentinel_map()
    fp = io.BytesIO()
    m.save(fp, close_file=False)
    fp.seek(0)
    map_html_str = fp.read().decode('utf-8')

    solara.Title("海岸線時光機")

    with solara.Column(style={"height": "100vh", "padding": "0"}):
        
        # --- 標題區 ---
        with solara.Row(style={"padding": "20px", "background-color": "#2c3e50", "align-items": "center"}):
             solara.HTML(tag="h2", unsafe_innerHTML="🌊 08. 旅程終點：海岸變遷時光機", style="color: white; margin: 0;")
             solara.Success("💡 本頁利用 Sentinel-2 衛星影像，觀測 2016-2022 年間立霧溪口的輸沙與海岸線變化。", icon="mdi-satellite-uplink")

        # --- 內容區 ---
        with solara.Columns([1, 3], style={"height": "calc(100vh - 100px)"}):
            
            # 左側：控制面板與地理教室
            with solara.Column(style={"padding": "20px", "background-color": "white", "height": "100%", "overflow-y": "auto"}):
                
                # 1. 時光機滑桿
                with solara.Card("📅 衛星時光機", margin=0, elevation=2):
                    solara.Markdown(f"### 當前年份：{current_year}")
                    solara.SliderInt(
                        label="拖曳年份",
                        value=year_index,
                        min=0,
                        max=len(AVAILABLE_YEARS) - 1,
                        step=1,
                        tick_labels=AVAILABLE_YEARS,
                        thumb_label=False
                    )
                    solara.Markdown("---")
                    solara.Markdown(f"**觀察重點**：\n{layer_info['desc']}")

                solara.Markdown("<br>")

                # 2. 地理教室：小平地的形成 (您指定新增的部分)
                with solara.Card("🏖️ 那塊小平地怎麼來的？", margin=0, elevation=2):
                    solara.Markdown("""
                    **立霧溪沖積扇 (Liwu River Delta)**
                    
                    您在地圖上看到的河口小平地，其實是兩股巨大力量的「戰場」：
                    
                    1.  **河流輸沙 (推出去)**：
                        立霧溪從 3000 公尺高山急流而下，切割大理石岩壁，挾帶大量泥沙衝向大海。
                    
                    2.  **海浪侵蝕 (打回來)**：
                        太平洋的波浪與沿岸流非常強勁，不斷拍打河口。
                    
                    **結果**：
                    泥沙來不及堆積成大三角洲，就被海浪打散帶走，只能形成這個小型的**扇狀沖積平原**。這也是為什麼東部海岸的三角洲通常都不大的原因。
                    """)
                
                solara.Markdown("---")
                solara.Info("💡 陰陽海現象：若您選擇 2019 等颱風較多的年份，會發現河口海水呈現明顯的土黃色，這就是大量輸沙的證明。")

            # 右側：地圖
            with solara.Column(style={"height": "100%", "padding": "0"}):
                solara.Div(
                    children=[
                         solara.HTML(
                            tag="iframe",
                            attributes={
                                "srcdoc": map_html_str,
                                "width": "100%",
                                "height": "100%",
                                "style": "border: none; width: 100%; height: 750px;" 
                            }
                        )
                    ],
                    style={"height": "100%", "width": "100%"},
                    key=f"sentinel-map-{current_year}"
                )

Page()