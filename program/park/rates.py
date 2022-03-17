import datetime
import time
import math
# 将收费车辆有关的信息读到列表


def rate(plate,path_gar,path_show):
    #path_show = 'project0/park/show.txt'
    r = 0
    lines = []  # 创建了一个空列表，里面没有元素
   # with open('garage.txt', 'r', encoding='utf-8') as f:
    #with open(path_gar, 'r', encoding='utf-8') as f:
    with open(path_gar, 'r') as f:
        for line in f.readlines():
            if line != '\n':
                lines.append(line)
                f.close()
    for line in lines:
        r += 1
        if plate in line:  # 如果a已经存在库中，那么获取时间，并计算费用，存入库中
            flag = r
            line = lines[flag - 1]
            time_sta = line[8:-1]
            print('开始时间:'+time_sta)
            time_array = time.strptime(time_sta, "%Y-%m-%d %H:%M:%S")
            time_stamp = int(time.mktime(time_array))
            tim_fin = time.time()  # 读取时间
            tim = float((tim_fin - time_stamp)) / 3600
            cost = math.trunc(tim * 10)
            other_fin_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取格式化的时间
            lines[flag - 1] = ''
            content_sh = plate + ' 停车费用:' + str(cost) + '元 离开时间:' + other_fin_time + '---' + '进入时间:' + time_sta #这个是要展示在ui里的字符串
           # txt_sho = open("show.txt", "a", encoding='utf-8')
           # txt_sho = open(path_show, "a", encoding='utf-8')
            txt_sho = open(path_show, "a", encoding='utf-8')
            txt_sho.write('\n')
            txt_sho.write(content_sh)
            txt_sho.close()
           # txt_age = open("garage.txt", "w", encoding='utf-8')  # 收费后从数据库中删除该车牌
           # txt_age = open(path_gar, "w", encoding='utf-8')  # 收费后从数据库中删除该车牌 #这是怎么删去的？
            txt_age = open(path_gar, "w")
            sep = ''
            txt_age.write(sep.join(lines))
            txt_age.close()
            # print('测试：'+plate+'\n'+time_sta+'\n'+other_fin_time+'\n'+str(cost))
            # print('结束')
            return plate+'\n\n'+time_sta+'\n\n'+other_fin_time+'\n\n'+str(cost)
    return "error:查询不到车辆的进入信息"
