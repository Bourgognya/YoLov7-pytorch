#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os
import time

import numpy as np
from PIL import Image
from yolo import YOLO

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#PyQt介面
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        # self.setBac
        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()#介面設置
        self.slot_init()#開啟相機事件
        self.database()
        self.predict()
        self.__flag_work = 0
        self.x = 0
        self.count = 0

    def predict(self):
        self.canshu.clicked.connect(self.prediction)
    #數值預測
    def prediction(self):
        path = 'output.txt'
        # f = open(path, 'w')
        # if __name__ == "__main__":
        #     yolo = YOLO()
        #     mode = "predict"
        #     crop= False
        #     count= False
        #     if mode == "predict":
        #         FName = fr"images\cap{time.strftime('%Y%m%d%H%M', time.localtime())}"
        #         img = FName+".jpg"
        #         image = Image.open(img)
        #         r_image = yolo.detect_image(image, crop = crop, count=count)
        #         r_image.show()
        #裁切圖片依序寫入txt檔併轉換成數值寫入資料庫
        f = open(path, 'w')
        FName = fr"images\cap{time.strftime('%Y%m%d%H%M', time.localtime())}"
        img = cv2.imread(FName+".jpg")
        # 裁切區域的 x 與 y 座標（左上角）
        x = 280
        y = 100
        # 裁切區域的長度與寬度
        w = 50
        h = 600
        # 裁切圖片
        for i in range(4):
            x1=x+(75*i)
            crop_img = img[y:y+h, x1:x1+w]
            cv2.imshow("cropped", crop_img)
            cv2.imwrite('img/crop/{}.jpg'.format(i), crop_img)
            cv2.waitKey(0)
        if __name__ == "__main__":
            yolo = YOLO()
            mode = "predict"
            crop= False
            count= False
            if mode == "predict":
                for i in range(4):
                    img = "img\crop\{}.jpg".format(i)
                    image = Image.open(img)
                    r_image = yolo.detect_image(image, crop = crop, count=count)
                    r_image.show()
        f = open(path, 'r')
        i,num=0,0
        for line in f.readlines():
            #print(line)
            num+=int(line)*(10**(2-i))
            i+=1
        print(num,"g")
        f.close()

    # #寫入資料庫
    def database(self):
        self.det.clicked.connect(self.write_database)
        print('3')
    def write_database(self):
        print('4')
        app = Flask(__name__)
        # MySql datebase
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:gary131464035@127.0.0.1:3306/oyster"
        oyster = SQLAlchemy(app)
        class Product(oyster.Model):
            print('ok3')
            __tablename__ = 'Product'
            pid = oyster.Column(oyster.Integer, primary_key=True)
            name = oyster.Column(oyster.String(30), unique=True, nullable=False)
            weight = oyster.Column(oyster.String(10), nullable=False)
            meat_weight = oyster.Column(oyster.Float, nullable=False)
            size= oyster.Column(oyster.Float, nullable=True)
            insert_time = oyster.Column(oyster.DateTime, default=datetime.now)
            update_time = oyster.Column(oyster.DateTime, onupdate=datetime.now, default=datetime.now)
            
            def __init__(self, name, weight, meat_weight, size):
                self.name = name
                self.weight = weight
                self.meat_weight = meat_weight
                self.size= size
        #讀取txt
        path = 'output.txt'
        f = open(path, 'r')
        i,num=0,0
        for line in f.readlines():
            num+=int(line)*(10**(2-i))
            i+=1
        f.close()
        print(num)
        #新增讀取資料
        product_max = Product('Oyster14',num,0.0,10.0)
        oyster.session.add(product_max)
        oyster.session.commit()
        app.run(debug=True)
        # @app.route('/')
        # def index():
        # # Create data
        #     oyster.create_all()
        #     return 'ok'

        # if __name__ == "__main__":
        #     app.run(debug=True)


