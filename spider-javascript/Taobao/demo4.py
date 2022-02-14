import re
a = ['周四 2019 Dec 26', '12月27日 00:16', '回放', '          胖女神显瘦秋冬穿搭', '175阅读', '0', '0', '周三 2019 Dec 25', '12月26日 00:15', '回放', '          胖女神显瘦秋冬穿搭', '175阅读', '0', '0', '12月25日 11:20', '回放', '          胖女神显瘦秋冬穿搭', '157阅读', '0', '0', '搜索店内宝贝', '宝贝分类', '首页', '全部宝贝', '店铺微淘', '宝贝分类', '联系客服']
b = ['回放', '218阅读', '0', '0', '12月28日 11:26', '回放', '          胖女神显瘦秋冬穿搭', '167阅读', '0', '0', '周五 2019 Dec 27', '12月28日 00:25', '回放', '          胖女神显瘦秋冬穿搭', '140阅读', '0', '0', '周四 2019 Dec 26', '12月27日 00:16', '          胖女神显瘦秋冬穿搭', '搜索店内宝贝', '宝贝分类', '首页', '全部宝贝', '店铺微淘', '宝贝分类', '联系客服']
c = ['回放', '561阅读', '0', '0', '周六 2020 Apr 25', '04月25日 09:58', '回放', '          美美大码开播啦', '415阅读', '0', '0', '周六 2019 Dec 28', '12月29日 00:26', '回放', '          胖女神显瘦秋冬穿搭', '218阅读', '0', '0', '12月28日 11:26', '          胖女神显瘦秋冬穿搭', '搜索店内宝贝', '宝贝分类', '首页', '全部宝贝', '店铺微淘', '宝贝分类', '联系客服']
date_pat = '(\d{1,2}月\d{1,2}日 .*)'
for i in range(len(a)):
    ret = re.match(date_pat,a[i])
    try:
        print(ret.group())
    except:
        pass
shop_pat='(\s{1,10}[\u4e00-\u9fa5].*)'
for i in range(len(a)):
    ret = re.match(shop_pat,a[i])
    try:
        print(ret.group())
    except:
        pass

def re_fun(shop_data_list):
    """正则提取直播日期和标题"""
    date_pat = '(\d{1,2}月\d{1,2}日 .*)'
    shop_pat = '(\s{1,10}[\u4e00-\u9fa5].*)'
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
    return date_list,title_list

s = re_fun(a)
print(s[0])
print(s[1])
