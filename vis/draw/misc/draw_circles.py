"""Tiny demo demonstrating mouse callback."""

import numpy as np
import cv2
import random

img = np.zeros((512, 512, 3), np.uint8)

cv2.circle(img, center=(200, 200), radius=100, color=(255, 255, 255), thickness=-1)

def draw_circle(event, x, y, flags, params):
  if event == cv2.EVENT_LBUTTONDOWN:
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    cv2.circle(img, center=(x, y), radius=random.randint(60, 100), color=(r, g, b), thickness=-1)
  
cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_circle)

while True:
  cv2.imshow("image", img)
  k = cv2.waitKey(1)
  if k == ord("s"):
    break 

cv2.destroyAllWindows()

