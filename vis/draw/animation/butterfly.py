"""MAKE IT RAIN"""
import argparse
import collections
from typing import Any
import random

import cv2
import numpy as np
import pygame

from vis.lib.animation_utils import RenderableAnimation
from vis.lib.math_utils import linear_rescale

butterfly_sprite = {
  "file": "/Users/admiralbolt/Movies/misc/images/butterfly_animation_sheet.png",
  "height": 25,
  "width": 30,
  "images_per_animation": 3,
  "animation_order": [0, 1, 2, 1],
  "number_of_sprites": 120
}

background_image_path = "/Users/admiralbolt/Movies/misc/images/dictionary_breathe_adjusted.jpeg"

class Butterfly:

  def __init__(self, images: list[np.array], animation_order: list[int]):
    self.images = images
    self.animation_order = animation_order
    self.frames_per_image = random.randint(20, 30)

  def create_animation(self, x: float = None, y: float = None):
    return ButterflyAnimation(
      butterfly=self,
      x=x or random.randint(0, 10),
      y=y or random.randint(-25, 1100),
      vx=random.randint(51, 56) + random.random(),
      vy=random.randint(-6, 5) + random.random()
    )

class ButterflyAnimation:

  def __init__(self, butterfly: Butterfly, x: int, y: int, vx: float, vy: float):
    self.butterfly = butterfly
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.frames_per_image = 30 - int(2 * (vx - 51))
    self.total_frames = self.frames_per_image * len(self.butterfly.animation_order)
    self.random_offset = random.randint(0, self.total_frames)
    self.done = False

  def get_image_from_frame(self, frame_number: int):
    image_index = (frame_number % self.total_frames) // self.frames_per_image
    return self.butterfly.images[self.butterfly.animation_order[image_index]]

  def update(self, fps=60):
    self.x += self.vx / fps
    self.y += self.vy / fps
    if self.x >= 1920:
      self.done = True

    if self.y >= 1080 or self.y <= -25:
      self.done = True

  def render(self, screen: pygame.Surface, frame_number: int):
    image = self.get_image_from_frame(frame_number=frame_number + self.random_offset)
    surface = pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "BGRA")
    surface.convert_alpha()
    screen.blit(surface, (self.x, self.y))


def load_sprites(sprite_info: dict[str, Any]) -> list[Butterfly]:
  butterflies = []
  sprite_sheet = cv2.imread(sprite_info["file"], cv2.IMREAD_UNCHANGED)
  height, width, channels = sprite_sheet.shape

  b, g, r, a = cv2.split(sprite_sheet)
  a[a > 0] = 205

  sprite_sheet = cv2.merge((b, g, r, a))

  images = []

  for h in range(0, height, sprite_info["height"]):
    for w in range(0, width, sprite_info["width"]):
      if len(butterflies) >= sprite_info["number_of_sprites"] / sprite_info["images_per_animation"]:
        return butterflies

      images.append(cv2.resize(sprite_sheet[h:h+sprite_info["height"], w:w+sprite_info["width"]], (0, 0), fx=1.5, fy=1.5))
      if len(images) == sprite_info["images_per_animation"]:
        butterflies.append(Butterfly(images=images, animation_order=sprite_info["animation_order"]))
        images = []

  return butterflies


class ButterflyVideo(RenderableAnimation):

  def __init__(self, audio_file: str, height: int=1080, width: int=1920):
    super().__init__(audio_file=audio_file, height=height, width=width)
    self.min_loudness = min(self.aa.loudness)
    self.max_loudness = np.quantile(self.aa.loudness, 0.8)
    self.background_image = cv2.imread(background_image_path)
    self.background_surface = pygame.image.frombuffer(self.background_image.tostring(), self.background_image.shape[1::-1], "BGR")
    self.background_surface.convert()
    self.all_butterflies = load_sprites(butterfly_sprite)
    self.butterflies: list[ButterflyAnimation] = []
    self.butterfly_meter = 0
    self.per_band = collections.defaultdict(float)
    self.time_between = 0.5

  def render_frame(self, current_seconds: float):
    loudness = self.aa.loudness[self.aa._get_frame(current_seconds=current_seconds)]
    clipped_loudness = linear_rescale(
      val=loudness,
      old_range=(self.min_loudness, self.max_loudness),
      new_range=(0, 10)
    )

    frequency_slice = self.aa.get_frequency_slice(current_seconds=current_seconds)
    for i, freq_db in enumerate(frequency_slice):
      scaled_db = linear_rescale(freq_db, old_range=(-30, 0), new_range=(0, 100))

      if scaled_db > 40 and current_seconds > (self.per_band[i] + self.time_between):
        self.butterflies.append(random.choice(self.all_butterflies).create_animation(y=1080-i * 25 + random.randint(-10, 10)))
        self.per_band[i] = current_seconds

    self.screen.blit(self.background_surface, (0, 0))

    delete_butterflies = []
    for i, butterfly in enumerate(self.butterflies):
      butterfly.update()
      butterfly.render(self.screen, frame_number=self.current_frame)

      if butterfly.done:
        delete_butterflies.append(i)

    pygame.display.flip()

    for j, i in enumerate(delete_butterflies):
      del self.butterflies[i - j]

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Rain animation!")
  parser.add_argument("--audio_file", help="Audio file to analyze.", required=True)
  parser.add_argument("--height", default=1080, type=int, help="Height of the video.")
  parser.add_argument("--width", default=1920, type=int, help="Width of the video.")
  parser.add_argument("--output_video", help="The output video to render.")
  parser.add_argument("--save_animation", default=False, action="store_true")
  args = parser.parse_args()
  
  pygame.init()

  butterfly = ButterflyVideo(audio_file=args.audio_file, height=args.height, width=args.width)
  if args.save_animation:
    butterfly.save_animation(output_video=args.output_video)
    exit()

  butterfly.play_animation()