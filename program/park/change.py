import re


def char(plate,path_gar,path_show):
    contents_gar = []
  #  path_gar = "garage.txt"
    #path_gar = 'C:/Users/Lenovo/Desktop/python_code/project0/park/garage.txt'
    #path_gar = 'project0/park/garage.txt'
    #  遍历收费车牌存储库，如果没有该车牌，获取时间并和车牌号一块存入收费车牌存储库中
    #txt_gar = open(path_gar, "r", encoding="utf-8")
    txt_gar = open(path_gar, "r")
    for line in txt_gar.readlines():
        line = line.strip()
        contents_gar.append(line)
    txt_gar.close()
    y = ' '.join(contents_gar)
    n = re.search(plate, y)
    if n is None:
       # print("11111111111")
        print(plate+'进入停车场')
        import park.time_re as time_re
        return time_re.time_s(plate,path_gar)
    else:
        print(plate+'离开停车场')
        import park.rates as rates
        return rates.rate(plate,path_gar,path_show)
      #  print("22222222222")
       