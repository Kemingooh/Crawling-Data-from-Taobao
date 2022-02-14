from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time
import os
import re
import csv
import pandas as pd
"""
重要参数说明：
1、data_time_title   #存储直播时间和直播标题
2、data_shop_list  #存储店铺名字和粉丝数
"""

"""
前置代码，打开淘宝，进入微淘界面
"""
data_time_title = []
desired_caps = {
    'platformName': 'Android',  # 被测手机是安卓
    'platformVersion': '9',  # 手机安卓版本
    'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
    'appPackage': 'com.taobao.taobao',  # 启动APP Package名称
    'appActivity': 'com.taobao.tao.TBMainActivity',  # 启动Activity名称
    'unicodeKeyboard': False,  # 使用自带输入法，输入中文时填True
    'resetKeyboard': True,  # 执行完程序恢复原来输入法
    'noReset': True,  # 不要重置App
    'newCommandTimeout': 6000,
    'automationName': 'UiAutomator2'
}

# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# 设置缺省等待时间
driver.implicitly_wait(20)
# 点击微淘按钮
weitao = driver.find_element_by_xpath('//android.widget.FrameLayout[@content-desc="微淘"]/android.widget.ImageView')
weitao.click()
time.sleep(1)


def find_index(src_list, target):
    """在给定集合中寻找目标所在索引"""

    # 用来存储目标索引的列表
    dst_index_list = []

    # 在给定集合中挨个比对，若与目标匹配，保留索引
    for index in range(len(src_list)):
        if (src_list[index] == target):
            dst_index_list.append(index)

    # 返回目标索引列表
    return dst_index_list
def re_fun(shop_data_list):
    """正则提取直播日期和标题"""
    date_pat = '(\d{1,2}月\d{1,2}日 .*)'
    shop_pat = '(\s{1,10}.*)'
    date_list = []
    title_list = []
    for i in range(len(shop_data_list)):
        ret = re.match(date_pat, shop_data_list[i])
        try:
            date_list.append(ret.group())
        except:
            pass
    for i in range(len(shop_data_list)):
        ret = re.match(shop_pat, shop_data_list[i])
        try:
            title_list.append(ret.group())
        except:
            pass
    return date_list, title_list
def save_shop_csv(data):
    """存储数据到csv中
    1.淘宝店铺名_粉丝数"""
    fp = open('淘宝直播数据_服饰.csv', 'a', encoding='utf-8', newline='')
    csv_writer = csv.writer(fp)
    for i in range(4):
        data.append('0')
    csv_writer.writerow(data)
    fp.close()
def save_page1_csv(shop_data,page_data1,title_data1,watch1,ID1,shop_number1,shops1,shops2):
    """1.淘宝店铺名和粉丝数量(data)
    2.存储时间和直播标题(data1,data2)"""

    fp = open('淘宝直播数据_服饰.csv', 'a', encoding='utf-8', newline='')
    csv_writer = csv.writer(fp)
    # try:
        # for i in range(len(data1)):
    temp_data = []
    try:
        temp_data.append(shop_data[0])
        temp_data.append(shop_data[1])
        temp_data.append(page_data1)
        temp_data.append(title_data1)
        temp_data.append(watch1)
        temp_data.append(ID1)
        temp_data.append(shop_number1)
        temp_data.append(shops1)
        temp_data.append(shops2)
        csv_writer.writerow(temp_data)
    except:
        print("存储出错1")
    # except:
    #     print("存储出错2")
    fp.close()

def scroll_fun(scroll_list):
    """根据列表中的值，根据首元素和末尾元素"""
    try:
        code_scroll_origin = 'new UiSelector().className("android.view.View").description("{}")'.format(scroll_list[0])
        code_scroll_des = 'new UiSelector().className("android.view.View").description("{}")'.format(scroll_list[len(scroll_list)-1])
        code_scroll_origin_ele = driver.find_element_by_android_uiautomator(code_scroll_origin)
        code_scroll_des_ele = driver.find_element_by_android_uiautomator(code_scroll_des)
        driver.drag_and_drop(code_scroll_des_ele, code_scroll_origin_ele)
    except:
        print("滑动部分出错")
        driver.swipe(start_x=176, start_y=1801, end_x=176, end_y=344, duration=500)
