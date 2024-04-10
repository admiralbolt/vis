import math

import pygame

def get_rainbow(val, max_val=1_000_000):
  """Get a rainbow color by linearly rescaling val => [0, max_val] => [0, 255]"""
  step = (val // (max_val / 6)) % 6
  pos = val % (max_val / 6)
  # Need to linearly rescale our step size down to the range [0-255].
  color_shift = int(pos * (255.0 / (max_val / 6)))

  return {
    0: (255, color_shift, 0),
    1: (255 - color_shift, 255, 0),
    2: (0, 255, color_shift),
    3: (0, 255 - color_shift, 255),
    4: (color_shift, 0, 255),
    5: (255, 0, 255 - color_shift)
  }[step]

# https://github.com/pygame/pygame/issues/3199
# >:(
def draw_line(screen: pygame.Surface, color, x, y, length, angle, width):
  # If either point of our line is out of bounds we want to clip it into bounds.
  p1 = [x, y]
  p2 = [x + length * math.cos(angle), y + length * math.sin(angle)]
  # If our line is entirely out of bounds, don't draw it.
  if (p1[0] <= 0 and p2[0] <= 0) or (p1[0] >= screen.get_width() and p2[1] >= screen.get_width()):
    return
  
  if (p1[1] <= 0 and p2[1] <= 0) or (p1[1] >= screen.get_height() and p2[1] >= screen.get_height()):
    return
  
  # Draw the on screen point first.
  if p1[0] >= 0 and p1[1] >= 0 and p1[0] <= screen.get_width() and p1[1] <= screen.get_height():
    pygame.draw.line(screen, color, p1, p2, width=width)
  else:
    pygame.draw.line(screen, color, p2, p1, width=width)

  # Shift p1 until it's on screen.
  # if p1[1] <= 0 and p2[1] > 0:
  #   p1[0] = x + math.cos(angle) * (-y / math.sin(angle))
  #   p1[1] = 0
  
  # pygame.draw.line(screen, color, p1, p2, width=width)

if __name__ == "__main__":
  pass