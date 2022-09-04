import cv2

cap = cv2.VideoCapture(0)        #開啟攝像頭
i=0
while(True):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)     #生成攝像頭視窗
    c= cv2.waitKey(1) & 0xff             
    if c==27:
        cap.release()
        break
    if c==113:   #如果按下q就截圖儲存
        cv2.imwrite("img/test/test{}.jpg".format(i), frame)   #儲存路徑
        print('ok')
        i=i+1