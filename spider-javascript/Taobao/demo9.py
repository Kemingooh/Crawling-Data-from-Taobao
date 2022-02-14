import re
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
    return shop_title,shop_price_list


a = [None, None, None, None, None, None, None, '62', '大码女装胖mm文艺减龄休闲文艺纯白色拼接织带包边衬衫短袖连衣裙', None, '¥\xa056.86', '马上抢', '61', '大码女装胖mmt恤洋气宽松减龄遮肚子纯色中长款上衣2020夏季新款', None, '¥\xa039.98', '马上抢', '60', '棉麻短袖t恤女夏2019新款200斤胖mm宽松大码显瘦V领盘扣亚麻上衣', None, '¥\xa036.98', '马上抢', None, None]
s = handle_page3_data2(a)
print(s)