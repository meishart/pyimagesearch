import numpy as np
import cv2

#vcap = cv2.VideoCapture("rtsp://foo:foo123@192.168.2.8:554/videoMain")
#vcap = cv2.VideoCapture(0)
while(1):
    ret, frame = vcap.read()
    print("Ret is {}".format(ret))
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)