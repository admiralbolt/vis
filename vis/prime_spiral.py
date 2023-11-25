import argparse
import pygame

parser = argparse.ArgumentParser(description="Prime spirals!")

HEIGHT = 1000
WIDTH = 1000
CENTER = pygame.Vector2(int(WIDTH / 2), int(HEIGHT / 2))
DOT_COLOR = pygame.color.Color(255, 255, 255)
TOTAL_SIZE = HEIGHT * WIDTH
SCALE = 255.0 / TOTAL_SIZE

# Vectors used for multiplication to move points.
DIRECTIONS = [
  pygame.Vector2(0, -1),
  pygame.Vector2(-1, 0),
  pygame.Vector2(0, 1),
  pygame.Vector2(1, 0)
]

# I've done this before, but can't import my math utils since I'm on plan
# wifi. The gist of the sieve of eratosthenes is basically creating a giant
# memory map and iteratively computing primes. We do this with global state
# and a BEEG boolean list. REMEMBER, YOU MUST CALL is_prime in order starting
# with 2.
sieve_state = [True] * (TOTAL_SIZE + 3)
def is_prime(n):
  if n < 2 or n >= TOTAL_SIZE:
    return False
  
  if sieve_state[n]:
    # Only need to update sieve state when we hit new primes.
    for i in range(n * n, TOTAL_SIZE + 1, n):
      sieve_state[i] = False

  return sieve_state[n]

def take_step(point: pygame.Vector2, step_data: dict) -> pygame.Vector2:
  new_point = point + DIRECTIONS[step_data["direction"]]

  step_data["counter"] += 1
  if step_data["counter"] == step_data["dist"]:
    step_data["counter"] = 0
    step_data["direction"] = (step_data["direction"] + 1) % 4
    step_data["sub_count"] += 1
    if step_data["sub_count"] == 2:
      step_data["dist"] += 1
      step_data["sub_count"] = 0

  return new_point


def prime_spiral(screen: pygame.display):
  step_data = {
    "dist": 1,
    "counter": 0,
    "sub_count": 0,
    "direction": 0
  }
  point = CENTER
  point = take_step(point, step_data)

  screen.fill("black")
  for n in range(2, TOTAL_SIZE):
    should_draw = is_prime(n)
    if should_draw:
      screen.set_at((int(point.x), int(point.y)), pygame.color.Color(140 - int(n * SCALE / 2), int(n * SCALE), 120 + int(n * SCALE / 2)))
    point = take_step(point, step_data)
  
  pygame.display.flip()



if __name__ == "__main__":
  args = parser.parse_args()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  prime_spiral(screen)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
     