import pandas as pd
import json
import os

month1=[]
price1303= pd.read_csv('files/dailyprice/1303/STOCK_DAY_1303_201101.csv',encoding='Big5',header=1)
price2330= pd.read_csv('files/dailyprice/2330/STOCK_DAY_2330_201101.csv',encoding='Big5',header=1)
yield1303=pd.read_csv('files/yield_1303.csv',encoding='Big5')
yield2330=pd.read_csv('files/yield_2330.csv',encoding='Big5')
foreign1303=pd.read_csv('files/foreign1303Jan.csv',encoding='Big5')
foreign2330=pd.read_csv('files/foreign2330Jan.csv',encoding='Big5')
for i in range(20):
    month1.append({
        'date':price1303['日期'][i],
        'dealnum_1303':price1303['成交股數'][i],
        'dealamt_1303':price1303['成交金額'][i],
        'open_1303':price1303['開盤價'][i],
        'max_1303':price1303['最高價'][i],
        'min_1303':price1303['最低價'][i],
        'close_1303':price1303['收盤價'][i],
        'diff_1303':price1303['漲跌價差'][i],
        'dealcount_1303':price1303['成交筆數'][i],
        'monthly_revenue_1303':'19407090',
        'compare_last_year_percent_1303':'-0.5',
        'peRation_1303':yield1303['本益比'][i],
        'yield_percent_1303':yield1303['殖利率'][i],
        'pbr_1303':yield1303['股價淨值比'][i],
        'foreign_hold_percent_1303':foreign1303['全體外資及陸資持股比率'][i],
        'dealnum_2330':price2330['成交股數'][i],
        'dealamt_2330':price2330['成交金額'][i],
        'open_2330':price2330['開盤價'][i],
        'max_2330':price2330['最高價'][i],
        'min_2330':price2330['最低價'][i],
        'close_2330':price2330['收盤價'][i],
        'diff_2330':price2330['漲跌價差'][i],
        'dealcount_2330':price2330['成交筆數'][i],
        'monthly_revenue_2330':'34424173',
        'compare_last_year_percent_2330':'15.3',
        'peRation_2330':yield2330['本益比'][i],
        'yield_percent_2330':yield2330['殖利率'][i],
        'pbr_1303':yield2330['股價淨值比'][i],
        'foreign_hold_percent_2330':foreign2330['全體外資及陸資持股比率'][i]
    })
for i in range(20):
    with open("files/json/201101.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(month1, ensure_ascii=False, indent=4))