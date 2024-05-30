import os

import cv2
import numpy as np

# Vertical line filtering params.
# The target percentage of pixels we want to identify a bar line.
VLINE_PERCENT = [0.98, 1]

class LoadBarlinesCallback:

  bar_positions: list[int]

  def __init__(self, cropped_image: np.array, staff_image: np.array):
    self.cropped_image = cropped_image
    self.staff_image = staff_image
    self.bar_positions = []

  def pick_margins(self, event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
      if self.pick_top:
        diff = self.top - y
        self.top = y
        self.height -= diff
      else:
        self.height = y - self.top

  def draw(self, window_name, image):
    new_image = image.copy()
    height, width, channels = new_image.shape
    # Draw top margin line =>
    cv2.line(new_image, (0, self.top), (width, self.top), (0, 255, 0), 1)
    # Draw bottom maring line =>
    cv2.line(new_image, (0, self.top + self.height), (width, self.top + self.height), (0, 255, 0), 1)

    cv2.imshow(window_name, new_image)

  def get_vertical_lines(self):
    gray = cv2.cvtColor(self.staff_image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)

    # We want to really accent the straight vertical lines, so we want to create
    # a kernel that is a single straight vertical line.
    kernel = np.array([
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
    ], dtype=np.uint8)
    accent = cv2.morphologyEx(invert, cv2.MORPH_ERODE, kernel)
    _, accent = cv2.threshold(accent, 0, 255, cv2.THRESH_BINARY)
    
    # 1) Find all vertical lines.
    num_pixels = np.count_nonzero(accent, axis=0)
    vertical_line_positions = []
    for x, p in enumerate(num_pixels):
      pct = p / accent.shape[0]
      if VLINE_PERCENT[0] <= pct <= VLINE_PERCENT[1]:
        vertical_line_positions.append(x)

    # 2) Filter down vertical lines to a single value i.e. if we have multiple
    # vertical lines in columns next to each other, we only want to see a 
    # single value.
    final_positions = []

    last_col = None
    for col in vertical_line_positions:
      if not last_col:
        last_col = col
        final_positions.append(col)
        continue

      if col > last_col + 2:
        final_positions.append(col)

      last_col = col 

    return final_positions

  def load(self):
    vertical_line_positions = self.get_vertical_lines()
    bar_line_positions = []

    with_lines = self.cropped_image.copy()
    for x in vertical_line_positions:
      cv2.line(with_lines, (x, 0), (x, with_lines.shape[0]), (0, 255, 0), 2)

    bar_line_window = "Is it a barline? (y/n)"
    cv2.namedWindow(bar_line_window)

    # Go through each of the vertical lines, and ask is it a barline.
    for col in vertical_line_positions:
      # Draw in a window around the vertical line.
      min_x = max(col - 500, 0)
      max_x = min(col + 500, with_lines.shape[1])
      highlight = with_lines.copy()
      cv2.line(highlight, (col, 0), (col, with_lines.shape[0]), (0, 180, 255), 3)
      cv2.imshow(bar_line_window, highlight[:, min_x:max_x])

      k = cv2.waitKey(0)
      if k == ord("y"):
        bar_line_positions.append(col)
    
    cv2.destroyAllWindows()
    self.bar_positions = bar_line_positions