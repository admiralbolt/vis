import argparse
import cv2
import math
import numpy as np
import os

parser = argparse.ArgumentParser(description="Interpolate the diff between two images.")
parser.add_argument("--image", help="Image to quantize.")
parser.add_argument("--output", help="Output image.")
parser.add_argument("--k", type=int, help="Number of colors to quantize into.")
parser.add_argument("--max_iter", type=int, default=50, help="Max number of iterations, no clue what it really does.")
parser.add_argument("--epsilon", type=float, default=0.1, help="Required accuracy, no clue what it really does.")


def kmeans_input_colors(image: str="", output: str="", colors: list=[]):
  if not os.path.isfile(image):
    return
  
  def get_closest(pixel):
    min_color = -1
    min_dist = 1000000000
    for i, color in enumerate(colors):
      dist = math.sqrt(
        (color[0] - pixel[0]) ** 2 + 
        (color[1] - pixel[1]) ** 2 + 
        (color[2] - pixel[2]) ** 2
      )   
      if dist < min_dist:
        min_dist = dist
        min_color = color
    return min_color

  im = cv2.imread(image)
  im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
  
  y, x, z = im.shape

  # I vaguely remember there being a faster way of doing these per pixel
  # operations, but don't have wifi so can't google for how to do it.
  # Should also probably be using a faster distance function above.
  for j in range(y):
    for i in range(x):
      im[j, i] = get_closest(im[j, i]) 

  im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
  cv2.imwrite(output, im)

def kmeans(image: str="", output: str="", k: int=10, max_iter: int=50, epsilon: float=0.1):
  if not os.path.isfile(image):
    return
  
  im = cv2.imread(image)
  
  pixel_vals = im.reshape((-1, 3))
  pixel_vals = np.float32(pixel_vals)

  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
  ret, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

  centers = np.uint8(centers)
  segmented_data = centers[labels.flatten()]

  segmented_image = segmented_data.reshape((im.shape))
  cv2.imwrite(output, segmented_image)


if __name__ == "__main__":
  args = parser.parse_args()
  kmeans(image=args.image, output=args.output, k=args.k, max_iter=args.max_iter, epsilon=args.epsilon)
