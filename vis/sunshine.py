import argparse
import math
import random
import pygame

parser = argparse.ArgumentParser(description="Sunshine!")

HEIGHT = 846
WIDTH = 1504
CENTER = pygame.Vector2(int(WIDTH / 2), int(HEIGHT / 2))
SUN_INNER_RADIUS = 100
SUN_INNER_COLOR = (255, 200, 0)
SUN_ROTATION_SCALING = 20
SUN_RAY_SCALING = 1.5
SUN_RAY_BASE_SPEED = 8

class Ray:

  length: float
  width: float
  color: tuple[int, int, int]
  speed: float
  angle: float
  position: tuple[float, float]

  def __init__(self):
    self.length = random.randint(75, 85) + random.random() 
    self.width = 1 + random.random()
    self.color = (random.randint(230, 255), random.randint(200, 240), 0)
    self.speed = SUN_RAY_BASE_SPEED + random.randint(3, 7) + random.random()
    self.angle = random.randint(0, 360) + random.random()
    self.x_factor = math.cos(self.angle * math.pi / 180)
    self.y_factor = math.sin(self.angle * math.pi / 180)
    self.position = (CENTER.x, CENTER.y)

  def in_bounds(self) -> bool:
    return self.position[0] < WIDTH and self.position[0] >= 0 and self.position[1] < HEIGHT and self.position[1] > 0
  
  def tick(self) -> None:
    self.position = (
      self.position[0] + self.x_factor * self.speed * (1.0 / SUN_RAY_SCALING),
      self.position[1] + self.y_factor * self.speed * (1.0 / SUN_RAY_SCALING)
    )
  
  def render(self, screen: pygame.display, offset: int) -> None:
    points = []
    # Need to draw a rotated rectangle. Close points are spaced a half width
    # away at 90 degrees relative to the target angle.
    points.append((
      self.position[0] + (self.width / 2) * math.cos((self.angle + 90) * math.pi / 180),
      self.position[1] + (self.width / 2) * math.sin((self.angle + 90) * math.pi / 180)
    ))
    # Far points should be full length in the target angle direction.
    points.append((
      points[-1][0] + self.length * self.x_factor,
      points[-1][1] + self.length * self.y_factor
    ))

    # Same but at -90 degrees aka + 270 degrees
    points.append((
      self.position[0] + (self.width / 2) * math.cos((self.angle + 270) * math.pi / 180),
      self.position[1] + (self.width / 2) * math.sin((self.angle + 270) * math.pi / 180)
    ))
    points.append((
      points[-1][0] + self.length * self.x_factor,
      points[-1][1] + self.length * self.y_factor
    ))

    pygame.draw.polygon(screen, self.color, points, width=math.ceil(self.width) + 1)


def render_pokey_sun_bits(screen: pygame.display, degree_offset: float=0, color: tuple=SUN_INNER_COLOR, num_triangles: int=12, center_scaling: float=0.8 * SUN_INNER_RADIUS, length_scaling=0.67 * SUN_INNER_RADIUS) -> None:
  for i in range(num_triangles):
    degree = degree_offset + (i / num_triangles) * 360
    centroid = (
      CENTER.x + center_scaling * math.cos(degree * math.pi / 180),
      CENTER.y + center_scaling * math.sin(degree * math.pi / 180)
    )
    triangle_points = []
    for d in [degree, degree + 140, degree + 220]:
      triangle_points.append((
        centroid[0] + length_scaling * math.cos(d * math.pi / 180),
        centroid[1] + length_scaling * math.sin(d * math.pi / 180)
      ))
    pygame.draw.polygon(screen, color, triangle_points, width=0)


def render_sun(screen: pygame.display, offset: int) -> None:
  # Need to render in reverse order!
  # Render a few sets of triangles pointing outwards.
  render_pokey_sun_bits(screen, degree_offset=offset / SUN_ROTATION_SCALING + 18, color=(250, 150, 0), num_triangles=13, center_scaling=(4/5) * SUN_INNER_RADIUS, length_scaling=0.45 * SUN_INNER_RADIUS)
  render_pokey_sun_bits(screen, degree_offset=offset / SUN_ROTATION_SCALING + 9, color=(250, 180, 0), num_triangles=13, center_scaling=(4/5) * SUN_INNER_RADIUS, length_scaling=0.58 * SUN_INNER_RADIUS)
  render_pokey_sun_bits(screen, degree_offset=offset / SUN_ROTATION_SCALING, color=SUN_INNER_COLOR, num_triangles=13, center_scaling=(4/5) * SUN_INNER_RADIUS, length_scaling=0.7 * SUN_INNER_RADIUS)

  # Render the main circle in the center.
  pygame.draw.circle(screen, SUN_INNER_COLOR, CENTER, SUN_INNER_RADIUS)

  pygame.draw.circle(screen, (250, 195, 0), CENTER, SUN_INNER_RADIUS, width=3)


SKY_COLORS = [
  (80, 180, 255),
  (0, 0, 50),
  (20, 40, 255)
]

STEP_SIZE = 500
TOTAL_STEPS = STEP_SIZE * len(SKY_COLORS)

def get_background_color(offset: int) -> tuple[int, int, int]:
  mod_offset = offset % TOTAL_STEPS
  chunk_pos = mod_offset // STEP_SIZE
  chunk_offset = mod_offset % STEP_SIZE
  # Hey, it's our old friend linear interpolation back again, woweeee.
  scaling_factor = (chunk_offset + 1) / STEP_SIZE

  start_color = SKY_COLORS[chunk_pos]
  end_color = SKY_COLORS[(chunk_pos + 1) % len(SKY_COLORS)]

  color = (
    (end_color[0] - start_color[0]) * scaling_factor + start_color[0],
    (end_color[1] - start_color[1]) * scaling_factor + start_color[1],
    (end_color[2] - start_color[2]) * scaling_factor + start_color[2]
  )
  
  return color

if __name__ == "__main__":
  args = parser.parse_args()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  clock = pygame.time.Clock()

  offset = 0

  rays: list[Ray] = []

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit

    screen.fill(get_background_color(offset=offset))

    for i, ray in enumerate(rays):
      if ray.in_bounds():
        ray.render(screen, offset=i)
        ray.tick()

    rays = [ray for ray in rays if ray.in_bounds()]

    render_sun(screen, offset=offset)

    while len(rays) < 20:
      rays.append(Ray())
    
    pygame.display.flip()

    clock.tick(60)
    offset += 1
