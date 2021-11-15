import cv2
import numpy as np
import copy
import datetime

# upload video
cap = cv2.VideoCapture(0)

# reading two frames
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():

    # get diference between two frames
    diff = cv2.absdiff(frame1, frame2)

    # convert diference in gray
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # treshold
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(thresh, None, iterations=5)

    # define contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        cnt_area = cv2.contourArea(contour)

        if cnt_area < 1000 or cnt_area > 4000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255))

        now = datetime.datetime.now()
        print(now)
        print(cnt_area)

    # cv2.drawContours(frame1, contours, -1, (0,0,255), 1)

    # show frames
    cv2.imshow('frame', frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()