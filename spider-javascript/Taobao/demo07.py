import re
a = [None, None, None, None, None, None, None, '10', '161-180号 在此链接拍。请注意：无质量问题不退换！', None, '¥\xa0111.11', '马上抢', '9', '181-200号 在此链接拍。请注意：无质量问题不退换！', None, '¥\xa0111.11', '马上抢', '8', '121-140号 在此链接拍。请注意：无质量问题不退换！', None, '¥\xa0111.11', '马上抢', None, None]
while None in a :
    a.remove(None)
while '马上抢' in a:
    a.remove('马上抢')
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
shop_price_list = []
shop_price_pat = '(¥.*)'

for i in range(len(a)):
    ret = re.match(shop_price_pat, a[i])
    try:
        shop_price_list.append(ret.group())
        print(ret.group())
    except:
        pass
print(shop_price_list)
for i in range(len(shop_price_list)):
    index_list = find_index(a,shop_price_list[i])


shop_title = []
for i in range(len(index_list)):
    shop_title.append(a[index_list[i]-1])

