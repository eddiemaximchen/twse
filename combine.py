import pandas as pd
import json
import os

stock1=[]
price= pd.read_csv('files/dailyprice/3008/STOCK_DAY_3008_201101.csv',encoding='Big5')
Yield=pd.read_csv('files/yield_3008.csv',encoding='Big5')
foreign=pd.read_csv('files/foreign3008Jan.csv',encoding='Big5')
for i in range(20):
    stock1.append({
        'date':str(price['日期'][i]),
        'dealnum':str(price['成交股數'][i]),
        'dealamt':str(price['成交金額'][i]),
        'open':str(price['開盤價'][i]),
        'max':str(price['最高價'][i]),
        'min':str(price['最低價'][i]),
        'close':str(price['收盤價'][i]),
        'diff':str(price['漲跌價差'][i]),
        'dealcount':str(price['成交筆數'][i]),
        'monthly_revenue':'1006078',
        'compare_last_year_percent':'36.7',
        'peRation':str(Yield['本益比'][i]),
        'yield_percent':str(Yield['殖利率'][i]),
        'pbr':str(Yield['股價淨值比'][i]),
        'foreign_hold_percent':str(foreign['全體外資及陸資持股比率'][i])
    })
for i in range(20):
    with open("files/json/stock3008.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(stock1, ensure_ascii=False, indent=4))
