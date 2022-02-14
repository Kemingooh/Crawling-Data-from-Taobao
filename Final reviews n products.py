from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import re
from urllib import parse
import time
import csv
import numpy as np


chromeOpts = webdriver.ChromeOptions()
chromeOpts.binary_location = r'c:\tools\chrome-win\chrome.exe'
driver = webdriver.Chrome(r'c:\tools\chromedriver.exe', options=chromeOpts)

#driver = webdriver.Chrome()
wait = WebDriverWait(driver,30)
upload_url = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.1fda11d9BYSdoS&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F%3Fspm%3Da230r.1.1581860521.1.4b0745f5cMecQZ'
driver.get(upload_url)
input('Press Enter after you have logined:')
baseurl = 'https://shop136098903.taobao.com'
data = open('pro_data.csv', 'w', encoding='gbk')
writer = csv.writer(data)

def get_page(baseurl):
    products = np.array(['name', 'oprice', 'cprice', 'sellcounter', 'start_from', 'popularity'])
    driver.get(baseurl)
    time.sleep(2)
    try:
        link = driver.find_element_by_css_selector('#hd div.all-cats-trigger.popup-trigger a')
        url_next = link.get_attribute('href')
    except:
        print('error')
    driver.get(url_next)  # 转入所有宝贝板块
    time.sleep(2)
    html = driver.page_source # 网页源代码
    get_product(html,products)

def get_product(html,products):

    doc=pq(html)
    divs=doc('#J_ShopSearchResult div.item3line1').items() # 遍历所有的块，一行一个块
    for div in divs:
        dls=div('dl').items() # 在每个块中取出产品
        for dl in dls:
            goods_url=dl.find('dd.detail a').attr('href')
            goods_url="https:"+goods_url
            driver.get(goods_url)
            time.sleep(2)
            html_pro = driver.page_source
            doc2 = pq(html_pro)
            divs2 = doc2('#detail div.tb-item-info.tb-clear')
            name = divs2.find('h3.tb-main-title').text()
            oprice = divs2.find('strong#J_StrPrice em.tb-rmb-num').text()
            cprice = divs2.find('em#J_PromoPriceNum.tb-rmb-num').text()
            sellcounter = divs2.find('strong#J_SellCounter').text()
            start_from = divs2.find('span#J-From').text()
            popularity = divs2.find('em.J_FavCount').text()
            product=[name,oprice,cprice,sellcounter,start_from,popularity]
            print(product)
            reviews = get_comment(goods_url)
            writer.writerow(product)
            writer.writerow(reviews)
            

    next_url = doc('#J_ShopSearchResult div.pagination.pagination-mini a')
    i = 0
    for item in next_url.items():
        if i == 1:
          if item.attr('href') is None : return
          else: driver.get('http:' + item.attr('href'))
        else: i = i +1
    time.sleep(2)
    next_page = driver.page_source
    get_product(next_page, products)

def get_comment(goods_url):
    reviews = []
    final_date=input('give me the final date(eg:202007)')
    final_date=int(final_date)
    flag=True
    try:
        driver.get(goods_url)
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TabBar > li:nth-child(2) > a')))
        button.click()
        wait.until(EC.presence_of_element_located((By.ID,'reviews')))
    except:
        print('failed')
    html_pro = driver.page_source
    doc2 = pq(html_pro)
    pgs=doc2('#reviews div.tb-revbd div.kg-pagination2 li').items()
    while(check_it_clickable(html_pro) and flag==True):
        doc2 = pq(html_pro)
        lis = doc2('#reviews div.tb-revbd li.J_KgRate_ReviewItem').items()
        for li in lis:
            review = li.find('div.J_KgRate_ReviewContent').text()
            review = "".join(review.split())
            date = li.find('div.tb-r-info span').text()
            date1 = re.sub('[年月日]','',date)
            date1 = int(date1[:6])
            style = li.find('div.tb-r-info').text()
            style = "".join(style.split())
            flag1,add_review=check_add(li)
            print(add_review)
            if flag1 == True:
                review=review+' '+add_review
            if date1 < final_date:
                flag=False
                break
            if review == "评价方未及时做出评价,系统默认好评!" or review == "此用户没有填写评价。":
                continue
            reviews.append(review, date, style)
        print(reviews)
        next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#reviews div.kg-pagination2 li.pg-next')))
        next_button.click()
        time.sleep(2)
    return reviews

def check_it_clickable(html1):
    html_pro = driver.page_source
    doc2=pq(html_pro)
    button_statue=doc2.find('#reviews div.kg-pagination2 li.pg-next').attr('class')
    if button_statue=='pg-next pg-disabled':
        flag=False
    else:
        flag=True
    return flag

#检测是否有追加评论，感觉有点问题

def check_add(li):
    flag = True
    try:
        tag = li.find('div.tv-rev-item-append div.J_KgRate_ReviewContent').text()
        return flag, tag
    except:
        flag = False
        tag = 0
        return flag, tag

get_page(baseurl)
data.close()
print('finished!')