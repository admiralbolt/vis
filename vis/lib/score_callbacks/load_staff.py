import cv2
import numpy as np
import pdf2image

class LoadStaffCallback:

  top: int = 0
  height: int = 0
  pick_top: bool = True

  def __init__(self, image: np.array):
    self.image = image

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

  def load(self):
    pick_margins = "Pick Staff"
    cv2.namedWindow(pick_margins)
    cv2.setMouseCallback(pick_margins, self.pick_margins)
    self.draw(pick_margins, self.image)
    
    while True:
      k = cv2.waitKey(0)
      if k == ord("a"):
        self.pick_top = not self.pick_top
      elif k == ord("d"):
        self.draw(pick_margins, self.image)
      else:
        break
    
    cv2.destroyAllWindows()


if __name__ == "__main__":
  pdf_file = "/Users/admiralbolt/Music/Scores/Take Me/cropped/Full score - Take Me = テイク・ミー.pdf"
  im = np.array(pdf2image.convert_from_path(pdf_file, dpi=200)[0])
  ls = LoadStaffCallback(image=im)
  ls.load()

  print(f"{ls.top=}, {ls.height=}")