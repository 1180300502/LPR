import datetime


def time_s(plate,path_gar):  # 将车牌和时间写入数据库
    print('车牌：'+plate)
    time_sta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   # gar = open("garage.txt", "a", encoding='utf-8')
    #gar = open(path_gar, "a", encoding='utf-8') 
    gar = open(path_gar, "a")
    #gar = open(path_gar, "a") 
    gar.write('\n')
    gar.write(plate)
    gar.write(" ")
    gar.write(time_sta)
    gar.close()
    return plate+'\n'+time_sta

