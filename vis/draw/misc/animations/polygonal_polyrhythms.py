import argparse
import math
import os

import numpy as np
import pygame


HEIGHT = 1000
WIDTH = 1000
CENTER = (WIDTH / 2, HEIGHT / 2)
SOUND_FOLDER = "/Users/admiralbolt/Music/Logic/KalimbaScales"

def get_sound_file(half_steps_up: int) -> str:
  return os.path.join(SOUND_FOLDER, f"Alloy Lead_{half_steps_up}.wav")

class Polygon:

  points: list[pygame.Vector2]
  last_side: int = -1
  sound: pygame.mixer.Sound

  def __init__(self, radius: float, sides: int, color: tuple[int, int, int], sound_file: str):
    self.radius = radius
    self.sides = sides
    self.color = color
    self.points = []
    for degree in np.arange(0, 360, 360.0 / sides):
      self.points.append(pygame.Vector2(
        CENTER[0] + radius * math.cos((degree) * math.pi / 180),
        CENTER[1] + radius * math.sin((degree) * math.pi / 180)
      ))
    self.degree_cycle = 360 / sides
    self.sound = pygame.mixer.Sound(sound_file)

  def render(self, screen: pygame.Surface, current_seconds: float) -> None:
    pygame.draw.polygon(screen, self.color, self.points, width=5)

    # Degree at which to draw a point. If we make one cycle around the polygon
    # per second, than we need to subdivide one second into 360 degrees....
    degree = current_seconds % 360

    # Guessing where the correct point to place the dot on the polygon should
    # be based on a parabolic function, where the peak is at the midpoint
    # of the degree cycle, and the 0's are at each end.
    which_side = int(degree // self.degree_cycle)
    point1: pygame.Vector2 = self.points[which_side]
    point2: pygame.Vector2 = self.points[(which_side + 1) % self.sides]
    distance = point1.distance_to(point2)
    # ANGLE TO DOES NOT WORK CORRECTLY.
    # FUCK YOU PYGAME.
    if point1.x == point2.x:
      angle_radians = math.pi / 2
    else:
      angle_radians = math.atan((point2.y - point1.y) / (point2.x - point1.x))
    degree_mod_cycle = degree % self.degree_cycle

    x_factor = -1 if point2.x < point1.x else 1
    y_factor = -1 if point2.y < point1.y else 1
    scale_factor = (degree_mod_cycle / self.degree_cycle)

    dot_x = point1.x + x_factor * distance * scale_factor * math.fabs(math.cos(angle_radians))
    dot_y = point1.y + y_factor * distance * scale_factor * math.fabs(math.sin(angle_radians))

    pygame.draw.circle(screen, color=self.color, center=(
      dot_x,
      dot_y,
    ), radius=10)

    if which_side != self.last_side:
      pygame.mixer.Sound.play(self.sound)

    self.last_side = which_side


def animate(polygons: list[Polygon], speed_factor: float=120) -> None:
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  clock = pygame.time.Clock()
  current_seconds = clock.tick(60)

  while True:
    current_seconds = speed_factor * pygame.time.get_ticks() / 1000
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
      
    screen.fill("black")
    for poly in polygons:
      poly.render(screen=screen, current_seconds=current_seconds)
    
    pygame.display.flip()
    clock.tick(60)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Polygonal Polyrhythms")
  args = parser.parse_args()

  pygame.init()
  pygame.mixer.init()

  
  # triangle = Polygon(radius=400, sides=3, color=(180, 80, 0), sound_file=get_sound_file(24))
  # square = Polygon(radius=400, sides=4, color=(0, 80, 250), sound_file=get_sound_file(0))
  # hexagon = Polygon(radius=400, sides=6, color=(240, 240, 0), sound_file=get_sound_file(7))
  # septagon = Polygon(radius=400, sides=7, color=(0, 240, 120), sound_file=get_sound_file(16))
  # thirteen_gon = Polygon(radius=400, sides=13, color=(180, 0, 80), sound_file=get_sound_file(14))

  # animate([triangle, square, hexagon, septagon, thirteen_gon], speed_factor=120)

  # triangle = Polygon(radius=400, sides=3, color=(180, 80, 0), sound_file=get_sound_file(0))
  # square = Polygon(radius=400, sides=4, color=(0, 80, 250), sound_file=get_sound_file(24))
  # pentagon = Polygon(radius=400, sides=5, color=(100, 200, 200), sound_file=get_sound_file(16))
  # hexagon = Polygon(radius=400, sides=6, color=(200, 200, 100), sound_file=get_sound_file(15))

  # animate([triangle, square, pentagon, hexagon], speed_factor=140)

  triangle = Polygon(radius=400, sides=3, color=(180, 80, 0), sound_file=get_sound_file(0))
  square = Polygon(radius=400, sides=4, color=(0, 80, 250), sound_file=get_sound_file(7))
  hexagon = Polygon(radius=400, sides=6, color=(240, 240, 0), sound_file=get_sound_file(14))
  septagon = Polygon(radius=400, sides=7, color=(0, 240, 120), sound_file=get_sound_file(16))
  octagon = Polygon(radius=400, sides=8, color=(0, 255, 255), sound_file=get_sound_file(17))
  
  animate([triangle, square, hexagon, septagon, octagon], speed_factor=140)
