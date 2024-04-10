import argparse

import aubio
import numpy as np
import pyaudio
import pygame
from pynput.keyboard import Key, Controller


class AudioListener:
  """Listen to some audio!"""

  p: pyaudio.PyAudio
  name: str
  device_index: int = -1
  device_info: dict = {}
  tolerance: float
  fft_size: int
  buffer_size: 1024

  def __init__(self, name: str, tolerance: float=0.8, buffer_size: int=1024, fft_size: int=4096):
    self.p = pyaudio.PyAudio()
    self.name = name
    self.fft_size = fft_size
    self.tolerance = tolerance
    self.buffer_size = buffer_size
    self.pitch = aubio.pitch("default", fft_size, self.buffer_size)
    self.pitch.set_unit("midi")
    self.pitch.set_tolerance(self.tolerance)
    
  def initialize(self):
    """Initialize audio listener, returns true if device is found."""
    for i in range(self.p.get_device_count()):
      device_info = self.p.get_device_info_by_index(i)
      print(i, device_info)
      if device_info["name"] == self.name:
        self.device_index = i
        self.device_info = device_info
        self.stream = self.p.open(
          format=pyaudio.paFloat32,
          input_device_index=self.device_index,
          channels=1,
          rate=44100,
          input=True,
          frames_per_buffer=self.buffer_size,
        )
        return True
    return False
  
  def detect_pitch(self) -> tuple[float, float]:
    buffer = self.stream.read(self.buffer_size, exception_on_overflow=False)
    signal = np.fromstring(buffer, dtype=np.float32)
    return (self.pitch(signal)[0], self.pitch.get_confidence())
  

# # PONG CONFIG
# keyboard_ranges = [
#   {
#     "key": Key.down,
#     "range": [30, 60]
#   },
#   {
#     "key": Key.up,
#     "range": [70, 100]
#   }
# ]
  
# QWOP CONFIG
# keyboard_ranges = [
#   {
#     "key": "q",
#     "range": [50, 64.9],
#   },
#   {
#     "key": "w",
#     "range": [65.1, 69.9],
#   },
#   {
#     "key": "o",
#     "range": [70.1, 74.9],
#   },
#   {
#     "key": "p",
#     "range": [75.1, 85]
#   }
# ]
  
# THNAAAAAKE
keyboard_ranges = [
  {
    "key": Key.down,
    "range": [45, 64.9],
  },
  {
    "key": Key.left,
    "range": [65.1, 69.9],
  },
  {
    "key": Key.right,
    "range": [70.1, 76.9],
  },
  {
    "key": Key.up,
    "range": [77.1, 100]
  }
]


def map_pitch_into_range(list_of_ranges, pitch):
  for i, keybind in enumerate(list_of_ranges):
    if keybind["range"][0] <= pitch <= keybind["range"][1]:
      return i
  return -1

def debug_display(input_device: str, tolerance: float=0.8, width: int=500, height: int=500, frames: int=10):
  pygame.init()

  screen = pygame.display.set_mode((width, height))
  clock = pygame.time.Clock()

  audio_listener = AudioListener(name=input_device)
  if not audio_listener.initialize():
    print("COULD NOT FIND DEVICE")
    return
  
  font = pygame.font.Font("freesansbold.ttf", 32)

  current_range = -1
  frame_count = 0
  keyboard = Controller()
  held_key = None

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
      
    screen.fill("black")
    pitch_value, confidence = audio_listener.detect_pitch()

    range_index = map_pitch_into_range(keyboard_ranges, pitch_value)
    if current_range == range_index and range_index != -1:
      frame_count += 1
    else:
      if held_key:
        keyboard.release(held_key)
        held_key = None
      frame_count = 0

    if frame_count == frames:
      key = keyboard_ranges[current_range]["key"]
      keyboard.press(key)
      held_key = key
      frame_count = 0

    current_range = range_index

    text = font.render(f"Pitch Value: {round(pitch_value)}", True, (100, 100, 255), (50, 50, 50))
    text_rect = text.get_rect()
    text_rect.left = 10
    text_rect.top = 20

    conf = font.render(f"Confidence Value: {confidence}", True, (100, 100, 255), (50, 50, 50))
    conf_rect = conf.get_rect()
    conf_rect.left = 10
    conf_rect.top = 80

    if held_key:
      button = font.render(str(held_key), True, (100, 100, 255), (50, 50, 50))
      button_rect = button.get_rect()
      button_rect.left = 200
      button_rect.top = 200
      screen.blit(button, button_rect)

    screen.blit(text, text_rect)
    screen.blit(conf, conf_rect)

    pygame.display.flip()
    clock.tick(60)



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="PITCH DETECTION DEBUG.")
  parser.add_argument("--input_device", type=str, help="Name of input device to listen to.")
  parser.add_argument("--tolerance", type=float, help="TOLERANCE", default=0.8)
  parser.add_argument("--frames", type=int, default=6)
  args = parser.parse_args()

  debug_display(input_device=args.input_device, frames=args.frames)