def scroll_fun2(scroll_list):

    """(爬取商品详细列表)根据列表中的值，根据首元素和末尾元素"""
    try:
        code_scroll_origin = 'new UiSelector().className("android.view.View").description("{}")'.format(str(scroll_list[0]))
        code_scroll_des = 'new UiSelector().className("android.view.View").description("{}")'.format(str(scroll_list[1]))
        code_scroll_origin_ele = driver.find_element_by_android_uiautomator(code_scroll_origin)
        code_scroll_des_ele = driver.find_element_by_android_uiautomator(code_scroll_des)
        driver.drag_and_drop(code_scroll_des_ele, code_scroll_origin_ele)
    except:
        print("第二部分滑动函数出错")
def handle_data4(a):
    """对数据第四次处理
    1.去除一些元
    2.去除分享抢卷
    3.去除满减"""
    while '元' in a:
        a.remove('元')
    while '分享抢券' in a:
        a.remove('分享抢券')
    pat1 = '(每\d{1,10}减\d{1,5})|(满\d{1,10}减\d{1,5})|(淘金币抵.*)'
    pat2 = '(满\d{1,10}减\d{1,5})'
    temp = []

    for i in range(len(a)):
        ret1 = re.match(pat1, a[i])
        try:
            temp.append(ret1.group())
        except:
            pass
    ret = []
    for i in a:
        if i not in temp:
            ret.append(i)
    return ret
def handle_page3_data(data_list):
    """第三页的数据处理，并返回数据
    1.shop_price_list  商品价格列表
    2.shop_title 商品标题列表"""
    while None in data_list:
        data_list.remove(None)
    while '马上抢' in data_list:
        data_list.remove('马上抢')
    shop_price_list = []
    shop_price_pat = '(¥.*)'

    for i in range(len(data_list)):
        ret = re.match(shop_price_pat, data_list[i])
        try:
            shop_price_list.append(ret.group())
            # print(ret.group())
        except:
            pass
    # print(shop_price_list)
    for i in range(len(shop_price_list)):
        index_list = find_index(data_list, shop_price_list[i])

    shop_title = []
    for i in range(len(index_list)):
        shop_title.append(data_list[index_list[i] - 1])

    return shop_title,shop_price_list
def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
def handle_page3_data2(data_list):
    """第三页的数据处理，并返回数据(含有中文的判断方法)
    1.shop_price_list  商品价格列表
    2.shop_title 商品标题列表"""
    while None in data_list:
        data_list.remove(None)
    while '马上抢' in data_list:
        data_list.remove('马上抢')
    shop_price_list = []
    shop_title = []
    shop_price_pat = '(¥.*)'

    for i in range(len(data_list)):
        ret = re.match(shop_price_pat, data_list[i])
        try:
            shop_price_list.append(ret.group())
            # print(ret.group())
        except:
            pass
    for i in range(len(data_list)):
        if (is_contain_chinese(data_list[i])):
            shop_title.append(data_list[i])
    shop_title = handle_data4(shop_title)
    return shop_title,shop_price_list

def turnPage(shop_num):
    """翻页数组，返回翻页的数组"""
    a = []
    b = int(shop_num)
    a.append(b)
    while b > 2:
        b = b - 2
        a.append(b)
    s = []
    ss = []
    for i in range(len(a)):
        s.append(a[i])
        try:
            s.append(a[i + 1])
        except:
            pass
        ss.append(s)
        s = []
    #判断最后一个嵌套数组的长度
    if len(ss[len(ss)-1]) == 1:
        ss.pop()
    return ss
