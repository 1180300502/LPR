from cpsb.carLicense import recognize
from park.main import record
import sys
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow,QDialog, QWidget
from AAA.form.main_window_ui import Ui_MainWindow
from AAA.form.cars_ui import Ui_cars
from AAA.form.driver_view_ui import Ui_driver_view
from AAA.form.help import Ui_help
from AAA.devs.video import CamVideo
import cv2
import numpy as np
import random
#import cpsb.carLicense
#import park

class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm,self).__init__()
        #引入主窗体
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.dev=CamVideo()
        self.dev.start()
        self.dev.sig_video.connect(self.show_video)
        self.is_cap=False
        #self.ans = '待检测'

        #创建按钮点击信号连接 
        self.ui.but_img_2.clicked.connect(self.show_driver)
        self.ui.but_img.clicked.connect(self.show_help)
        self.ui.but_record.clicked.connect(self.show_cars)
    def capture(self):
        self.is_cap=True
    
    # def rec(self):
    #     path_save = 'C:/Users/Lenovo/Desktop/python_code/project0/program/test.txt'#存储答案的路径
    #    # class_id,result = recognize('C:/Users/Lenovo/Desktop/python_code/project0/program/cpsb/car/0.jpg')
    #     result = '青DDD2222'
    #     f,ans = record(result)
    #     print(ans)
    #     txt_sho = open(path_save, "w", encoding='utf-8')#w 覆盖原值
    #     txt_sho.write(ans)
    #     txt_sho.close()
    #    # class_id,pro = self.rec.recognizer(self.cap_img)
    #    # result = F"{class_id},{pro}"
    #    # self.ui.label.setText(result)

    def show_driver(self):
        self.win_driver=driver_window()
        self.win_driver.show()

    def show_help(self):
        self.win_help=help_window()
        self.win_help.show()
    
    def show_cars(self):
        self.win_cars=cars_window()
        self.win_cars.show()

    def show_video(self,h,w,c,data): #data是要显示的图片
       # path_save = ''#存储答案的路径
        path_save = '../test.txt'#存储答案的路径
        path_pic = ''
        m=random.randint(0,2)
        path_pic='../cpsb/data/'+str(m)+'.jpg'
        img = QImage(data,w,h,w*c,QImage.Format_RGB888)
        #cv2.imshow("picture",img)
        # i,tmp = cpsb(picpath)#怎么把从路径读入改成直接 读图片
        # f,ans = park.record(tmp)
        # txt_sho = open(path_save, "w", encoding='utf-8')#w 覆盖原值
        # txt_sho.write(ans)
        # txt_sho.close()
        pix=QPixmap.fromImage(img)
        #cv2.imshow(img)
        if self.is_cap:
            self.cap_img=np.ndarray(
                (h,w,c),
                np.uint8,
                data
            )
            self.ui.img_label.setPixmap(pix)
            self.ui.img_label.setScaledContents(True)
            #result = '青DDD2222'
           # class_id,result = recognize(self.cap_img)
            #class_id,result = recognize('C:/Users/Lenovo/Desktop/python_code/project0/program/cpsb/car/0.jpg')
            class_id,result = recognize(path_pic)
            f,ans = record(result)
            print(ans)
            #txt_sho = open(path_save, "w", encoding='utf-8')#w 覆盖原值
            txt_sho = open(path_save, "w")
            txt_sho.write(ans)
            txt_sho.close()
            self.is_cap=False
            pic = cv2.imread(path_pic)
            cv2.imshow('car', pic)
        self.ui.img_camera.setPixmap(pix)
        self.ui.img_camera.setScaledContents(True)
    
    def closeEvent(self,e):
        self.dev.close()

class driver_window(QWidget):
    def __init__(self):
        path_read = '../test.txt' #和show_video 的path_save是同一个，存储识别的结果
        super(driver_window,self).__init__()
        #引入司机查看界面
        self.ui= Ui_driver_view()
        #self.ui.setupUi(self,"haha")#这里是答案，就是车牌识别的结果
        with open(path_read,'r') as f:
            msg=f.read()
            self.ui.setupUi(self,msg)#这里是答案，就是车牌识别的结果      
    # def getMoney(self):
    #     self.filename=QFileDialog.getOpenFileNames()


class help_window(QWidget):
    def __init__(self):
        super(help_window,self).__init__()
        #引入信息界面
        self.ui = Ui_help()
        self.ui.setupUi(self)
        #self.ui.label.setSource

class cars_window(QWidget):
    def __init__(self):
        super(cars_window,self).__init__()
        #引入仓库界面
        self.ui=Ui_cars()
        self.ui.setupUi(self)

if __name__=='__main__':
    app =QApplication(sys.argv)
    win_main=MainForm()
    win_main.show()
    app.exec_()

       