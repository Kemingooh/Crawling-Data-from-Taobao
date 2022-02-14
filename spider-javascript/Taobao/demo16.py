import re
a = ['元', '分享抢券', '\u3000\u3000\u3000\u3000 大萌/秋冬新  图书馆女孩~ 复古时髦小甜甜灯芯绒v领宽松背带裤女', '每200减25', '满499减10', '\u3000\u3000\u3000\u3000 大萌/秋冬新  钻进暖暖の小羊羔世界  宽松羊羔毛马甲外套 回馈款', '每200减25', '满499减10', '\u3000\u3000\u3000\u3000 大萌/秋冬新  Mom Jeans！ 两粒扣 磨毛做旧锥形高腰九分牛仔…', '每200减25', '满499减10']
def handle_data4(a):
    """对数据第三次处理
    1.去除一些元
    2.去除分享抢卷
    3.去除满减"""
    while '元' in a :
        a.remove('元')
    while '分享抢券' in a :
        a.remove('分享抢券')
    pat1 = '(每\d{1,10}减\d{1,5})|(满\d{1,10}减\d{1,5})'
    pat2 = '(满\d{1,10}减\d{1,5})'
    temp = []

    for i in range(len(a)):
        ret1 = re.match(pat1,a[i])
        try:
            temp.append(ret1.group())
        except:
            pass
    list3 = list(set(a)-set(temp))
    return list3

