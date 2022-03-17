import re

def record(plate):
    # plate = "青ADD1484"
    #plate = '青DDD1434'
    contents_in = []
    #path_in = "inner.txt"'
    path_in='C:/Users/26578/Desktop/中国高科实习/项目/program/park/inner.txt'#内部车辆信息文件
    path_gar = 'C:/Users/26578/Desktop/中国高科实习/项目/program/park/garage.txt'#车库内目前停放车辆的信息文件
    path_show = 'C:/Users/26578/Desktop/中国高科实习/项目/program/park/show.txt'#存储记录的信息文件
    #path_in = 'project0/park/inner.txt'
    #path_in = './inner.txt'
    # 打开存储内部车辆车牌号的文件，并读取信息
    # txt_in = open(path_in, "r", encoding="utf-8")
    txt_in = open(path_in, "r")
    for line in txt_in.readlines():
        line = line.strip()
        contents_in.append(line)
    txt_in.close()
    x = ' '.join(contents_in)
    m = re.search(plate, x)  # 将接收到的车牌与内部车牌进行字符串匹配
    if m is None:  # 若匹配不到将车牌信息传入到charge.py进行停车费计算
        import park.change as change
        show = change.char(plate,path_gar,path_show)
        return False,show#不是内部车辆
    else:
        return True,'内部车辆' #是内部


# if __name__=='__main__':
#     print(record('青DDD2222'))


# import re
# plate = "青ADD1484"
# contents_in = []
# #path_in = "inner.txt"'
# path_in='C:/Users/Lenovo/Desktop/python_code/project0/park/inner.txt'
# # 打开存储内部车辆车牌号的文件，并读取信息
# txt_in = open(path_in, "r", encoding="utf-8")
# for line in txt_in.readlines():
#     line = line.strip()
#     contents_in.append(line)
# txt_in.close()
# x = ' '.join(contents_in)
# m = re.search(plate, x)  # 将接收到的车牌与内部车牌进行字符串匹配
# if m is None:  # 若匹配不到将车牌信息传入到charge.py进行停车费计算
#     import change
#     change.char(plate)


