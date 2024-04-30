"""MAKE IT RAIN"""
import argparse
import math
import random

import numpy as np
import pygame

from vis.lib.animation_utils import RenderableAnimation
from vis.lib.math_utils import linear_rescale
from vis.lib.drawing_utils import draw_line

class RainDrop:
  """One little rain drop."""

  done: bool = False

  def __init__(self, x: float, y: float, angle: float, speed: float, length: float, width: float, color=(255, 255, 255)):
    self.x = x
    self.y = y
    self.angle = angle
    self.speed = speed
    self.length = length
    self.width = width
    self.color = color

  def render(self, screen: pygame.Surface):
    draw_line(screen, self.color, self.x, self.y, self.length, self.angle, self.width)
  
  def move(self, screen: pygame.Surface, dt: float):
    self.x += self.speed * math.cos(self.angle) * dt
    self.y += self.speed * math.sin(self.angle) * dt

    self.length -= random.uniform(0.1, 1.4) * dt
    if self.length <= 0:
      self.done = True

    if self.y > screen.get_height() + 1:
      self.done = True

class Rain:
  """Lots of rain drops!"""

  def __init__(self, screen: pygame.Surface, dps: float, rain_gauge: float):
    self.screen = screen
    self.dps = dps
    self.rain_gauge = rain_gauge
    self.rain_meter = 0
    self.rain_drops = []

  def add_raindrop(self, loudness: float):
    length = random.randint(40, 48)
    self.rain_drops.append(RainDrop(
      x=random.randint(0, 1.25 * self.screen.get_width()),
      y=0 - length,
      angle=2 * math.pi * random.randint(90, 110) / 360,
      speed=random.randint(400, 450) + random.random() + 5 * loudness * loudness,
      length=length,
      width=3
    ))

  def update_and_render(self, dt: float, loudness: float):
    self.rain_meter += self.dps * dt
    if self.rain_meter >= self.rain_gauge:
      for _ in range(int(self.rain_meter / self.rain_gauge)):
        self.add_raindrop(loudness=loudness)
      self.rain_meter = 0

    delete_drops = []
    for i, drop in enumerate(self.rain_drops):
      drop.move(self.screen, dt=dt)
      drop.render(self.screen)

      if drop.done:
        delete_drops.append(i)

    for j, i in enumerate(delete_drops):
      del self.rain_drops[i - j]

class Storm(RenderableAnimation):

  rain: Rain

  def __init__(self, audio_file: str, height: int=1080, width: int=1920):
    super().__init__(audio_file=audio_file, height=height, width=width)
    self.rain = Rain(screen=self.screen, dps=0, rain_gauge=0.75)
    self.min_loudness = min(self.aa.loudness)
    self.max_loudness = np.quantile(self.aa.loudness, 0.8)

  def render_frame(self, current_seconds: float):
    loudness = self.aa.loudness[self.aa._get_frame(current_seconds=current_seconds)]
    clipped_loudness = linear_rescale(
      val=loudness,
      old_range=(self.min_loudness, self.max_loudness),
      new_range=(0, 10)
    )
    self.screen.fill("black")
    self.rain.update_and_render(dt=self.dt, loudness=clipped_loudness)
    self.rain.dps = 3 * clipped_loudness * clipped_loudness
    pygame.display.flip()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Rain animation!")
  parser.add_argument("--audio_file", help="Audio file to analyze.", required=True)
  parser.add_argument("--height", default=1080, type=int, help="Height of the video.")
  parser.add_argument("--width", default=1920, type=int, help="Width of the video.")
  parser.add_argument("--output_video", help="The output video to render.")
  parser.add_argument("--save_animation", default=False, action="store_true")
  args = parser.parse_args()

  pygame.init()

  storm = Storm(audio_file=args.audio_file, height=args.height, width=args.width)
  if args.save_animation:
    storm.save_animation(output_video=args.output_video)
    exit()

  storm.play_animation()