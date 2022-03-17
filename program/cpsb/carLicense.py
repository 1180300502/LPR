# 导入所需模块
import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
import random


# 定义必要函数

# 显示图片
def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


# plt显示彩色图片
def plt_show0(img):
    b, g, r = cv2.split(img)
    img = cv2.merge([r, g, b])
    plt.imshow(img)
    plt.show()


# plt显示灰度图片
def plt_show(img):
    plt.imshow(img, cmap='gray')
    plt.show()


# 图像去噪灰度处理
def gray_guss(image):
    image = cv2.GaussianBlur(image, (3, 3), 0)#高斯去噪
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)#将BGR格式转换成灰度图片
    return gray_image



# 提取车牌部分图片
def get_carLicense_img(image,origin_image):
    #高斯去噪灰度处理
    gray_image = gray_guss(image)
    # 预览效果
    # 展示图片1
    # plt_show(gray_image)

    #sobel算子边缘检测
    Sobel_x = cv2.Sobel(gray_image, cv2.CV_16S, 1, 0)
    absX = cv2.convertScaleAbs(Sobel_x)#将原图片转换为uint8类型
    image = absX
    # 展示图片1
    # plt_show(image)

    # 自适应阈值处理，变成黑白图像
    ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
    # 展示图片1
    # plt_show(image)

    # 闭运算,是白色部分练成整体，先膨胀后腐蚀
    kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernelX,iterations = 3)
    # 展示图片1
    #  plt_show(image)

    #去除小白点
    kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
    kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 19))

    image = cv2.dilate(image, kernelX)
    image = cv2.erode(image, kernelX)

    image = cv2.erode(image, kernelY)
    image = cv2.dilate(image, kernelY)
    # 展示图片1
    # plt_show(image)

    # 中值滤波去除噪点
    image = cv2.medianBlur(image, 15)
    # 展示图片1
    # plt_show(image)

    # 轮廓检测
    # cv2.RETR_EXTERNAL表示只检测外轮廓
    # cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 绘制轮廓
    image1 = origin_image.copy()
    cv2.drawContours(image1, contours, -1, (0, 255, 0), 5)
    # 展示图片1
    # plt_show0(image1)


    for item in contours:
        rect = cv2.boundingRect(item)
        x = rect[0]
        y = rect[1]
        weight = rect[2]
        height = rect[3]
        if (weight > (height * 3)) and (weight < (height * 4)):
            image = origin_image[y:y + height, x:x + weight]
            return image



def carLicense_spilte(image):
    #将车牌图像去噪并二值化
    gray_image = gray_guss(image)
    ret, image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
    # 展示图片1
    # plt_show(image)


    # 计算二值图像黑白点的个数，处理绿牌照问题，让车牌号码始终为白色
    area_white = 0
    area_black = 0
    height, width = image.shape
    for i in range(height):
        for j in range(width):
            if image[i, j] == 255:
                area_white += 1
            else:
                area_black += 1
    if area_white > area_black:
        ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        # plt_show(image)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,3))
    image = cv2.dilate(image, kernel)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)




    words = []
    word_images = []
    for item in contours:
        word = []
        rect = cv2.boundingRect(item)
        x = rect[0]
        y = rect[1]
        weight = rect[2]
        height = rect[3]
        word.append(x)
        word.append(y)
        word.append(weight)
        word.append(height)
        words.append(word)
    words = sorted(words, key=lambda s: s[0], reverse=False)
    i = 0
    for word in words:
        if (word[3] > (word[2] * 1.8)) and (word[3] < (word[2] * 3.5)):
            i = i + 1
            splite_image = image[word[1]:word[1] + word[3], word[0]:word[0] + word[2]]
            word_images.append(splite_image)
    return word_images


# 准备模板
template = ['0','1','2','3','4','5','6','7','8','9',
            'A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z',
            '藏','川','鄂','甘','赣','贵','桂','黑','沪','吉','冀','津','晋','京','辽','鲁','蒙','闽','宁',
            '青','琼','陕','苏','皖','湘','新','渝','豫','粤','云','浙']

# 读取一个文件夹下的所有图片，输入参数是文件名，返回文件地址列表
def read_directory(directory_name):
    referImg_list = []
    for filename in os.listdir(directory_name):
        referImg_list.append(directory_name + "/" + filename)
    return referImg_list

# 中文模板列表（只匹配车牌的第一个字符）
def get_chinese_words_list():
    chinese_words_list = []
    for i in range(34,64):
        #c_word = read_directory('./refer1/'+ template[i])
        c_word = read_directory('C:/Users/26578/Desktop/中国高科实习/项目/program/cpsb/refer1/'+ template[i])
        chinese_words_list.append(c_word)
    return chinese_words_list
chinese_words_list = get_chinese_words_list()

