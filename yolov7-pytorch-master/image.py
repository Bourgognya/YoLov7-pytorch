import cv2

img = cv2.imread("images\cap202208241306.jpg")
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