#介面設置(字體 按鈕)
    def set_ui(self):
        font = QtGui.QFont()
        font.setFamily("kaiti")#字體
        font.setPointSize(18)
        self.textBrowser = QtWidgets.QLabel("牡蠣辨識系統")
        self.textBrowser.setAlignment(Qt.AlignCenter)
        self.textBrowser.setFont(font)

        # self.label.setText(_translate("MainWindow", "TextLabel"))
        self.mm_layout = QVBoxLayout()
        self.l_down_widget = QtWidgets.QWidget()
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()
        self.button_open_camera = QtWidgets.QPushButton(u'打開相機')
        self.button_cap = QtWidgets.QPushButton(u'拍照')

        self.canshu = QtWidgets.QPushButton(u'重量檢測')
        self.det = QtWidgets.QPushButton(u'寫入資料庫')
        fontx = QtGui.QFont()
        fontx.setFamily("kaiti")
        fontx.setPointSize(16)

        # Button 的颜色修改
        button_color = [self.button_open_camera, self.button_cap, self.canshu, self.det]
        for i in range(4):
            button_color[i].setFont(fontx)
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                          "QPushButton:hover{color:red}"
                                          "QPushButton{background-color:rgb(78,255,255)}"
                                          "QPushButton{border:2px}"
                                          "QPushButton{border-radius:10px}"
                                          "QPushButton{padding:2px 4px}")

        self.button_open_camera.setMinimumHeight(50)
        self.button_cap.setMinimumHeight(50)
        self.canshu.setMinimumHeight(50)
        self.det.setMinimumHeight(50)

        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(500, 500)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)

        self.label_show_camera.setFixedSize(641, 481)
        # self.label_show_camera.setFixedSize(1300, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_cap)
        self.__layout_fun_button.addWidget(self.canshu)
        self.__layout_fun_button.addWidget(self.det)
        self.__layout_fun_button.addWidget(self.label_move)
        # 添加一个右侧的组件
        self.right_widget = QWidget()
        self.right_widget_layout = QHBoxLayout()
        self.cap_label = QLabel()
        self.cap_label.setFixedSize(641, 481)
        # self.label_show_camera.setFixedSize(1300, 481)
        self.cap_label.setAutoFillBackground(False)
        self.right_widget_layout.addWidget(self.label_show_camera)
        self.right_widget_layout.addWidget(self.cap_label)
        self.right_widget.setLayout(self.right_widget_layout)

        self.__layout_main.addWidget(self.right_widget)
        self.__layout_main.addLayout(self.__layout_fun_button)
        # self.__layout_main.addWidget(self.label_show_camera)


        # self.setLayout(self.__layout_main)
        self.l_down_widget.setLayout(self.__layout_main)
        self.mm_layout.addWidget(self.textBrowser)
        self.mm_layout.addWidget(self.l_down_widget)
        self.setLayout(self.mm_layout)
        self.label_move.raise_()
        self.setWindowTitle(u'牡蠣辨識系統')
        # self.setStyleSheet("#MainWindow{border-image:url(DD.png)}")

       
        # 设置背景图片
        # palette1 = QPalette()
        # palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('img\crop\AnyConv.com__3a5a5122bf0b0f48df71729b9d356804.jpg')))
        # self.setPalette(palette1)
        
    def slot_init(self):#相機按鈕
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_cap.clicked.connect(self.capx)


    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM,  cv2.CAP_DSHOW)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"請檢測相機是否設置正確",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)

                self.button_open_camera.setText(u'關閉相機')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'開啟相機')

    def show_camera(self):
        # if __name__ == "__main__":
        #     path = 'output.txt'
        #     f = open(path, 'w')
        #     yolo = YOLO()
        #     mode = "video"
        #     video_path      = 0
        #     video_fps       = 25.0
        #     video_save_path = "img/test6.mp4"
        #     if mode == "video":
        #         capture = cv2.VideoCapture(video_path)
        #         if video_save_path!="":
        #             fourcc  = cv2.VideoWriter_fourcc(*'XVID')
        #             size    = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        #             out     = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)
        #         ref, frame = capture.read()
        #         if not ref:
        #             raise ValueError("未能正确读取摄像头（视频），请注意是否正确安装摄像头（是否正确填写视频路径）。")
        #         i=0
        #         fps = 0.0
        #         while(True):
        #             t1 = time.time()
        #             # 读取某一帧
        #             ref, frame = capture.read()
        #             if not ref:
        #                 break
        #             # 格式转变，BGRtoRGB
        #             frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        #             # 转变成Image
        #             frame = Image.fromarray(np.uint8(frame))
        #             # 进行检测
        #             frame = np.array(yolo.detect_image(frame))
        #             #RGBtoBGR满足opencv显示格式
        #             frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        #             cv2.imshow("video",frame)
        #             c= cv2.waitKey(1) & 0xff 
        #             if video_save_path!="":
        #                 out.write(frame)
        #             if c==27:
        #                 capture.release()
        #                 break
        #             if c==113:   #如果按下q就截圖儲存
        #                 cv2.imwrite("img/test/test{}.jpg".format(i), frame)   #儲存路徑
        #                 print('ok')
        #                 i=i+1
        #         print("Video Detection Done!")
        #         capture.release()
        #         if video_save_path!="":
        #             print("Save processed video to the path :" + video_save_path)
        #             out.release()
        #         cv2.destroyAllWindows()

        flag, self.image = self.cap.read()
        # # face = self.face_detect.align(self.image)
        # # if face:
        # #     pass
        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # # print(show.shape[1], show.shape[0])
        # # show.shape[1] = 640, show.shape[0] = 480
        self.showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
        # # self.x += 1
        # # self.label_move.move(self.x,100)

        # # if self.x ==320:
        # #     self.label_show_camera.raise_()

    def capx(self):
        FName = fr"images\cap{time.strftime('%Y%m%d%H%M', time.localtime())}"
        # cv2.imwrite(FName + ".jpg", self.image)
        print(FName)
        # self.label_2.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.cap_label.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
        self.showImage.save(FName + ".jpg", "JPG", 100)
        

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"關閉", u"確認關閉?")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'確定')
        cacel.setText(u'取消')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            #             self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    # ex.setStyleSheet("#MainWindow{border-image:url(DD.png)}")
    ex.show()
    sys.exit(App.exec_())
