import librosa
import math
import numpy as np
import pygame

from vis.lib.audio_utils import AudioAnalyzer
from vis.lib.math_utils import linear_rescale
from vis.lib.drawing_utils import get_rainbow

from pprint import pprint

def to_db(val):
  return 20 * math.log(val, 10)

audio_analyzer = AudioAnalyzer(file_name="Insomnia.wav")
audio_analyzer.process_features()

# print(audio_analyzer.tempo)
# print(audio_analyzer.beats)
# print(librosa.frames_to_time(audio_analyzer.beats, sr=audio_analyzer.sample_rate))
# exit()

pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w)
screen_h = int(infoObject.current_w/2)

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])

t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(audio_analyzer.file_name)
pygame.mixer.music.play(0)

# bar_width = int(screen_w / len(frequencies))
bar_width = 3
min_decible = -80
max_decible = 0
decible_ratio = 700 / 80

# Run until the user asks to quit
running = True
while running:

  t = pygame.time.get_ticks()
  deltaTime = (t - getTicksLastFrame) / 1000.0
  getTicksLastFrame = t

  # Did the user click the window close button?
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Fill the background with black.
  screen.fill((0, 0, 0))

  current_seconds = pygame.mixer.music.get_pos() / 1000.0

  if audio_analyzer.on_beat(current_seconds):
    print(f"CURRENT SECONDS: {current_seconds}")
    print()

  # Get the frequency db slice based on the current pos of the mixer:
  slice = audio_analyzer.get_frequency_slice(current_seconds=current_seconds)
  loudness = audio_analyzer.get_loudness(current_seconds=current_seconds)

  clipped_loudness = linear_rescale(loudness, old_range=(-40, -10), new_range=(0, 100))
  pygame.draw.rect(screen, get_rainbow(clipped_loudness, 100), (0, 0, (clipped_loudness) * 10, 200))

  max_index = len(slice) - 1
  # DRAW!
  for i, freq_db in enumerate(slice):
    height = (80 + freq_db) * decible_ratio
    pygame.draw.rect(screen, get_rainbow(i, max_index), (bar_width * i, 700 - height, bar_width, height))

  # Flip the display
  pygame.display.flip()

# Done! Time to quit.
pygame.quit()