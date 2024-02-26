import cv2
import numpy as np
import random
from scipy.spatial import Delaunay

FILTERS = [
  "rainbow_edge",
  "stained_glass"
]

def get_canny_edges(image: np.array, lower_threshold: int=50, upper_threshold: int=100, r=None, g=None, b=None) -> np.array:
  """Get rainbow colored edges from canny edge detection."""
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

class DelaunauyTriangulation:

  vertices: np.array
  tri: Delaunay
  masks: list[np.array]

  def __init__(self, vertices: np.array, tri: Delaunay, masks: list[np.array]):
    self.vertices = vertices
    self.tri = tri
    self.masks = masks


def get_delaunay_triangulation(width: int, height: int, triangle_size: int=200) -> DelaunauyTriangulation:
  """Get Delaunay triangulation of a grid."""
  triangle_size = 50
  vertical_slices = int(height / triangle_size)
  horizontal_slices = int(width / triangle_size)
  rng_height_bound = int(height / (vertical_slices * 3)) + 1
  rng_width_bound = int(width / (horizontal_slices * 3)) + 1
  vertices = np.array([[0, 0]], dtype=np.uint8)

  for i in range(horizontal_slices + 1):
    for j in range(vertical_slices + 1):
      if i == 0 and j == 0:
        continue
      no_offset = any([i == 0, i == horizontal_slices, j == 0, j == vertical_slices])
      x_offset = 0 if no_offset else random.randint(-rng_width_bound, rng_width_bound)
      y_offset = 0 if no_offset else random.randint(-rng_height_bound, rng_height_bound)
      x = int((i / horizontal_slices) * width) + x_offset
      y = int((j / vertical_slices) * height) + y_offset
      vertices = np.append(vertices, [[x, y]], axis=0)

  tri = Delaunay(vertices)
  masks = []
  for simplice in tri.simplices:
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, [vertices[simplice]], color=255)
    masks.append(mask)

  return DelaunauyTriangulation(vertices=vertices, tri=tri, masks=masks)

def stained_glass(image: np.array, dt: DelaunauyTriangulation) -> np.array:
  """Apply stained glass effect based on Delaunay triangulation."""
  height, width, _ = image.shape
  final = np.zeros((height, width, 3), dtype=np.uint8)

  for simplice, mask in zip(dt.tri.simplices, dt.masks):
    mean_color = cv2.mean(image, mask=mask)
    cv2.fillPoly(final, [dt.vertices[simplice]], color=mean_color)
    cv2.polylines(final, [dt.vertices[simplice]], True, (0, 0, 0), 2)

  return final
