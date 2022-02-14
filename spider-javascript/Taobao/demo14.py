import pandas as pd
import csv
df = pd.read_csv('淘宝店铺信息(full)（数码）(1).csv')
shop_list = list(df['淘宝店铺名称'])
#print(shop_list)
temp_list = []
temp = []
with open('抓取的店铺.txt','r',encoding='utf-8') as fp:
    for line in fp:
        temp_list.append(line.replace('\n',''))

#集合的差集
list_3 = list(set(shop_list)-set(temp_list))
print(list_3)
fp = open('未抓取的店铺.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(fp)
csv_writer.writerow(['淘宝店铺名称'])
# csv_writer.writerow(['轻风数码工作室'])
for i in range(len(list_3)):
    temp.append(list_3[i])
    csv_writer.writerow(temp)
    temp = []