import cv2
import numpy as np

WINDOW = "Mean Shift"
cv2.namedWindow(WINDOW)
cv2.createTrackbar("SP", WINDOW, 0, 100, lambda x: x)
cv2.createTrackbar("SR", WINDOW, 0, 100, lambda x: x)

im = cv2.imread("/Users/admiralbolt/Pictures/Hrmmphn.jpg")
shifted = im


def redraw():
  sp = cv2.getTrackbarPos("SP", WINDOW)
  sr = cv2.getTrackbarPos("SR", WINDOW)
  shifted = cv2.pyrMeanShiftFiltering(im, sp=sp, sr=sr)
  cv2.imshow(WINDOW, np.hstack((im, shifted)))

while True:
  k = cv2.waitKey(0)
  if k == ord('d'):
    redraw()
  else:
    quit()

