import argparse
import math

import numpy as np
import pygame

parser = argparse.ArgumentParser(description="F R A C T A L S")
parser.add_argument("--sides", type=int, help="Number of sides", default=7)
parser.add_argument("--depth", type=int, help="Number of iterations", default=5)
parser.add_argument("--rotate", default=False, action="store_true", help="SPIN THE BOARD")

HEIGHT = 1000
WIDTH = 1000
CENTER = (WIDTH / 2, HEIGHT / 2)

def linear_rescale(val, val_min, val_max, range_min, range_max) -> float:
  return int(range_min + ((range_max - range_min) * (val - val_min)) / ((val_max - val_min) or 1))

def get_polygon_points(radius: float, sides: int, rotation: float=0) -> list[pygame.Vector2]:
  """Get points for a polygon inscribed in a circle.

  We can do this by getting {sides} number of points evenly spaced around a 
  circle of the input radius.
  """
  points = []
  for degree in np.arange(0, 360, 360.0 / sides):
    points.append(pygame.Vector2(
      CENTER[0] + radius * math.cos((degree + rotation) * math.pi / 180),
      CENTER[1] + radius * math.sin((degree + rotation) * math.pi / 180)
    ))
  return points

def draw_fractal(screen: pygame.display, sides: int, depth: int, max_radius: float, global_rotation: float = 0):
  rotation = 0
  start_color = pygame.color.Color(20, 140, 255)
  end_color = pygame.color.Color(140, 40, 240)
  for i in range(depth):
    radius = max_radius if i == 0 else radius * math.cos((180.0 / sides) * math.pi / 180)
    points = get_polygon_points(radius, sides, rotation=(rotation + global_rotation + i * 5))
    # Generate color based on linear rescaling of the radius.
    color = pygame.color.Color(
      linear_rescale(max_radius - radius, 20, max_radius, start_color.r, end_color.r),
      linear_rescale(max_radius - radius, 20, max_radius, start_color.g, end_color.g),
      linear_rescale(max_radius - radius, 20, max_radius, start_color.b, end_color.b),
    )
    pygame.draw.polygon(screen, color, points, width=max(1, 4 - int(i / 6)))
    rotation += 360.0 / (sides * 2)

def animate(sides: int, depth: int, rotate: bool=False):
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  clock = pygame.time.Clock()
  last_updated = clock.tick(60)
  i = 0

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
      
    screen.fill("black")
    draw_fractal(screen, sides, depth, max_radius=460, global_rotation=(i / 4.0) if rotate else 0)
    pygame.display.flip()
    i = (i + 1) % 1440
    pygame.time.delay(20)


if __name__ == "__main__":
  args = parser.parse_args()
  animate(args.sides, args.depth, rotate=args.rotate)
