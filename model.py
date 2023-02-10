import csv
import json
import pandas as pd
import requests

#指定選股起訖日期
date_from='2011-01-03'
date_to='2011-01-31'

stock_open=int(20) #1月有20個營業日
allstock=15140

#取出本益比
files=[]
ratio={}
with open('files/201101yield.csv',encoding='cp950') as file:
    csvReader=csv.DictReader(file)

    for row in csvReader:
        files.append(row)
#字典值都是字串 所以再塞入list 數字才能轉成int *一定要to_dict()才有效*
#to_dict()取出的值是錯的
ratio=pd.DataFrame(files).to_dict()
pe=[]
sum_pe=0
#取出本益比
for i in ratio['本益比']:
    pe.append(i)
for i in pe:
    sum_pe=i+sum_pe
avg_pe=sum_pe/(allstock*stock_open)
div=[]
sum_div=0
#取出殖利率
for i in ratio['殖利率']:
    div.append(i)
for i in div:
    sum_div=i+sum_div
avg_div=sum_div/(allstock*stock_open)

# 取出成交量
files1=[]
vol=[]
with open('files/market/FMTQIK_201101.csv',encoding='cp950') as file1:
    csvReader=csv.DictReader(file1)
    for row in csvReader:
        files1.append(row)
vol_dict=pd.DataFrame(files1).to_dict()
vo1=[]
sum_pe=0
for i in vol_dict['成交股數']:
    vol.append(i)
sum_vol=0
for i in vol:
    sum_vol=i+sum_vol
avg_vol=sum_vol/stock_open
#載入個股資料
stock1301=pd.read_json('files/json/stock1301.json')
stock1303=pd.read_json('files/json/stock1303.json')
stock2330=pd.read_json('files/json/stock2330.json')
stock2882=pd.read_json('files/json/stock2882.json')
stock3008=pd.read_json('files/json/stock3008.json')
#算個股資料
stock_result=[]

sum_div_1301=0
sum_deal_num_1301=0
sum_pe_1301=0
for i in stock1301:    
    sum_div_1301=sum(stock1301['yield_percent'].values)
    sum_deal_num_1301=sum(stock1301['dealnum'].values)
    sum_pe_1301=sum(stock1301['peRation'].values)
avg_div_1301=sum_div_1301/20
avg_deal_num_1301=sum_deal_num_1301/20
avg_pe_1301=sum_pe_1301/20

sum_div_1303=0
sum_deal_num_1303=0
sum_pe_1303=0
for i in stock1303:
    sum_div_1303=sum(stock1303['yield_percent'].values)
    sum_deal_num_1303=sum(stock1301['dealnum'].values)
    sum_pe_1303=sum(stock1303['peRation'].values)
avg_div_1303=sum_div_1303/20
avg_deal_num_1303=sum_deal_num_1303/20
avg_pe_1303=sum_pe_1303/20

sum_div_2330=0
sum_deal_num_2330=0
sum_pe_2330=0
for i in stock2330:
    sum_div_2330=sum(stock2330['yield_percent'].values)
    sum_deal_num_2330=sum(stock2330['dealnum'].values)
    sum_pe_2330=sum(stock2330['peRation'].values)
avg_div_2330=sum_div_2330/20
avg_deal_num_2330=sum_deal_num_2330/20
avg_pe_2330=sum_pe_2330/20

sum_div_2882=0
sum_deal_num_2882=0
sum_pe_2882=0
for i in stock2882:
    sum_div_2882=sum(stock2882['yield_percent'].values)
    sum_deal_num_2882=sum(stock2882['dealnum'].values)
    sum_pe_2882=sum(stock2882['peRation'].values)
avg_div_2882=sum_div_2882/20
avg_deal_num_2882=sum_deal_num_2882/20
avg_pe_2882=sum_pe_2882/20

sum_div_3008=0
sum_deal_num_3008=0
sum_pe_3008=0
for i in stock3008:
    sum_div_3008=sum(stock3008['yield_percent'].values)
    sum_deal_num_3008=sum(stock3008['dealnum'].values)
    sum_pe_3008=sum(stock3008['peRation'].values)
avg_div_3008=sum_div_3008/20
avg_deal_num_3008=sum_deal_num_3008/20
avg_pe_3008=sum_pe_3008/20
# 挑出殖利率大於平均的2倍 本益率大於平均的2倍 成交量大於平均成交量 
if avg_div_1301 > (avg_div) and avg_pe_1301 >(avg_pe) and avg_deal_num_1301 >avg_vol:
    stock_result.append({
        'stockNo':'1301',
        'avg_div':avg_div_1301,
        'avg_deal_num':avg_deal_num_1301
    })

if avg_div_1303 > (avg_div) and avg_pe_1303 >(avg_pe) and avg_deal_num_1303 >avg_vol:
    stock_result.append({
        'stockNo':'1303',
        'avg_div':avg_div_1303,
        'avg_deal_num':avg_deal_num_1303
    })
if avg_div_2330 > (avg_div) and avg_pe_2330 >(avg_pe) and avg_deal_num_2330 >avg_vol:
    stock_result.append({
        'stockNo':'2330',
        'avg_div':avg_div_2330,
        'avg_deal_num':avg_deal_num_2330
    })

if avg_div_2882 > (avg_div) and avg_pe_2882 >(avg_pe) and avg_deal_num_2882 >avg_vol:
    stock_result.append({
        'stockNo':'2882',
        'avg_div':avg_div_2882,
        'avg_deal_num':avg_deal_num_2882
    })

if avg_div_3008 > (avg_div) and avg_pe_3008 >(avg_pe) and avg_deal_num_3008 >avg_vol:
    stock_result.append({
        'stockNo':'3008',
        'avg_div':avg_div_3008,
        'avg_deal_num':avg_deal_num_3008
    })

#發送到line
msg="推薦個股:"
for i in stock_result:
    msg=msg+i


headers={
     'Authorization':'Bearer 6wwku50yAt06aJGXNhQEuWz44fS8ojjG07Pxj2MEw1q', #line notify token
     'Content-Type':'application/x-www-form-urlencoded'
 }
payload={'message':msg}
r=requests.post('https://notify-api.line.me/api/notify',headers=headers,params=payload)
 