def page3_data(shop_number_rec):
    """第三个页面的数据
    1,shop_list存储商品标题数据"""
    print("*"*30)
    print("进入第三个界面")
    print("*"*30)
    # shops_list = []
    temp_shops_list = []
    # eles = driver.find_elements_by_class_name('android.view.View')
    # for ele in eles:
    #     shop_title = ele.get_attribute('content-desc')
    #     temp_shops_list.append(shop_title)
    # s = handle_page3_data(temp_shops_list)
    # print(s[0])
    # print(s[1])
    # scroll_fun(s[0])
    time.sleep(2)
    #接受商品数量，由商品数量来判断滑动次数
    # for i in range(4):
    #     eles = driver.find_elements_by_class_name('android.view.View')
    #     for ele in eles:
    #         shop_title = ele.get_attribute('content-desc')
    #         temp_shops_list.append(shop_title)
    #     s1 = handle_page3_data(temp_shops_list)
    #     print(s1[0])
    #     print(s1[1])
    #     scroll_fun(s1[0])
    # turnPage_list = turnPage(shop_number_rec)
    # for i in range(len(temp_shops_list)):
    #
    #     eles = driver.find_elements_by_class_name('android.view.View')
    #     for ele in eles:
    #         shop_title = ele.get_attribute('content-desc')
    #         temp_shops_list.append(shop_title)
    #     s = handle_page3_data(temp_shops_list)
    #     print(s[0])
    #     print(s[1])
    #     scroll_fun2(turnPage_list[i])
    # for i in range(10):
    #     driver.swipe(start_x=970, start_y=2016, end_x=970, end_y=549, duration=1000)
    #     time.sleep(1)
        # eles = driver.find_elements_by_class_name('android.view.View')
        # for ele in eles:
        #     shop_title = ele.get_attribute('content-desc')
        #     #print(shop_title)
        #     temp_shops_list.append(shop_title)
    # eles = driver.find_elements_by_class_name('android.view.View')
    # for ele in eles:
    #     shop_title = ele.get_attribute('content-desc')
    #     # print(shop_title)
    #     temp_shops_list.append(shop_title)
    # print(temp_shops_list)
        # print(temp_shops_list)
        # s = handle_page3_data(temp_shops_list)
        # print(s[0])
        # print(s[1])
    """
    获取商品的标题和商品的价格
    """
    shop_title_list = []
    shop_price_list = []
    flag = True
    print("抓取 第三个页面数据")
    try:
        eles = driver.find_elements_by_class_name('android.view.View')
        for ele in eles:
            shop_title = ele.get_attribute('content-desc')
            temp_shops_list.append(shop_title)
        print(temp_shops_list)
        s = handle_page3_data2(temp_shops_list)
        temp_shops_list = []
        # print(s[0])
        # print(s[1])
        shop_title_list.append(s[1])
        shop_title_list.append(s[0])
        scroll_fun(s[0])
    except:
        print("第三个页面抓取失败了")
        eles = driver.find_elements_by_class_name('android.view.View')
        for ele in eles:
            shop_title = ele.get_attribute('content-desc')
            temp_shops_list.append(shop_title)
        print(temp_shops_list)
        s = handle_page3_data2(temp_shops_list)
        temp_shops_list = []
        shop_title_list.append(s[1])
        shop_title_list.append(s[0])
        scroll_fun(s[0])

    #判断商品结束条件
    count  = 0
    temp_list = []
    while len(turnPage(shop_number_rec))>count:
        # count += 1
        eles = driver.find_elements_by_class_name('android.view.View')
        for ele in eles:
            shop_title = ele.get_attribute('content-desc')
            temp_shops_list.append(shop_title)
        s = handle_page3_data2(temp_shops_list)
        print(s[0])
        print(s[1])
        temp_shops_list = []
        shop_title_list.append(s[0])
        shop_price_list.append(s[1])
        # if count % 2 == 0:
        # temp_list.append(s[0])
        # temp_list = temp_list[3:]
        # if ( operator.eq(temp_list,s[0]) ):
        #     flag = False
        # else:
        #     shop_title_list.append(s[0])
        #     shop_price_list.append(s[1])
        #     scroll_fun(s[0])
        #
        #
        # print(s[0])
        # print(s[1])
        # if(flag):
        #     print("继续爬")
        #     scroll_fun(s[0])
        # else:
        #     print("到底了")
        #     break
        scroll_fun(s[0])

        count +=1
    print("商品爬取结束")
    return shop_title_list,shop_price_list




