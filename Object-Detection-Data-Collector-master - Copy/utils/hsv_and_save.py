import cv2
import argparse


def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)


def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values


def restartTrackbar(range_filter, vals):
    cv2.namedWindow("Trackbars", 0)
    count = 0
    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            print(f"count-->> {vals[count]}")
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars",
                               vals[count], 255, callback)
            count += 1


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--class", default='Random', type=str, help="Object Class"
                    )
    args = vars(ap.parse_args())
    return args
