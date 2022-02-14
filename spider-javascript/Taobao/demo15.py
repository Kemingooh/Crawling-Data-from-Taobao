import re
# a = ['元', '分享抢券', '\u3000\u3000\u3000\u3000 大萌/秋冬新 守护你的童趣与少女心~ 笑脸插肩袖厚实质感毛衣上衣', '\u3000\u3000\u3000\u3000 大萌/秋冬新 甜美乖巧全靠它！羊毛插肩袖基础纯色宽松毛衣针…', '\u3000\u3000\u3000\u3000 大萌/秋冬新  毫不费力の时髦感 蓝粒绒大衣式口袋宽松纯色外套女']
# a = ['元', '分享抢券', '\u3000\u3000\u3000\u3000 大萌/秋冬新  图书馆女孩~ 复古时髦小甜甜灯芯绒v领宽松背带裤女', '每200减25', '满499减10', '\u3000\u3000\u3000\u3000 大萌/秋冬新  钻进暖暖の小羊羔世界  宽松羊羔毛马甲外套 回馈款', '每200减25', '满499减10', '\u3000\u3000\u3000\u3000 大萌/秋冬新  Mom Jeans！ 两粒扣 磨毛做旧锥形高腰九分牛仔…', '每200减25', '满499减10']
a = ['\u3000\u3000 夏日水蜜桃适用11pro max苹果x手机壳iphone8plus少女se软xs/xr套', '淘金币抵0.5元', '\u3000\u3000 个性浮雕适用11pro max苹果xr手机壳iphonex/xr情侣8plus潮xs女7P', '淘金币抵0.5元', '简约笑脸适用11pro max苹果x手机壳iphone8plus全包xr/xs防摔7/se', '淘金币抵0.5元']
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
s = handle_page3_data2(a)
print(s[0])