def page2_click(shop_data,page_data,title_data):
    """进入第二个界面
    1.进入第二个界面二获取观看人数和商品数量
    2.点击进入第三个界面"""
    print("*"*30)
    print("进入第二个界面")
    print("*"*30)
    for i in range(len(page_data)):
        code ='new UiSelector().className("android.view.View").description("{}")'.format(page_data[i])
        ele = driver.find_element_by_android_uiautomator(code)
        ele.click()
        time.sleep(2)
        #进入直播，点击暂停
        # driver.find_element_by_id('com.taobao.taobao:id/taolive_video_enter_btn').click()
        TouchAction(driver).wait(5000).tap(x=97, y=1974, count=1).perform()

        #获取观看人数
        watch_ele = driver.find_element_by_id('com.taobao.taobao:id/taolive_topbar_watch_num')
        watch = watch_ele.text
        print(watch)

        #获取淘宝直播间ID
        ID_ele = driver.find_element_by_id('com.taobao.taobao:id/taolive_room_watermark_text')
        ID = ID_ele.text
        print(ID)

        #获取直播的商品数量
        shops_ele = driver.find_element_by_id('com.taobao.taobao:id/taolive_product_switch_btn_text')
        shop_number = shops_ele.text
        print(shop_number)
        shops_ele.click()


        time.sleep(2)
        #进入第三个界面
        shops = page3_data(shop_number)
        save_page1_csv(shop_data, page_data[i], title_data[i], watch, ID, shop_number, shops[0], shops[1])
        #模拟返回键

        driver.press_keycode(4)
        driver.press_keycode(4)

def scroll_data(shop_data):
    """滑动时抓取直播日期和直播标题"""
    flag = 0
    sum_time_title_list = []  # 滑动页面时抓取时间和标题信息
    temp_date_list = []
    time.sleep(3)
    eles = driver.find_elements_by_class_name('android.view.View')
    for ele in eles:
        sum_time_title_list.append(ele.get_attribute('content-desc'))
    while '' in sum_time_title_list:
        sum_time_title_list.remove('')
    # print(sum_time_title_list)
    # temp_index = find_index(sum_time_title_list, "回放")
    # print(temp_index)
    # del temp_index[0]
    # for i in range(len(temp_index)):
    #     temp_date_list.append(sum_time_title_list[temp_index[i] - 2])
    #     temp_date_list.append(sum_time_title_list[temp_index[i] + 1].strip())
    # num = sum_time_title_list.index("搜索店内宝贝")
    # if sum_time_title_list[num - 3] == "0":
    #     temp_date_list.append(sum_time_title_list[num - 2])
    # else:
    #     temp_date_list.append(sum_time_title_list[num - 3])
    # temp_date_list.append(sum_time_title_list[num - 1].strip())
    while None in sum_time_title_list:
        sum_time_title_list.remove(None)
    print("*"*30)
    print("滑动界面")
    print(sum_time_title_list)
    data_list = re_fun(sum_time_title_list)
    # save_page1_csv(shop_data,data_list[0],data_list[1])
    #传递店铺和直播数据
    page2_click(shop_data,data_list[0],data_list[1])
    scroll_fun(data_list[0])
    print(data_list[0])
    print(data_list[1])
    data_time_title.extend(data_list[1])
    if sum_time_title_list.count('到底了') !=0 :
        flag = 1
        return temp_date_list,flag


    return temp_date_list,flag


