a = ['最新微淘', '上新', '直播', '周一 2020 Oct 12', '10月12日 19:29', '回放', '          10.12 福利直播', '', '900阅读', '0', '0', '周五 2020 Oct 09', '10月09日 20:00', '回放', '          10.9直播捡漏', '', '939阅读', '0', '0', '周三 2020 Oct 07', '10月07日 19:23', '          10.7福利直播', '搜索店内宝贝', '宝贝分类', '花姑子服饰', '关注', '粉丝数33.4万', '首页', '全部宝贝', '店铺微淘', '宝贝分类', '联系客服']
def find_index(src_list, target):
    """在给定集合中寻找目标所在索引"""

    #用来存储目标索引的列表
    dst_index_list = []

    #在给定集合中挨个比对，若与目标匹配，保留索引
    for index in range(len(src_list)):
        if (src_list[index] == target):
            dst_index_list.append(index)

    #返回目标索引列表
    return dst_index_list
s_index = find_index(a,"回放")
data_list = []
data_time_title_list = []
data_list.append(a[len(a)-6])
data_list.append(a[len(a)-8])
for i in range(len(s_index)):
    data_time_title_list.append(a[s_index[i]-2])
    data_time_title_list.append(a[s_index[i]+1].strip())
#加上一页中的最后一个数据
num = a.index("搜索店内宝贝")
data_time_title_list.append(a[num-3])
data_time_title_list.append(a[num-1].strip())
print(data_list)
print(data_time_title_list)
