import cv2
import numpy as np
import random

source_window = "Ahhhh"
im = cv2.imread("/Users/admiralbolt/Downloads/sunset_me.jpg")

def redraw(_):
  ms = cv2.pyrMeanShiftFiltering(im,
                                 sp=cv2.getTrackbarPos("Spatial Window Radius", source_window),
                                 sr=cv2.getTrackbarPos("Color Window Radius", source_window))
  cv2.imshow("ms", ms)

cv2.namedWindow(source_window)
cv2.imshow(source_window, im)

cv2.createTrackbar("Spatial Window Radius", source_window, 50, 50, redraw)
cv2.createTrackbar("Color Window Radius", source_window, 100, 100, redraw)



# gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# gray = cv2.blur(gray, (3,3))

# def threshold_callback(threshold):
#   canny_output = cv2.Canny(gray, threshold, threshold * 2)
#   contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#   drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
#   for i in range(len(contours)):
#       color = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
#       cv2.drawContours(drawing, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)
#   # Show in a window
#   cv2.imshow('Contours', drawing)

# # Trackbar stuff!
# source_window = "Ahhhh"
# cv2.namedWindow(source_window)
# cv2.imshow(source_window, im)

# max_threshold = 255
# threshold = 10

# cv2.createTrackbar("Canny Threshold:", source_window, threshold, max_threshold, threshold_callback)

cv2.waitKey(0)
