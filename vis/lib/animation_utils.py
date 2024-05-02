from abc import ABC, abstractmethod

import cv2
import pygame
import numpy as np
from progress.bar import Bar

from vis.lib.audio_utils import AudioAnalyzer

class RenderableAnimation(ABC):
  """A renderable animation!

  The render_frame() function shuold be overriden, and the animation can either
  be played or rendered directly to a 60fps video.
  """

  aa: AudioAnalyzer
  screen: pygame.Surface
  width: int
  height: int
  dt: float
  current_frame: int

  def __init__(self, audio_file: str, height: int=1080, width: int=1920):
    self.aa = AudioAnalyzer(audio_file)
    self.aa.process_features()
    self.screen = pygame.display.set_mode((width, height))
    self.width = width
    self.height = height
    self.dt = 0
    self.current_frame = 0

  @abstractmethod
  def render_frame(self, current_seconds: float):
    pass

  def play_animation(self):
    """Play the animation!"""
    clock = pygame.time.Clock()

    pygame.mixer.music.load(self.aa.file_name)
    pygame.mixer.music.play(0)

    while True:
      if not pygame.mixer.music.get_busy():
        raise SystemExit
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          raise SystemExit
      
      current_seconds = pygame.mixer_music.get_pos() / 1000.0
      self.render_frame(current_seconds=current_seconds)
      self.dt = clock.tick(60) / 1000.0
      self.current_frame += 1

  def save_animation(self, output_video: str):
    """Save the animation to a file!"""
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    writer = cv2.VideoWriter(output_video, fourcc, 60, (self.width, self.height))
    total_frames = int(self.aa.duration_seconds * 60)
    self.dt = 1.0 / 60

    with Bar("Processing", max=total_frames) as bar:    
      for current_seconds in np.arange(0, self.aa.duration_seconds, (1.0 / 60)):
        self.render_frame(current_seconds=current_seconds)
        writer.write(cv2.cvtColor(pygame.surfarray.pixels3d(self.screen.copy()).swapaxes(0, 1), cv2.COLOR_RGB2BGR))
        self.current_frame += 1
        bar.next()

    writer.release()