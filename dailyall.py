'''
臺灣證券交易所
個股日成交資訊
https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html

目標:
整合下拉式選單與元素的定位與操控，來下載交易資料，並擷圖
'''

'''
匯入套件
'''
# 操作 browser 的 驅動程式
from selenium import webdriver
# 負責開啟和關閉 Chrome 的套件
from selenium.webdriver.chrome.service import Service
# 自動下載 Chrome Driver 的套件
from webdriver_manager.chrome import ChromeDriverManager
# 例外處理的工具
from selenium.common.exceptions import TimeoutException
# 面對動態網頁，等待、了解某個元素的狀態，通常與 exptected_conditions 和 By 搭配
from selenium.webdriver.support.ui import WebDriverWait
# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC
# 期待元素出現要透過什麼方式指定，經常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By
# 取得系統時間的工具
from datetime import datetime
# 強制停止/強制等待 (程式執行期間休息一下)
from time import sleep
# 處理下拉式選單的工具
from selenium.webdriver.support.ui import Select
# 隨機取得 User-Agent
from fake_useragent import UserAgent
import os
import pandas as pd

# 建立下載路徑/資料夾，不存在就新增 (os.getcwd() 會取得當前的程式工作目錄)
folderPath = os.path.join(os.getcwd(), 'files')
if not os.path.exists(folderPath):
    os.makedirs(folderPath)
#建立股價資料夾    
folderPath1=os.path.join(os.getcwd(),'files/dailyprice')
if not os.path.exists(folderPath1):
    os.makedirs(folderPath1)    

# 啟動瀏覽器工具的選項
ua = UserAgent()
my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")                # 不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")         # 最大化視窗
my_options.add_argument("--incognito")               # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")   # 取消通知
my_options.add_argument(f'--user-agent={ua.random}') # (Optional)加入 User-Agent
#預設下載路徑 不會動態改路徑 所以先放到dailyprice 再用 shell script 搬家
my_options.add_experimental_option("prefs", {"download.default_directory": folderPath1})
# 取得最新的 WebDriver 來 match Chrome
driver = webdriver.Chrome(
    options = my_options,
    service = Service(ChromeDriverManager().install())
)
# 走訪網址stocklist=pd.read_csv('files/stocklist.csv')
url = 'https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html'
# 走訪頁面
def visit():
    driver.get(url)

# 選取下拉式選單的項目
def setDropDownMenu():
    #找到股號選單
    stockNo = driver.find_element(By.CSS_SELECTOR, 'input.stock-code-autocomplete')
    #載入所有代號
    stocklist=pd.read_csv('files/stocklist.csv',encoding='cp950',dtype=str)
    for stock_no in stocklist['證券代號']:
        #建立該股資料夾
        folderPath2=os.path.join(os.getcwd(),'files/dailyprice/%s'%stock_no)
        if not os.path.exists(folderPath2):
            os.makedirs(folderPath2)
        #按證券列表抓
        stockNo.send_keys(stock_no)
        #從100年下載到111年 要用BIG5開 
        for i in range(11):
            year='民國 %s 年'%str(i+100)
            #建立該年資料夾
            folderPath3 = os.path.join(os.getcwd(), 'files/dailyprice/%s'%stock_no+'/%s'%year)
            if not os.path.exists(folderPath3):
                os.makedirs(folderPath3)
            for j in range(1,13):
                try:
                # 強制等待
                    sleep(1)
                # 選擇 select[name="yy"] 元素，並依 option 的 innerText 來進行選取
                    yy = Select(driver.find_element(By.CSS_SELECTOR, 'div#d1 > select[name="yy"]'))
                    yy.select_by_visible_text(year)
                # 強制等待
                    sleep(1)
                # 選擇 select[name="mm"] 元素，並依 option 的 value 來進行選取
                    mm = Select(driver.find_element(By.CSS_SELECTOR, 'div#d1 > select[name="mm"]'))
                    mm.select_by_value(str(j))
                # 強制等待
                    sleep(1)
                # 強制等待
                    sleep(1)
                # 按下查詢
                    driver.find_element(
                        By.CSS_SELECTOR, 
                        'a.button.search'
                    ).click()
                # 強制等待
                    sleep(2)
                # 等待篩選元素出現
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located( (By.CSS_SELECTOR, "div.tools > a.csv")))                   
                # 下載檔案
                    webdriver.ChromeOptions().add_experimental_option("prefs", {"download.default_directory": folderPath3})
                    driver.find_element(By.CSS_SELECTOR, "div.tools > a.csv").click()        
                # 強制等待
                    sleep(2)   
                except TimeoutException:
                    print("等待逾時，即將關閉瀏覽器…")
                    driver.quit()
                except Exception as err:
                    print(str(err))
                    driver.quit() 

# 關閉瀏覽器
def close():
    driver.quit()

# 主程式 如果被匯入 這裡不會執行
if __name__ == '__main__':
    visit()
    setDropDownMenu()
    close()