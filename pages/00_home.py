import solara
import leafmap.maplibregl as leafmap  # 使用 3D 後端
import pydeck as pdk # 確保 pydeck 有被載入

# 設定頁面標題
@solara.component
def Page():
    
    # --- 1. 頁面標題區 ---
    with solara.Column(style={"padding": "20px"}):
        solara.Title("橫貫台灣：從平地到雲端") 
        
        solara.Markdown(r"""
        # 🏔️ 橫貫台灣：中橫與台14甲的地理探索
        
        歡迎來到我們的 GIS 期末報告！這是一個基於 **Solara** 與 **Leafmap** 建構的互動式地理資訊系統。
        我們將帶領你穿越台灣最壯麗的公路——**中部橫貫公路 (台8線)** 與 **合歡山公路 (台14甲)**。
        
        ### 🎯 專案目標
        1. **視覺化**：透過 3D 地形圖，展現從海拔 400m 直升 3275m 的劇烈地貌變化。
        2. **環境變遷**：利用衛星影像捲簾 (Split Map) 觀察霧社水庫與太魯閣峽谷的環境特徵。
        3. **風險分析**：結合 GeoPandas 分析道路沿線的潛在災害風險。
        """)

    # --- 2. 關鍵地點展示 ---
        solara.Markdown("### 📍 路線關鍵點")
        with solara.Row(gap="20px"):
            with solara.Card("起點：台灣地理中心碑", margin=0, elevation=2):
                solara.Markdown("位於南投埔里，海拔約 450m，是台灣地理幾何中心。")
            
            with solara.Card("最高點：武嶺", margin=0, elevation=2):
                solara.Markdown("海拔 3275m，台灣公路最高點，也是單車騎士的聖地。")
                
            with solara.Card("終點：太魯閣", margin=0, elevation=2):
                solara.Markdown("世界級峽谷景觀，立霧溪切穿大理岩形成的壯麗地貌。")

    # --- 3. 互動地圖預覽 ---
    with solara.Column(style={"padding": "20px"}):
        solara.Markdown("### 🗺️ 路線概覽")
        
        # 建立地圖物件
        # style="positron" 是一個很乾淨的底圖
        m = leafmap.Map(center=[24.0, 121.1], zoom=9, style="positron")
        
        # [關鍵修正] maplibregl 後端必須使用 to_solara() 才能顯示！
        # 這裡不使用 m.element()，那只適用於 ipyleaflet
        m.to_solara(height="600px")

    # --- 4. 頁尾 ---
    with solara.Column(style={"padding": "20px", "border-top": "1px solid #ddd"}):
        solara.Markdown("""
        ---
        **組員名單**：地理系 114級
        *本專案使用 GitHub Codespaces 開發，部署於 Hugging Face Spaces。*
        """)

Page()