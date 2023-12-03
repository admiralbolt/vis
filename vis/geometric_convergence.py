import argparse
import math

import pygame

from vis.utils import drawing_utils

parser = argparse.ArgumentParser(description="Cosine**n convergence")
parser.add_argument("--depth", type=int, help="Number of iterations", default=140)
parser.add_argument("--ratio", type=float, help="Ratio to use", default=0.97)
parser.add_argument("--degree", type=float, help="Degree change between steps", default=68.75)

HEIGHT = 1000
WIDTH = 1000
CENTER = pygame.Vector2(WIDTH / 2, HEIGHT / 2)


def cos_convergence(screen: pygame.display, ratio: float=0.95, depth: int=0, degree_step: float=68.75):
  x_scale = (WIDTH / 2) - 5
  y_scale = (HEIGHT / 2) - 5

  points = []
  val = 1
  for i in range(depth):
    degree = i * degree_step * math.pi / 180
    points.append(pygame.Vector2(CENTER.x + math.cos(degree) * x_scale * val, CENTER.y - math.sin(degree) * y_scale * val))
    val *= ratio
  
  screen.fill("black")
  pygame.draw.line(screen, pygame.color.Color(100, 100, 200), start_pos=(0, HEIGHT / 2), end_pos=(WIDTH, HEIGHT / 2))
  pygame.draw.line(screen, pygame.color.Color(100, 100, 200), start_pos=(WIDTH / 2, 0), end_pos=(WIDTH / 2, HEIGHT))
  for i in range(len(points) - 1):
    pygame.draw.line(screen, drawing_utils.get_rainbow(i, depth), start_pos=points[i], end_pos=points[i + 1])
  pygame.display.flip()

if __name__ == "__main__":
  args = parser.parse_args()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  cos_convergence(screen, ratio=args.ratio, depth=args.depth, degree_step=args.degree)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit