import solara

# 設定頁面標題
@solara.component
def Page():
    
    # --- 1. 頁面標題區 ---
    with solara.Column(style={"padding": "20px"}):
        solara.Title("橫貫台灣：從平地到雲端") 
        
        solara.Markdown(r"""
        # 🏔️ 橫貫台灣：中橫與台14甲的地理探索
        
        歡迎來到我們的 GIS 期末報告！這是一個基於 **Solara** 建構的地理資訊系統。
        我們將帶領你穿越台灣最壯麗的公路——**中部橫貫公路 (台8線)** 與 **合歡山公路 (台14甲)**。
        
        *(目前地圖功能維護中，請先瀏覽專案介紹)*
        """)

    # --- 2. 關鍵地點展示 (使用卡片代替地圖) ---
    with solara.Column(style={"padding": "20px", "background-color": "#f0f2f6", "border-radius": "10px"}):
        solara.Markdown("### 📍 路線亮點")
        
        with solara.Row(gap="20px", style={"flex-wrap": "wrap"}):
            # 卡片 1
            with solara.Card("起點：台灣地理中心碑", margin=2):
                solara.Markdown("**海拔 450m**")
                solara.Markdown("位於南投埔里，是台灣地理幾何中心。")
                # 放一張靜態圖片代替地圖
                solara.Image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Geographic_Center_of_Taiwan_Monument_20090620.jpg/640px-Geographic_Center_of_Taiwan_Monument_20090620.jpg", width="100%")
            
            # 卡片 2
            with solara.Card("最高點：武嶺", margin=2):
                solara.Markdown("**海拔 3275m**")
                solara.Markdown("台灣公路最高點，也是單車騎士的聖地。")
                solara.Image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Wuling_and_Hehuanshan_East_Peak_20110522.jpg/640px-Wuling_and_Hehuanshan_East_Peak_20110522.jpg", width="100%")
                
            # 卡片 3
            with solara.Card("終點：太魯閣", margin=2):
                solara.Markdown("**海拔 60m**")
                solara.Markdown("世界級峽谷景觀，立霧溪切穿大理岩。")
                solara.Image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Taroko_Gorge_and_Liwu_River_20080313.jpg/640px-Taroko_Gorge_and_Liwu_River_20080313.jpg", width="100%")

    # --- 3. 專案目標 ---
    with solara.Column(style={"padding": "20px"}):
        solara.Markdown("""
        ### 🎯 我們要做什麼？
        1. **視覺化**：透過 3D 地形圖，展現高低落差的震撼。
        2. **環境變遷**：觀察霧社水庫與太魯閣峽谷的環境特徵。
        3. **風險分析**：分析道路沿線的潛在災害風險。
        """)

    # --- 4. 頁尾 ---
    with solara.Column(style={"padding": "20px", "border-top": "1px solid #ddd", "margin-top": "20px"}):
        solara.Markdown("""
        **組員名單**：地理系 114級
        *本專案使用 GitHub Codespaces 開發，部署於 Hugging Face Spaces。*
        """)

Page()