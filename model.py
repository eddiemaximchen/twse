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
ratio=[]
file=open('files/201101yield.csv','r',encoding='cp950')
lines=file.readlines()
file.close()
list1=[]
list2=[]
list3=[]
#get 本益比
sum_pe=0
for i in lines:
    list1=i.split(',')
    list2.append(list1[4])
    list3.append(list1[5])
del list2[0]
del list3[0]
pe=[float(list) for list in list2] #從字串改成浮點數
div=[float(list) for list in list3]
for i in pe:
    sum_pe=sum_pe+i
avg_pe=sum_pe/allstock

sum_div=0
#get 殖利率 
for i in div:
    sum_div=sum_div+i
avg_div=sum_div/allstock
#留下嘗試紀錄
# with open('files/201101yield.csv',encoding='cp950') as file:
    # csvReader=csv.DictReader(file)
# 
    # every record is a dictory
    # for row in csvReader:
        # ratio.append({
            # '日期':row['日期'],
            # '證券代號':row['證券代號'],
            # '本益比':row['本益比'],
            # '殖利率':row['殖利率']
# 
        # })
# for i in range(15140):
    # with open("files/json/ration.json", "w", encoding="utf-8") as file:
        # file.write(json.dumps(ratio, ensure_ascii=False, indent=4))
#字典值都是字串 所以再塞入list 數字才能轉成int *一定要to_dict()才有效*
#to_dict()取出的值是錯的
#sum(.values)==>TypeError: unsupported operand type(s) for +: 'int' and 'str'
#ratio=pd.DataFrame(files).to_json(force_ascii=False)值亂了
#兩層中括弧去不掉
# ratio=pd.DataFrame(files).values.tolist()

#載入個股資料
stock1301=pd.read_json('files/json/stock1301.json')
stock1303=pd.read_json('files/json/stock1303.json')
stock2330=pd.read_json('files/json/stock2330.json')
stock2882=pd.read_json('files/json/stock2882.json')
stock3008=pd.read_json('files/json/stock3008.json')
#算個股資料

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

# 挑出殖利率大於平均 本益比大於平均 
stock_result=''
if avg_div_1301 > (avg_div) and avg_pe_1301 >(avg_pe):
    stock_result=stock_result+'1301,'

if avg_div_1303 > (avg_div) and avg_pe_1303 >(avg_pe):
    stock_result=stock_result+'1303,'
if avg_div_2330 > (avg_div) and avg_pe_2330 >(avg_pe):
    stock_result=stock_result+'2330,'

if avg_div_2882 > (avg_div) and avg_pe_2882 >(avg_pe):
    stock_result=stock_result+'2882,'

if avg_div_3008 > (avg_div) and avg_pe_3008 >(avg_pe):
    stock_result=stock_result+'3008,'

#發送到line
msg='推薦個股'+stock_result+'殖利率&本益比均高於市場平均'


headers={
     'Authorization':'Bearer 6wwku50yAt06aJGXNhQEuWz44fS8ojjG07Pxj2MEw1q', #line notify token
     'Content-Type':'application/x-www-form-urlencoded'
 }
payload={'message':msg}
r=requests.post('https://notify-api.line.me/api/notify',headers=headers,params=payload)
 
