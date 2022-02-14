# a = []
# b = 10
# a.append(b)
# while b>2:
#     b = b-2
#     a.append(b)
# print(a)
# s =[]
# ss = []
# count = 0
# for i in range(len(a)):
#     s.append(a[i])
#     try:
#         s.append(a[i+1])
#     except:
#         pass
#
#
#     ss.append(s)
#     s =[]


# print(ss)
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
a = turnPage(10)