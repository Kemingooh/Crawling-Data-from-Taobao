from selenium import webdriver
import time
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains
import csv
wd = webdriver.Chrome('chromedriver.exe') # 数码店铺
wd.implicitly_wait(10)
# url = "https://shopsearch.taobao.com/browse/shop_search.htm?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=shop&ssid=s5-e&commend=all&imgfile=&q=%E6%95%B0%E7%A0%81&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest&s=0"
url = "https://shopsearch.taobao.com/browse/shop_search.htm?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=shop&ssid=s5-e&commend=all&imgfile=&q=%E6%95%B0%E7%A0%81&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest&isb=0&shop_type=&ratesum=&s=0"
wd.get(url)
time.sleep(2)
# 扫码登录
wd.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()
time.sleep(5)
# 选择店铺类型选择
'''wd.find_element_by_xpath('//*[@id="J_relative"]/div[1]/div/div/div[1]/div/div[1]/span[1]').click()
wd.find_element_by_xpath('//*[@id="J_relative"]/div[1]/div/div/div[1]/div/div[2]/div/a[1]').click()
time.sleep(2)'''

def login_page(number):
    """店铺页面"""
    js = "window.scrollBy(0,500)"
    for i in range(10):
        wd.execute_script(js)
        time.sleep(1)
    page_data = wd.page_source
    return page_data


def shop_url(page_data):
    """店铺链接爬取"""
    urls = []
    data = []
    page_data = page_data
    html = etree.HTML(page_data)
    shop_ulrs = html.xpath('//h4//a[@trace="shop"][1]/@href')

    #店铺链接处理
    for i in range (len(shop_ulrs)):
        url = "https:"+shop_ulrs[i]
        urls.append(url)
    # print(urls)
    return urls


def handle_data_1(page_data):# 在首页中爬取好评率，店铺名称，（地址不太会处理），店铺皇冠等级
    shops = []
    good_rates = []
    ranks =[]
    page_data = page_data
    html = etree.HTML(page_data)
    shops_s = html.xpath('//h4//a[@trace="shop"][1]/text()')
    good_rate_s = html.xpath('//div[@class="valuation clearfix"]/div[@class="good-comt"]/text()')
    # address = html.xpath('//p[@class="shop-info"]//span[@class="shop-address"]/text()')
    rank = html.xpath('//div[@class="m-shoplist"]//h4/a[2]/@class')
    #店铺名称处理
    for i in range(len(shops_s)):
        temporarily = shops_s[i].replace("\n","")
        temporarily = temporarily.strip()
        shops.append(temporarily)

    #店铺好评率处理
    for i in range(len(good_rate_s)):
        temporarily = good_rate_s[i].replace("好评率: ","")
        good_rates.append(temporarily)

    # 店铺皇冠等级处理
    for i in range(len(rank)):
        temporarily = rank[i].replace("rank seller-rank-", "")
        ranks.append(temporarily)
    return shops, good_rates ,ranks




def handle_data_2(url):# 在店铺详情页内爬取数据
    '''describe_scores = [] # 描述评分
    service_scores = []  # 服务评分
    logistics_scores = [] #物流评分
    opening_time = [] # 开店时间
    rank = [] #皇冠等级
    gold = [] # 是否通过金牌卖家认证
    consumer_guarantee = [] #是否有消费者保障协议'''
    wd.get(url)
    time.sleep(2)
    page = wd.page_source
    html = etree.HTML(page)
    '''describe_scores = html.xpath('//a[@data-goldlog-id="/tbwmdd.1.047"]/span[@class="dsr-num red"][1]/text()')
    service_scores = html.xpath('//a[@data-goldlog-id="/tbwmdd.1.047"]/span[@class="dsr-num red"][2]/text()')'''
    scores = html.xpath('//em[@class="count"]/text()')
    gold = html.xpath('//span[@class="qualification"]/a[@class="J_TGoldlog jinpai-v"]')
    consumer_guarantee = html.xpath('//span[@class="qualification"]/a[@class="J_TGoldlog"]')
    # hover_element = wd.find_element_by_xpath("//i[@id='J_TEnterShop']")
    # ActionChains(wd).move_to_element(hover_element).perform()
    opening_time = html.xpath('//span[@class="id-time J_id_time"]/text()')
    describe_scores = scores[0]
    service_scores = scores[1]
    logistics_scores =scores[2]
    if len(opening_time) == 0:
        opening_time.append(0)
    if len(gold) == 0:
        gold.append(0)
    else:
        gold = []
        gold.append(1)
    if len(consumer_guarantee) == 0:
        consumer_guarantee.append(0)
    else:
        consumer_guarantee = []
        consumer_guarantee.append(1)

    print(describe_scores, service_scores, logistics_scores,opening_time,gold,consumer_guarantee)
    return describe_scores, service_scores, logistics_scores, opening_time, gold, consumer_guarantee


def change_page():
    """切换到下一页"""
    js = "window.scrollBy(0,500)"
    try:
        for i in range(5):
            wd.execute_script(js)
            time.sleep(1)
        wd.find_element_by_xpath('//*[@id="shopsearch-pager"]/div/div/div/ul/li[8]/a/span[1]').click()
    except:


        wd.find_element_by_xpath('//*[@id="shopsearch-pager"]/div/div/div/div[2]/span[3]').click()


if __name__ == '__main__':
    fp = open('../../WeChat Files/wxid_v7nq72jwkmqz22/FileStorage/Fav/Temp/87e3c89f/res/淘宝店铺信息(full).csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(fp)
    csv_writer.writerow(['淘宝店铺名称', '淘宝店铺链接', '淘宝皇冠等级', '好评率', '描述评分', '服务评分', '物流评分', '开店时间', '是否有金牌认证', '是否有消费者协议'])
    for x in range(99):
        page_data = login_page(x)
        s= str(20*x)
        url ="https://shopsearch.taobao.com/browse/shop_search.htm?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=shop&ssid=s5-e&commend=all&imgfile=&q=%E6%95%B0%E7%A0%81&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest&isb=0&shop_type=&ratesum=&s=" + s
        urls = shop_url(page_data)
        shops, good_rates, ranks = handle_data_1(page_data)
        for i in range(0, len(urls)):
            describe_scores, service_scores, logistics_scores, opening_time, gold, consumer_guarantee = handle_data_2(urls[i])
            data = []
            data.append(shops[i])
            data.append(urls[i])
            data.append(ranks[i])
            data.append(good_rates[i])
            data.append(describe_scores)
            data.append(service_scores)
            data.append(logistics_scores)
            data.append(opening_time[0])
            data.append(gold[0])
            data.append(consumer_guarantee[0])
            csv_writer.writerow(data)
            data = []
            '''except:
                print("页面缺少开店信息")'''
        wd.get(url)  # 返回首页
        change_page()