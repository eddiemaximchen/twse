import csv
import json
import pandas as pd
#指定選股起訖日期
date_from='2011-01-03'
date_to='2011-01-31'

#指定值利率參數
div_floor=int(5)
vol_floor=int(100)
stock_open=int(20) #1月有20個營業日
allstock=970
#取出本益比
files=[]
ratio={}
with open('files/201101yield.csv',encoding='cp950') as file:
    csvReader=csv.DictReader(file)

    for row in csvReader:
        files.append(row)
df=pd.DataFrame(files)
ratio=df.to_dict()
sum_pe=sum(ratio['本益比'].values())
sum_div=sum(ratio['殖利率'].values())

ave_pe=sum_pe/allstock
avg_div=sum_div/allstock

# 取出成交量
vol=pd.read_csv('files/market/FMTQIK_201101.csv',encoding='cp950')
vol_data=[]
sum_vol=0
for i in vol:
    sum_vol=sum_vol+vol

avg_vol=sum_vol/20
#載入個股資料
stock1301=pd.read_json('files/json/stock1301.json')
stock1303=pd.read_json('files/json/stock1303.json')
stock2330=pd.read_json('files/json/stock2330.json')
stock2882=pd.read_json('files/json/stock2882.json')
stock3008=pd.read_json('files/json/stock3008')
# 挑出殖利率大於5%的股票 捨去月均量太小的股票 
vol_share_floor=vol_floor*1000
stock_result=[]

for i in stock1301:
    sum_div_1301=float(sum_div_1301)+float(stock1301['yield_percent'])
    sum_deal_num_1301=int(sum_deal_num_1301)+int(stock1301['dealnum'])
avg_div_1301=sum_div_1301/20
avg_deal_num_1301=sum_deal_num_1301/20

for i in stock1303:
    sum_div_1303=float(sum_div_1303)+float(stock1303['yield_percent'])
    sum_deal_num_1303=sum_deal_num_1303+stock1301['dealnum']
avg_div_1303=sum_div_1303/20
avg_deal_num_1303=sum_deal_num_1303/20

for i in stock2330:
    sum_div_2330=float(sum_div_2330)+float(stock2330['yield_percent'])
    sum_deal_num_2330=sum_deal_num_2330+stock1301['dealnum']
avg_div_2330=sum_div_2330/20
avg_deal_num_2330=sum_deal_num_2330/20


for i in stock2882:
    sum_div_2882=float(sum_div_2882)+float(stock2882['yield_percent'])
    sum_deal_num_2882=sum_deal_num_2882+stock1301['dealnum']
avg_div_2882=sum_div_2882/20
avg_deal_num_2882=sum_deal_num_2882/20


for i in stock3008:
    sum_div_3008=float(sum_div_3008)+float(stock3008['yield_percent'])
    sum_deal_num_3008=sum_deal_num_3008+stock3008['dealnum']
avg_div_3008=sum_div_3008/20
avg_deal_num_3008=sum_deal_num_3008/20
if avg_div_1301 >5 and avg_deal_num_1301 >vol_share_floor:
    stock_result.append({
        'stockNo':'1301',
        'avg_div':'avg_div_1301',
            'avg_deal_num':'avg_deal_num_1301'
    })

if avg_div_1301 >5 and avg_deal_num_1301 >vol_share_floor:
    stock_result.append({
        'stockNo':'1301',
        'avg_div':'avg_div_1301',
            'avg_deal_num':'avg_deal_num_1301'
    })

if avg_div_1303 >5 and avg_deal_num_1303 >vol_share_floor:
    stock_result.append({
        'stockNo':'1303',
        'avg_div':'avg_div_1303',
            'avg_deal_num':'avg_deal_num_1303'
    })

if avg_div_2330 >5 and avg_deal_num_2330 >vol_share_floor:
    stock_result.append({
        'stockNo':'2330',
        'avg_div':'avg_div_2330',
            'avg_deal_num':'avg_deal_num_2330'
    })

if avg_div_2882 >5 and avg_deal_num_2882 >vol_share_floor:
    stock_result.append({
        'stockNo':'2882',
        'avg_div':'avg_div_2882',
            'avg_deal_num':'avg_deal_num_2882'
    })
if avg_div_3008 >5 and avg_deal_num_3008 >vol_share_floor:
    stock_result.append({
        'stockNo':'3008',
        'avg_div':'avg_div_3008',
            'avg_deal_num':'avg_deal_num_3008'
    })

#得到最終結果
print(stock_result)

