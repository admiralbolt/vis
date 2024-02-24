import cv2
import numpy as np
import random

def get_canny_edges(image, lower_threshold=50, upper_threshold=100, r=None, g=None, b=None):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  canny_output = cv2.Canny(gray, lower_threshold, upper_threshold)
  contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
  for i in range(len(contours)):
    cr = r if r is not None else random.randint(0, 256)
    cg = g if g is not None else random.randint(0, 256)
    cb = b if b is not None else random.randint(0, 256)
    cv2.drawContours(drawing, contours, i, (cr, cg, cb), 2, cv2.LINE_8, hierarchy, 0)
  return drawing
