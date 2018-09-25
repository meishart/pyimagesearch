import numpy as np
import cv2
cap = cv2.VideoCapture("rtsp://moo:moo123@192.168.1.106:554/videoMain")
#cap = cv2.VideoCapture(0)

fps = cap.get(cv2.CAP_PROP_FPS)
print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fps = cap.get(cv2.CAP_PROP_FPS)
print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

cap.release()
cv2.destroyAllWindows()

