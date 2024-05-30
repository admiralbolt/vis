import bisect
import dataclasses
import glob
import json
import math
import os
import shutil

import cv2
import numpy as np
import pdf2image
import PIL

from vis.lib.score_callbacks import load_barlines, load_margins, load_staff


# LIMITS ARE MEANT TO BROKEN.
# TO GO EVEN FURTHER BEYOND!!!
PIL.Image.MAX_IMAGE_PIXELS = 999999999999999999

@dataclasses.dataclass
class ScoreOptions:
  """Class for keeping track of options for score parsing."""
  top_margin: int = 100
  bottom_margin: int = 100
  left_margin: int = 100
  right_margin: int = 100
  staff_margin: int = 0
  staff_height: int = 0
  bar_positions: list[int] = dataclasses.field(default_factory=lambda: [])
  width: int = 0
  invert: bool = False
  transparent: bool = False
  from_bars: list[int] = dataclasses.field(default_factory=lambda: [])

  def to_json(self):
    return json.dumps(dataclasses.asdict(self), indent=2)
  
  def from_json(data):
    return ScoreOptions(**data)


class ScoreParser:

  pdf_file: str
  options: ScoreOptions
  num_slices: int

  def __init__(self, score_dir: str, gen_options: bool=False, debug: bool=False):
    self.score_dir = score_dir
    self.options_file = os.path.join(score_dir, "options.json")
    self.debug = debug
    self.gen_options = gen_options
    self._initialize()

  def _initialize(self):
    self._load_score()
    self._load_options()
    self.cropped_image = self.image[self.options.top_margin:self.image.shape[0] - self.options.bottom_margin, self.options.left_margin:self.image.shape[1] - self.options.right_margin]
    self.num_slices = int(math.ceil(self.cropped_image.shape[1] / self.options.width))
    self.debug_folder = os.path.join(self.cropped_folder, "debug")
    # Cleanup old png files.
    for f in glob.glob(os.path.join(self.cropped_folder, "*.png")):
      os.remove(f)

    if os.path.isdir(self.debug_folder):
      shutil.rmtree(self.debug_folder)

    if self.debug:
      os.makedirs(self.debug_folder)

  def _load_score(self):
    """Validate expected setup."""
    if not os.path.isdir(self.score_dir):
      print(f"Can't find directory {self.score_dir}")
      exit()

    self.cropped_folder = os.path.join(self.score_dir, "cropped")
    if not os.path.isdir(self.cropped_folder):
      print(f"Can't find directory {self.cropped_folder}")
      exit()

    pdfs = glob.glob(os.path.join(self.cropped_folder, "*.pdf"))
    if len(pdfs) == 0:
      print("No PDF files in sub folder.")
      exit()
    
    self.pdf_file = pdfs[0]
    self.image = np.array(pdf2image.convert_from_path(self.pdf_file, dpi=200)[0])

  def _load_options(self):
    if self.gen_options or not os.path.exists(self.options_file):
      self.generate_options()
      return
        
    with open(self.options_file, "r") as rh:
      self.options = ScoreOptions.from_json(json.load(rh))

  def generate_options(self):
    self.options = ScoreOptions()
    # Load margins.
    lm = load_margins.LoadMarginCallback(image=self.image)
    lm.load()
    self.options.left_margin = lm.left
    self.options.right_margin = lm.right
    self.options.top_margin = lm.top
    self.options.bottom_margin = lm.bottom

    self.cropped_image = self.image[self.options.top_margin:self.image.shape[0] - self.options.bottom_margin, self.options.left_margin:self.image.shape[1] - self.options.right_margin]

    # Load just the staff.
    ls = load_staff.LoadStaffCallback(image=self.image[self.options.top_margin:self.image.shape[0] - self.options.bottom_margin, self.options.left_margin:self.options.left_margin + 1000])
    ls.load()
    self.options.staff_margin = ls.top
    self.options.staff_height = ls.height

    self.staff_image = self.cropped_image[self.options.staff_margin:self.options.staff_margin + self.options.staff_height, :]

    # Pick out the barlines!
    lb = load_barlines.LoadBarlinesCallback(cropped_image=self.cropped_image, staff_image=self.staff_image)
    lb.load()
    self.options.bar_positions = lb.bar_positions

    # Ask some questions about other options.
    width = input("Input Slice width(default=1920): ")
    self.options.width = 1920 if not width else int(width)

    invert = input("Invert (default=False): ")
    self.options.invert = not not invert

    transparent = input("Transparent (default=False): ")
    self.options.transparent = not not transparent
    
    with open(self.options_file, "w") as wh:
      wh.write(self.options.to_json())


  def write_chunk(self, x, i):
    chunk_data = self.cropped_image[:, x:x + self.options.width]
    cv2.imwrite(os.path.join(self.cropped_folder, f"cropped_part_{i}.png"), cv2.bitwise_not(chunk_data) if self.options.invert else chunk_data)

  def slice(self):
    self.write_chunk(0, 0)
    i = 1
    x = self.options.width
    while x < self.cropped_image.shape[1]:
      # We want to display the bar line, so give a tiny bit of offset.
      b = bisect.bisect(self.options.bar_positions, x)
      x = self.options.bar_positions[bisect.bisect(self.options.bar_positions, x) - 1] - 20
      self.write_chunk(x, i)
      x += self.options.width
      i += 1

      if i >= 150:
        print("Unbound loop, stopping.")
        break

    # Last bit won't start on a barline, but should be width exactly still.
    self.write_chunk(self.cropped_image.shape[1] - self.options.width, i - 1)

    # If specific bars are set, render from those positions.
    for from_bar in self.options.from_bars:
      self.write_chunk(self.options.bar_positions[from_bar -1] - 20, f"bar_{from_bar}")

    