def shop_page(shop_name):
    """1、进入店铺页面
    2、进入微淘直播
    3、返回第一张图的相关信息
    4、sum_pag1_data得到一个总的列表数据"""
    sum_pag1_data = []
    temp_data_shop_list = []
    data_shop_list = []
    # 点击搜索
    search_element = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="끽"]')
    search_element.click()
    time.sleep(1)
    search_input = driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
    search_input.click()
    #shop_name = '美美大码服饰'
    shop_shell = "adb shell am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(shop_name)
    os.system(shop_shell)
    # 点击搜索按钮，进入店铺详情页
    time.sleep(3)
    search_button = driver.find_element_by_xpath('//android.view.View[@content-desc="搜索"]').click()
    time.sleep(1)
    TouchAction(driver).wait(2000).tap(x=281, y=573, count=1).perform()

    # 店铺页面，转到微淘直播
    time.sleep(5)  # 由于网络原因页面存在加载时间
    try:
        code = 'new UiSelector().text("店铺微淘").className("android.view.View")'
        ele = driver.find_element_by_android_uiautomator(code)
        ele.click()
    except:
        code = 'new UiSelector().text("店铺微淘").className("android.view.View")'
        ele = driver.find_element_by_android_uiautomator(code)
        ele.click()

    time.sleep(5)  # 由于网络原因页面存在加载时间
    try:
        live_broadcast_ele = driver.find_element_by_xpath('//android.view.View[@content-desc="直播"]')
        live_broadcast_ele.click()
        time.sleep(3)
        eles = driver.find_elements_by_class_name('android.view.View')
        for ele in eles:
            sum_pag1_data.append(ele.get_attribute('content-desc'))
            temp_data_shop_list.append(ele.text)
        while None in sum_pag1_data:
            sum_pag1_data.remove(None)
        #对data_shop_list中数据进行处理
        print("*1"*30)
        print(temp_data_shop_list)
        while '' in temp_data_shop_list:
            temp_data_shop_list.remove('')
        print(temp_data_shop_list)
        print("*"*30)
        shop_index = temp_data_shop_list.index(shop_name)
        data_shop_list.append(temp_data_shop_list[shop_index])
        data_shop_list.append(temp_data_shop_list[shop_index+1])
        # print(data_shop_list)
        # save_shop_csv(data_shop_list)


    except:
        try:
            live_broadcast_ele = driver.find_element_by_xpath('//android.view.View[@content-desc="直播"]')
            live_broadcast_ele.click()
            time.sleep(5)
            try:
                eles = driver.find_elements_by_class_name('android.view.View')
                for ele in eles:
                    sum_pag1_data.append(ele.get_attribute('content-desc'))
                    temp_data_shop_list.append(ele.text)
                while None in sum_pag1_data:
                    sum_pag1_data.remove(None)
                print("*2" * 30)
                print(temp_data_shop_list)
                while '' in temp_data_shop_list:
                    temp_data_shop_list.remove('')
                shop_index = temp_data_shop_list.index(shop_name)
                data_shop_list.append(temp_data_shop_list[shop_index])
                data_shop_list.append(temp_data_shop_list[shop_index + 1])
            except:
                driver.swipe(start_x=176, start_y=1801, end_x=176, end_y=1200, duration=500)
                eles = driver.find_elements_by_class_name('android.view.View')
                for ele in eles:
                    sum_pag1_data.append(ele.get_attribute('content-desc'))
                    temp_data_shop_list.append(ele.text)
                while None in sum_pag1_data:
                    sum_pag1_data.remove(None)
                print("*2" * 30)
                print(temp_data_shop_list)
                while '' in temp_data_shop_list:
                    temp_data_shop_list.remove('')
                shop_index = temp_data_shop_list.index(shop_name)
                data_shop_list.append(temp_data_shop_list[shop_index])
                data_shop_list.append(temp_data_shop_list[shop_index + 1])
            # save_shop_csv(data_shop_list)

        except:
            print("店铺没有直播数据")
            with open('未开直播的店铺','a',encoding='utf-8') as fp:
                fp.write(shop_name+'\n')
                driver.quit()




    """点击进入第二个页面"""
    # code = 'new UiSelector().className("android.view.View").descriptionContains("直播").instance(1)'
    # search_page2_ele= driver.find_element_by_android_uiautomator(code)
    # search_page2_ele.click()
    # s_index = find_index(sum_pag1_data, "回放")
    # data_shop_list = []
    # data_time_title_list = []
    # data_shop_list.append(sum_pag1_data[len(sum_pag1_data) - 6])
    # data_shop_list.append(sum_pag1_data[len(sum_pag1_data) - 8])
    # for i in range(len(s_index)):
    #     data_time_title_list.append(sum_pag1_data[s_index[i] - 2])
    #     data_time_title_list.append(sum_pag1_data[s_index[i] + 1].strip())
    # num = sum_pag1_data.index("搜索店内宝贝")
    # data_time_title_list.append(sum_pag1_data[num - 3])
    # data_time_title_list.append(sum_pag1_data[num - 1].strip())
    # print(data_shop_list)
    # print(data_time_title_list)
    # data_time_title.extend(data_time_title_list)
    # )"""滑动屏幕"""
    #     # code_scroll_origin = 'new UiSelector().className("android.view.View").description("{}")'.format(
    #     #     data_time_title_list[0])
    #     # code_scroll_des = 'new UiSelector().className("android.view.View").description("{}")'.format(
    #     #     data_time_title_list[4]
    # code_scroll_origin_ele = driver.find_element_by_android_uiautomator(code_scroll_origin)
    # code_scroll_des_ele = driver.find_element_by_android_uiautomator(code_scroll_des)
    # # driver.drag_and_drop(code_scroll_origin_ele,code_scroll_des_ele)
    # driver.drag_and_drop(code_scroll_des_ele, code_scroll_origin_ele)

    """10.25日 淘宝最新版本，
    1.店铺信息class的text的属性提取
    2.直播信息由class 的content-desc属性提取"""
    try:
        temp_scrool = re_fun(sum_pag1_data)
        # save_page1_csv(data_shop_list,temp_scrool[0],temp_scrool[1])
        print(temp_scrool[0])
        page2_click(data_shop_list,temp_scrool[0],temp_scrool[1])
        scroll_fun(temp_scrool[0])
        for i in range(20):
            flag = scroll_data(data_shop_list)
            if flag ==1:
                break
        driver.press_keycode(4)
        driver.press_keycode(4)
    except:
        print("点击进入第二个页面,出错")


    # input("结束程序")
    # driver.quit()


