# PyImageSearch: Object tracking
# Reference: https://www.pyimagesearch.com/wp-content/uploads/2014/11/opencv_crash_course_camshift.pdf

import argparse
import imutils
import cv2
import numpy as np

# current frame in the video that we are processing.
frame = None
# region of interest in the video
roi_points = []
# indicates whether we are currently selecting the object we want to track.
input_mode = False


def select_roi(event, x, y, flags, param):
    global frame, roi_points, input_mode

    if input_mode and event == cv2.EVENT_LBUTTONDOWN and len(roi_points) < 4:
        roi_points.append((x, y))
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv2.imshow("frame", frame)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to video file")
    args = vars(ap.parse_args())

    global frame, roi_points, input_mode

    # if video path was not provided, use camera
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)
    else:
        # load the video
        camera = cv2.VideoCapture(args["video"])

    # set up the mouse callback
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", select_roi)

    # initialize termination criteria
    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    roi_box = None