# 英文模板列表（只匹配车牌的第二个字符）
def get_eng_words_list():
    eng_words_list = []
    for i in range(10,34):
        e_word = read_directory('C:/Users/26578/Desktop/中国高科实习/项目/program/cpsb/refer1/'+ template[i])
        eng_words_list.append(e_word)
    return eng_words_list
eng_words_list = get_eng_words_list()

# 英文数字模板列表（匹配车牌后面的字符）
def get_eng_num_words_list():
    eng_num_words_list = []
    for i in range(0,34):
        word = read_directory('C:/Users/26578/Desktop/中国高科实习/项目/program/cpsb/refer1/'+ template[i])
        eng_num_words_list.append(word)
    return eng_num_words_list
eng_num_words_list = get_eng_num_words_list()


# 读取一个模板地址与图片进行匹配，返回得分
def template_score(template,image):
    template_img=cv2.imdecode(np.fromfile(template,dtype=np.uint8),1)
    template_img = cv2.cvtColor(template_img, cv2.COLOR_RGB2GRAY)
    ret, template_img = cv2.threshold(template_img, 0, 255, cv2.THRESH_OTSU)
#     height, width = template_img.shape
#     image_ = image.copy()
#     image_ = cv2.resize(image_, (width, height))
    image_ = image.copy()
    height, width = image_.shape
    template_img = cv2.resize(template_img, (width, height))
    result = cv2.matchTemplate(image_, template_img, cv2.TM_CCOEFF)
    return result[0][0]

def template_matching(word_images):
    results = []
    for index,word_image in enumerate(word_images):
        if index==0:
            best_score = []
            for chinese_words in chinese_words_list:
                score = []
                for chinese_word in chinese_words:
                    result = template_score(chinese_word,word_image)
                    score.append(result)
                best_score.append(max(score))
            i = best_score.index(max(best_score))
            # print(template[34+i])
            r = template[34+i]
            results.append(r)
            continue
        if index==1:
            best_score = []
            for eng_word_list in eng_words_list:
                score = []
                for eng_word in eng_word_list:
                    result = template_score(eng_word,word_image)
                    score.append(result)
                best_score.append(max(score))
            i = best_score.index(max(best_score))
            # print(template[10+i])
            r = template[10+i]
            results.append(r)
            continue
        else:
            best_score = []
            for eng_num_word_list in eng_num_words_list:
                score = []
                for eng_num_word in eng_num_word_list:
                    result = template_score(eng_num_word,word_image)
                    score.append(result)
                best_score.append(max(score))
            i = best_score.index(max(best_score))
            # print(template[i])
            r = template[i]
            results.append(r)
            continue
    return results


# # 输出对应的识别车牌图片以及识别的车牌号码结果
# def cpsb():
#     i=random.randint(0,19)
#     print(i)
#     str1 = ''
#     str1 = '.\data\\' + str(i) + '.jpg'
#     # 读取待检测图片
#     origin_image = cv2.imread(str1)
#     # plt_show0(origin_image)

#     image = origin_image.copy()
#     carLicense_image = get_carLicense_img(image,origin_image)
#     # plt_show0(carLicense_image)

#     image = carLicense_image.copy()
#     word_images = carLicense_spilte(image)

#     # 绿牌要改为8，蓝牌为7，显示所用
#     for i, j in enumerate(word_images):
#         plt.subplot(1, 8, i + 1)
#         plt.imshow(word_images[i], cmap='gray')
#     # plt.show()
#     word_images_ = word_images.copy()
#     result = template_matching(word_images_)
#     print(result)
#     return i,result

# # i,result=cpsb()

# 输出对应的识别车牌图片以及识别的车牌号码结果
def recognize(picpath):
    # i=random.randint(0,19)
    # print(i)
    # str1 = ''
    # str1 = '.\data\\' + str(i) + '.jpg'
    #picpath = 'C:/Users/Lenovo/Desktop/python_code/project0/cpsb/car/0.jpg'
    # 读取待检测图片
    origin_image = cv2.imread(picpath)
    # plt_show0(origin_image)

    image = origin_image.copy()
    carLicense_image = get_carLicense_img(image,origin_image)
    # plt_show0(carLicense_image)

    image = carLicense_image.copy()
    word_images = carLicense_spilte(image)

    # 绿牌要改为8，蓝牌为7，显示所用
    for i, j in enumerate(word_images):
        plt.subplot(1, 8, i + 1)
        plt.imshow(word_images[i], cmap='gray')
    # plt.show()
    word_images_ = word_images.copy()
    result = template_matching(word_images_)
    result = ''.join(result)
   # print(result)
    return i,result #所属类别（绿牌或者蓝牌）和识别结果

# i,result=cpsb()
# recognize('../cpsb/car/0.jpg')
# if __name__=='__main__':
#     print(recognize('C:/Users/Lenovo/Desktop/python_code/project0/program/cpsb/car/0.jpg'))




