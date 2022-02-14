import csv
fp = open('淘宝直播数据_服饰.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(fp)
csv_writer.writerow(['店铺名', '粉丝数', '直播时间', '直播标题', '观看人数','直播商品数','直播间ID','直播商品','商品价格'])