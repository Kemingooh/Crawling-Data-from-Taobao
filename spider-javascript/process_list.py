from csv import reader

file_path = r'C:\Users\DELL\Desktop\淘宝直播数据_数码.csv'

if __name__=='__main__':
    with open(file_path,'r',encoding='utf-8') as csv_file:
        file_reader=reader(csv_file)
        res=[]
        for r in file_reader:
            if len(r)>=2:
                link=r[1]
                if link.startswith('http'):
                    res.append(r[1])
    
        print(res)
