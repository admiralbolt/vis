import argparse
import math

import numpy as np
import pygame

parser = argparse.ArgumentParser(description="F R A C T A L S")
parser.add_argument("--size", type=float, help="Size of initial triangle", default=800)
parser.add_argument("--depth", type=int, help="Number of iterations", default=7)

HEIGHT = 1000
WIDTH = 1000
CENTER = pygame.Vector2(WIDTH / 2, HEIGHT / 2 + 100)

LINE_COLOR = pygame.color.Color(255, 0, 0)

def get_line_color(depth: int) -> pygame.color.Color:
  return pygame.color.Color(255, int(255 * depth / args.depth), 9 * depth)

def compute_points(center: pygame.Vector2, radius: float, degrees: list[int]) -> list[pygame.Vector2]:
  """Inscribe points in a circle with radius r at each degree specified."""
  points = []
  for degree in degrees:
    points.append(pygame.Vector2(
      center.x + radius * math.cos(degree * math.pi / 180),
      center.y + radius * math.sin(degree * math.pi / 180)
    ))
  return points

def sierpinski(screen: pygame.display, depth: int, size: float):
  """Triangles!

  Render in reverse order so bigger triangles take priority
  """
  all_polygons = []
  screen.fill("black")
  radius = size * math.sqrt(2) / 2
  first_triangle_points = compute_points(CENTER, radius, degrees=[30, 150, 270])
  centers = [CENTER]
  radius = radius / 2
  for i in range(depth):
    new_centers = []
    for center in centers:
      points = compute_points(center, radius, degrees=[90, 210, 330])
      all_polygons.append((points, i))
      new_centers.extend(compute_points(center, radius, degrees=[30, 150, 270]))
    
    # Then update vals for next iter.
    radius = radius / 2
    centers = new_centers

  all_polygons.reverse()
  for polygon, i in all_polygons:
    pygame.draw.polygon(screen, get_line_color(i), polygon, width=max(1, 3 - int(i / 3)))
  
  pygame.draw.polygon(screen, LINE_COLOR, first_triangle_points, width=4)

  pygame.display.flip()


if __name__ == "__main__":
  args = parser.parse_args()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
      
    sierpinski(screen, args.depth, args.size)