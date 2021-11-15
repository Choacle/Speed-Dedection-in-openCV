import cv2


class RectControl:

    def __init__(self):
        self.frame = None
        self.x, self.y = None, None
        self.h = 20
        self.w = 20

    def createRect(self, center, frame):
        self.x, self.y = center
        self.frame = frame
        cv2.rectangle(self.frame, (self.x-self.w, self.y-self.h),
                      (self.x+self.w, self.y+self.h), (0, 255, 0))
        return self.frame

    def checkdims(self, key):
        if self.w <= 0:
            self.w = self.w+1
        if self.h <= 0:
            self.h = self.h+1

    def control(self, key):
        if key == ord('1'):
            if self.w == 10:
                self.w -= 0
            else:
                self.w -= 1
        if key == ord('2'):
            self.w += 1
        if key == ord('3'):
            if self.h == 10:
                self.h -= 0
            else:
                self.h -= 1
        if key == ord('4'):
            self.h += 1

    def get_csv_vals(self, class_name):
        return {'x1': self.x-self.w,
                'y1': self.y-self.h,
                'x2': self.x+self.w,
                'y2': self.y+self.h,
                'Class': class_name}
