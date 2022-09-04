import cv2
cap1 = cv2.VideoCapture("img/test1.mp4")
cap2 = cv2.VideoCapture("img/test2.mp4")

if not cap1.isOpened():
    print("Cannot open camera1")
    exit()
if not cap2.isOpened():
    print("Cannot open camera2")
    exit()

while True:
    ret1, img1 = cap1.read()
    ret2, img2 = cap2.read()
    

    cv2.imshow('test2', img2)
    cv2.imshow("test1",img1)
    if cv2.waitKey(1) == ord('q'):
        break
cap1.release()
cap2.release()
cv2.destroyAllWindows()