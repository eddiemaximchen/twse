'''
臺灣證券交易所
即時重大訊息
https://mops.twse.com.tw/mops/web/t05sr01_1

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
# 強制停止/強制等待 (程式執行期間休息一下)
from time import sleep
# 隨機取得 User-Agent
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

ua = UserAgent()
# 啟動瀏覽器工具的選項
my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")               # 不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")         # 最大化視窗
my_options.add_argument("--incognito")               # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")   # 取消通知
my_options.add_argument(f'--user-agent={ua.random}') # (Optional)加入 User-Agent
# 取得最新的 WebDriver 來 match Chrome
driver = webdriver.Chrome(
    options = my_options,
    service = Service(ChromeDriverManager().install())
)
# 走訪網址
url = 'https://mops.twse.com.tw/mops/web/t05sr01_1'
# 走訪頁面
def visit():
    driver.get(url);

def chkinfo():
    try:
        # 強制等待
        sleep(2)

        # 等待篩選元素出現
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located( 
                (By.CSS_SELECTOR, "table.hasBorder") 
            )
        )                
        # 強制等待
        sleep(2)
        #找出公佈重大訊息的股票代號
        html = urlopen(url)
        bs = BeautifulSoup(html.read(),'html.parser')
        Alltitle=bs.find_all('tr',{'class':'even'})
        msg=""
        for title in Alltitle:
            msg=msg+title.find('td').get_text()+', '
        Alltitle=bs.find_all('tr',{'class':'odd'})
        for title in Alltitle:
            msg=msg+title.find('td').get_text()+', '
    except TimeoutException:
        print("等待逾時，即將關閉瀏覽器…")
        driver.quit()
    #發送到line
    headers={
        'Authorization':'Bearer 6wwku50yAt06aJGXNhQEuWz44fS8ojjG07Pxj2MEw1q', #line notify token
        'Content-Type':'application/x-www-form-urlencoded'
    }
    payload={'message':'個股%s'%msg+'重大訊息'}
    print(payload)
    r=requests.post('https://notify-api.line.me/api/notify',headers=headers,params=payload)
    return r.status_code
    
# 關閉瀏覽器
def close():
    driver.quit()

# 主程式 如果被匯入 這裡不會執行
if __name__ == '__main__':
    visit()
    chkinfo()
    close()
    