if __name__ == '__main__':
    fp = open('淘宝直播数据_服饰.csv', 'a', encoding='utf-8', newline='')
    csv_writer = csv.writer(fp)
    fp.close()
    # csv_writer.writerow(['店铺名', '粉丝数', '直播时间', '直播标题', '观看人数','直播商品数','直播间ID','直播商品','商品价格'])
    # input("1")
    df = pd.read_csv('未抓取的店铺.csv')
    full_shoplist = df['淘宝店铺名称']
    full_shoplist = list(full_shoplist)
    for i in range(len(full_shoplist)):
        try:
            with open('抓取的店铺.txt', 'a', encoding='utf-8') as fp:
                fp.write(full_shoplist[i]+"\n")
            try:
                shop_page(full_shoplist[i])
            except:
                print("失败了，需要重新爬取")
                with open('失败的店铺.txt','a',encoding='utf-8') as fp:
                    fp.write(full_shoplist[i]+'\n')
                try:
                    desired_caps = {
                        'platformName': 'Android',  # 被测手机是安卓
                        'platformVersion': '9',  # 手机安卓版本
                        'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
                        'appPackage': 'com.taobao.taobao',  # 启动APP Package名称
                        'appActivity': 'com.taobao.tao.TBMainActivity',  # 启动Activity名称
                        'unicodeKeyboard': False,  # 使用自带输入法，输入中文时填True
                        'resetKeyboard': True,  # 执行完程序恢复原来输入法
                        'noReset': True,  # 不要重置App
                        'newCommandTimeout': 6000,
                        'automationName': 'UiAutomator2'
                    }

                    # 连接Appium Server，初始化自动化环境
                    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                    # 设置缺省等待时间
                    driver.implicitly_wait(20)
                    # 点击微淘按钮
                    weitao = driver.find_element_by_xpath(
                        '//android.widget.FrameLayout[@content-desc="微淘"]/android.widget.ImageView')
                    weitao.click()
                    time.sleep(1)
                except:
                    desired_caps = {
                        'platformName': 'Android',  # 被测手机是安卓
                        'platformVersion': '9',  # 手机安卓版本
                        'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
                        'appPackage': 'com.taobao.taobao',  # 启动APP Package名称
                        'appActivity': 'com.taobao.tao.TBMainActivity',  # 启动Activity名称
                        'unicodeKeyboard': False,  # 使用自带输入法，输入中文时填True
                        'resetKeyboard': True,  # 执行完程序恢复原来输入法
                        'noReset': True,  # 不要重置App
                        'newCommandTimeout': 6000,
                        'automationName': 'UiAutomator2'
                    }

                    # 连接Appium Server，初始化自动化环境
                    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                    # 设置缺省等待时间
                    driver.implicitly_wait(20)
                    # 点击微淘按钮
                    weitao = driver.find_element_by_xpath(
                        '//android.widget.FrameLayout[@content-desc="微淘"]/android.widget.ImageView')
                    weitao.click()
                    time.sleep(1)
        except:
            os.system('adb kill-server')
            os.system('adb start-server')
            time.sleep(2)
