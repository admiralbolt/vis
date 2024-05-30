import cv2
import numpy as np
import pdf2image

class LoadMarginCallback:

  top: int = 0
  left: int = 0
  right: int = 0
  bottom: int = 0
  pick_top_left: bool = True

  def __init__(self, image: np.array):
    self.image = image
    self.image = np.hstack([self.image[:, 0:1000], self.image[:, -1000:]])

  def pick_margins(self, event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
      if self.pick_top_left:
        self.left = x
        self.top = y
      else:
        self.right = self.image.shape[1] - x
        self.bottom = self.image.shape[0] - y

  def draw(self, window_name, image):
    new_image = image.copy()
    height, width, channels = new_image.shape
    # Draw top margin line =>
    cv2.line(new_image, (0, self.top), (width, self.top), (0, 255, 0), 1)
    # Draw bottom maring line =>
    cv2.line(new_image, (0, height - self.bottom), (width, height - self.bottom), (0, 255, 0), 1)
    # Draw left margin line =>
    cv2.line(new_image, (self.left, 0), (self.left, height), (0, 255, 0), 1)
    # Draw right margin line =>
    cv2.line(new_image, (width - self.right, 0), (width - self.right, height), (0, 255, 0), 1)

    cv2.imshow(window_name, new_image)

  def load(self):
    pick_margins = "Pick Margins"
    cv2.namedWindow(pick_margins)
    cv2.setMouseCallback(pick_margins, self.pick_margins)
    self.draw(pick_margins, self.image)
    
    while True:
      k = cv2.waitKey(0)
      if k == ord("a"):
        self.pick_top_left = not self.pick_top_left
      elif k == ord("d"):
        self.draw(pick_margins, self.image)
      else:
        break

    cv2.destroyAllWindows()


if __name__ == "__main__":
  pdf_file = "/Users/admiralbolt/Music/Scores/Take Me/cropped/Full score - Take Me = テイク・ミー.pdf"
  im = np.array(pdf2image.convert_from_path(pdf_file, dpi=200)[0])
  lm = LoadMarginCallback(image=im)
  lm.load()

  print(f"{lm.top=}, {lm.left=}, {lm.right=}, {lm.bottom=}")