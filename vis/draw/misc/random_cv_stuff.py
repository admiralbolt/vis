import random
import time

import cv2
import numpy as np

def item_access():
  """Access pixels via item/itemset()."""
  im = np.zeros((800, 800, 3), dtype=np.uint8)
  for i in range(50, 100, 1):
    for j in range(50, 100, 1):
      im.itemset((i, j, 0), random.randint(120, 200))
      im.itemset((i, j, 1), random.randint(120, 200))
      im.itemset((i, j, 2), random.randint(120, 200))

  return im
   
def manual_access():
  """Turns out, manual access instead of using the item methods IS faster."""
  im = np.zeros((800, 800, 3), dtype=np.uint8)
  for i in range(50, 100, 1):
    for j in range(50, 100, 1):
      im[i, j] = [random.randint(120, 200), random.randint(120, 200), random.randint(120, 200)]
  return im

def np_add():
  """Messing with direct adding instead of cv2.adding."""
  im1 = cv2.imread("/Users/admiralbolt/scratch/misc_images/cc.jpeg")
  im2 = cv2.imread("/Users/admiralbolt/scratch/misc_images/image_1.jpg")
  im2 = cv2.resize(im2, (im1.shape[1], im1.shape[0]))
  cv2.imshow("im1", im1)
  cv2.imshow("im2", im2)
  cv2.imshow("ADD", im1 + im2)
  cv2.waitKey(0)

def convolve():
  """CONVOLUTION"""
  im2 = cv2.imread("/Users/admiralbolt/scratch/misc_images/image_1.jpg")
  # kernel = np.array([
  #   [2, 1, 0, -1, -2],
  #   [2, 1, 0, -1, -2],
  #   [2, 1, 0, -1, -2],
  #   [2, 1, 0, -1, -2],
  #   [2, 1, 0, -1, -2]
  # ])
  kernel = np.array([
    [2, 2, 2, 2, 2],
    [2, -3, -3, -3, 2],
    [2, -3, -8, -3, 2],
    [2, -3, -3, -3, 2],
    [2, 2, 2, 2, 2],
  ])
  dst = cv2.filter2D(im2, -1, kernel)
  cv2.imshow("dst", dst)
  cv2.waitKey(0)



def time_n_calls(fn, n: int) -> float:
  if n <= 0:
    return 0

  total = 0
  for i in range(n):
    s = time.time()
    fn()
    total += time.time() - s
  return total

def time_a_function(fn):
  for i in [5, 10, 25, 50, 100]:
    t = time_n_calls(fn, i)
    if t >= 0.2:
      return t / i

  return t


if __name__ == "__main__":
  # print(f"item_access={time_a_function(item_access)}")
  # print(f"manual access={time_a_function(manual_access)}")
  # np_add()
  convolve()