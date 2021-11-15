import cv2
from imutils.video import VideoStream
import time
from operator import xor
import numpy as np
import imutils
from utils.rect_control import RectControl
from utils.hsv_and_save import *
import csv
import os
import copy
import pyautogui
import pyads

plc = pyads.Connection('5.18.142.230.1.1', 801)
plc.open()

csv_dict_old = 0
img_count = 0
range_filter = 'HSV'
setup_trackbars(range_filter)
isTrackbar = True

args = get_arguments()

labels = ['Filename', 'x1', 'y1', 'x2', 'y2', 'Class']

file_exists = os.path.isfile('coords_labels.csv')
with open('coords_labels.csv', 'a') as file:
    if not file_exists:
        writer = csv.DictWriter(file, fieldnames=labels)
        writer.writeheader()

rect = RectControl()

vs = VideoStream(src=0).start()
while True:

    frame = vs.read()
    frame = cv2.flip(frame, 1)
    frame_orig = copy.deepcopy(frame)
    frame_to_thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if isTrackbar:
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(
            range_filter)
    thresh = cv2.inRange(
        frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    if isTrackbar == True:
        thresh = np.stack((thresh, )*3, axis=-1)
        frame = np.concatenate((frame, thresh), axis=1)

    else:
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                frame = rect.createRect(center, frame)

        frame = frame[:, :640, :]

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('Q'):
        vs.stop()
        break
    if key == ord('t') or key == ord('T'):
        if isTrackbar:
            vX = get_trackbar_values(range_filter)
            cv2.destroyWindow('Trackbars')
            print(f"vals ---> {vX}")
        if not isTrackbar:
            restartTrackbar(range_filter, vX)

        isTrackbar = not isTrackbar

    if key == ord('s') or key == ord('S'):
        csv_dict = rect.get_csv_vals(args['class'])
        print(csv_dict)
        if csv_dict_old != 0:
            #if csv_dict_old['x1'] < csv_dict['x1']:
            #    print("1")
            #    plc.write_by_name("MAIN.veri", False, pyads.PLCTYPE_BOOL)
            #if csv_dict_old['x1'] > csv_dict['x1']:
            #    print("0")
            #    plc.write_by_name("MAIN.veri2", False, pyads.PLCTYPE_BOOL)
            #if csv_dict_old['y1'] < csv_dict['y1']:
            #    print("2")
            #if csv_dict_old['y1'] > csv_dict['y1']:
            #    print("3")
            if  csv_dict_old['y1'] > 210:
                plc.write_by_name("MAIN.yOne", True, pyads.PLCTYPE_BOOL)
            elif csv_dict_old['y1'] < 190:
                plc.write_by_name("MAIN.yTwo", True, pyads.PLCTYPE_BOOL)
            else:
                plc.write_by_name("MAIN.yOne", False, pyads.PLCTYPE_BOOL)
                plc.write_by_name("MAIN.yTwo", False, pyads.PLCTYPE_BOOL)

        print(csv_dict_old)
        csv_dict_old = csv_dict

    if key == ord('c') or key == ord('C'):
        args['class'] = input("Please enter new class name : ")
    rect.control(key)

plc.close()
cv2.destroyAllWindows()
