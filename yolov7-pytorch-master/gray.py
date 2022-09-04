import cv2

# method 1
image = cv2.imread('VOCdevkit/VOC2007/JPEGImages/1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# method 2
#image = cv2.imread('lena.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.imwrite('gary.jpg', image)
