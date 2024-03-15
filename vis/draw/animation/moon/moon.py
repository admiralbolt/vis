import argparse
import math
import random

import cv2
import numpy as np
import pygame
from progress.bar import Bar

from vis.lib.audio_utils import AudioAnalyzer
from vis.lib.drawing_utils import get_rainbow
from vis.lib.math_utils import linear_rescale
from vis.lib.video_utils import write_frames_to_video

HEIGHT = 1080
WIDTH = 1920

star = cv2.imread("star_mask.png")
_, star_mask = cv2.threshold(cv2.cvtColor(star, cv2.COLOR_BGR2GRAY), 125, 255, cv2.THRESH_BINARY)
center = tuple(np.array(star_mask.shape[1::-1]) / 2)

def apply_glow(image: np.array, kernel: tuple[int, int] = (17, 17)) -> np.array:
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  _, foreground_mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
  foreground = cv2.bitwise_and(image, image, mask=foreground_mask)

  blur = cv2.GaussianBlur(image, ksize=kernel, sigmaX=10, sigmaY=10)
  blur = cv2.blur(blur, ksize=(kernel[0] - 6, kernel[1] - 6))
  background = cv2.bitwise_and(blur, blur, mask=np.bitwise_not(foreground_mask))
  return cv2.add(foreground, background)

class Star:

  x: int
  y: int
  speed_x: float
  speed_y: float
  color: tuple[int, int, int]
  size_multiplier: float
  created_at: float
  time_to_live: float
  base_mask: np.array
  image: np.array

  def __init__(self, created_at: float, color: tuple[int, int, int], x: int = 0, y: int = 0, size_multiplier: float=1.5):
    self.color = color
    self.x = x or random.randint(0, 1920)
    self.y = y or random.randint(0, 1080)
    self.speed_x = -3 + random.randint(0, 5) + random.random()
    self.speed_y = 3 + random.randint(2, 3) + random.random()
    self.size_multiplier = size_multiplier
    self.time_to_live = random.randint(1, 2) + random.random() + random.random()
    self.created_at = created_at
    rotation_matrix = cv2.getRotationMatrix2D(center, angle=random.randint(1, 72), scale=1)
    self.base_mask = cv2.warpAffine(src=star_mask, M=rotation_matrix, dsize=(star_mask.shape[1], star_mask.shape[0]))

  def _redraw(self, alpha: int):
    canvas = np.zeros((star_mask.shape[0], star_mask.shape[1], 4), dtype=np.uint8)
    canvas[:] = (self.color + (alpha,))
    canvas = cv2.bitwise_and(canvas, canvas, mask=self.base_mask)
    canvas = cv2.resize(canvas, (0, 0), fx=self.size_multiplier, fy=self.size_multiplier)
    self.image = canvas

  def render(self, screen: pygame.Surface, current_seconds: float):
    alpha = linear_rescale((self.created_at + self.time_to_live) - current_seconds, (0, self.time_to_live), (0, 255))
    self._redraw(alpha=alpha)

    surface = pygame.image.frombuffer(self.image, (self.image.shape[1], self.image.shape[0]), "RGBA")
    surface.convert_alpha()
    screen.blit(surface, (self.x, self.y))
    self.x += self.speed_x
    self.y += self.speed_y

  def is_finished(self, current_seconds: float):
    return (self.created_at + self.time_to_live) <= current_seconds

def draw_moon(screen: pygame.Surface, moon_color: tuple[int, int, int], loudness: float) -> None:
  """Draw a moon by drawing two overlapping circles, with one being the background color."""
  canvas = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
  # Color needs to be BGR for opencv.
  cv2.circle(canvas, center=(220, 220), radius=170, color=(moon_color + (1, )), thickness=-1)
  cv2.circle(canvas, center=(270, 220), radius=160, color=(0, 0, 0, 0), thickness=-1)
  # Adjust glow size depending on volume!
  size = 17 + int(loudness * 2)
  if size % 2 == 0:
    size -= 1
  moon = apply_glow(canvas, kernel=(size, size))
  surface = pygame.image.frombuffer(moon, screen.get_size(), "RGBA")
  surface.convert_alpha()
  screen.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

class MoonAnimation:

  stars: list[Star]
  aa: AudioAnalyzer
  current_color: tuple = (20, 20, 80)
  direction: int = 3

  def __init__(self, audio_file: str):
    self.frames = []
    self.stars = []
    self.aa = AudioAnalyzer(file_name=audio_file)
    self.aa.process_features()
    pass

  def render(self, screen: pygame.Surface, current_seconds: float):
    clipped_loudness = linear_rescale(
      val=self.aa.get_loudness(current_seconds=current_seconds),
      old_range=(-40, -10),
      new_range=(0, 10)
    )
    frequency_slice = self.aa.get_frequency_slice(current_seconds=current_seconds)
    for i, freq_db in enumerate(frequency_slice):
      scaled_db = linear_rescale(freq_db, old_range=(-15, 0), new_range=(0, 100))
      if scaled_db > 0 and random.random() < 0.2:
        self.stars.append(Star(color=get_rainbow(scaled_db, 100), x=(i * 100) % 1920, created_at=current_seconds, size_multiplier=0.1 + 0.04 * random.random() + 0.001 * scaled_db))

    if self.aa.on_beat(current_seconds=current_seconds, width=0.08):
      r, g, b = self.current_color
      b += self.direction
      if b >= 160 or b <= 80:
        self.direction *= -1
      self.current_color = (r, g, b)

    
    screen.fill(self.current_color)
    draw_moon(screen, moon_color=(255, 245, 190), loudness=clipped_loudness)
    cleanup_indexes = []
    for i, star in enumerate(self.stars):
      star.render(screen, current_seconds=current_seconds)
      if star.is_finished(current_seconds=current_seconds):
        cleanup_indexes.append(i)

    for j, i in enumerate(cleanup_indexes):
      del self.stars[i - j]
      
    pygame.display.flip()

def moon_loop(audio_file: str, output_video: str, animate: bool=True):
  pygame.init()
  screen = pygame.display.set_mode((1920, 1080))
  clock = pygame.time.Clock()
  moon = MoonAnimation(audio_file)

  if not animate:
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    writer = cv2.VideoWriter(output_video, fourcc, 60, (WIDTH, HEIGHT))
    total_frames = int(moon.aa.duration_seconds * 60)

    with Bar("Processing", max=total_frames) as bar:    
      for current_seconds in np.arange(0, moon.aa.duration_seconds, (1.0 / 60)):
        moon.render(screen, current_seconds=current_seconds)
        writer.write(cv2.cvtColor(pygame.surfarray.pixels3d(screen.copy()).swapaxes(0, 1), cv2.COLOR_RGB2BGR))
        bar.next()

    writer.release()
    return

  pygame.mixer.music.load(moon.aa.file_name)
  pygame.mixer.music.play(0)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
    
    current_seconds = pygame.mixer_music.get_pos() / 1000.0
    moon.render(screen, current_seconds=current_seconds)
    clock.tick(60)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Moon animation!")
  parser.add_argument("--audio_file", help="Audio file to analyze!", required=True)
  parser.add_argument("--output_video", help="Output movie to write!", required=True)
  parser.add_argument("--animate", default=False, action="store_true")
  args = parser.parse_args()

  moon_loop(args.audio_file, args.output_video, animate=args.animate)

  