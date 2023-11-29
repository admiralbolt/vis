import argparse
import bisect
import operator
import pygame

parser = argparse.ArgumentParser(description="Prime snake!")
parser.add_argument("--points", type=int, help="Number of points to compute!", default=1_000_000)

HEIGHT = 1000
WIDTH = 1000
CENTER = pygame.Vector2(int(WIDTH / 2), int(HEIGHT / 2))
DOT_COLOR = pygame.color.Color(255, 255, 255)
TOTAL_SIZE = HEIGHT * WIDTH
# Vectors used for multiplication to move points.
DIRECTIONS = [
  (0, -1),
  (-1, 0),
  (0, 1),
  (1, 0),
]

sieve_state = [True] * (TOTAL_SIZE + 3)
def is_prime(n, max_n=1_000_000):
  if n < 2 or n >= TOTAL_SIZE:
    return False
  
  if sieve_state[n]:
    # Only need to update sieve state when we hit new primes.
    for i in range(n * n, TOTAL_SIZE + 1, n):
      sieve_state[i] = False

  return sieve_state[n]

def get_color(index, cycle_length=24000):
  # RAINBOW
  step = (index // (cycle_length / 6)) % 6
  pos = index % (cycle_length / 6)
  # Need to linearly rescale our step size down to the range [0-255].
  color_shift = int(pos * (255.0 / (cycle_length / 6)))

  return {
    0: (255, color_shift, 0),
    1: (255 - color_shift, 255, 0),
    2: (0, 255, color_shift),
    3: (0, 255 - color_shift, 255),
    4: (color_shift, 0, 255),
    5: (255, 0, 255 - color_shift)
  }[step]

class Point:

  def __init__(self, index, x, y):
    self.original_index = index
    self.x = x
    self.y = y
    self.color = get_color(index)

  def __lt__(self, obj):
    return self.x < obj.x and self.y < obj.y

def compute_points(number_of_points=1_000_000):
  points = []
  direction = 0
  point = Point(1, int(WIDTH / 2), int(HEIGHT / 2))
  for i in range(1, number_of_points):
    points.append(point)
    if is_prime(i):
      direction = (direction + 1) % 4
    point = Point(i + 1, point.x + DIRECTIONS[direction][0], point.y + DIRECTIONS[direction][1])

  return sorted(points, key=lambda point: (point.x, point.y))

def prime_snake(screen: pygame.display, points, x_values, y_values, xoffset, yoffset):
  # Find all the points that should be displayed.
  min_x = bisect.bisect_left(x_values, xoffset)
  max_x = bisect.bisect_right(x_values, WIDTH + xoffset) - 1
  min_y = bisect.bisect_left(y_values, yoffset)
  max_y = bisect.bisect_right(y_values, HEIGHT + yoffset) - 1
  for index in range(max(min_x, min_y), min(max_x, max_y) + 1):
    point = points[index]
    screen.set_at((point.x - xoffset, point.y - yoffset), point.color)

  pygame.display.flip()

if __name__ == "__main__":
  args = parser.parse_args()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  points = compute_points(number_of_points=args.points)
  x_values = [point.x for point in points]
  y_values = [point.y for point in points]
  xoffset = 0
  yoffset = 0

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
      
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
      xoffset += 25
    elif keys[pygame.K_LEFT]:
      xoffset -= 25
    
    if keys[pygame.K_UP]:
      yoffset -= 25
    elif keys[pygame.K_DOWN]:
      yoffset += 25
      
    screen.fill(color="black")
    prime_snake(screen, points, x_values, y_values, xoffset, yoffset)