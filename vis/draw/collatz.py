import argparse
import collections
import math
import matplotlib.pyplot as plt
import pygame
import pygame.freetype


parser = argparse.ArgumentParser(description="Prime snake!")
parser.add_argument("--width", type=int, help="Width of window!", default=900)
parser.add_argument("--height", type=int, help="Height of window!", default=900)

TEXT_SIZE = 30
FT_FONT = None

def collatz_map(n: int=100_000) -> dict[int, int]:
  """Create a dictionary that contains collatz conjecture mappings like so:

  {
    2: 1,
    3: 10,
    4: 2
  }
  """
  collatz = {}
  collatz[2] = 1
  for i in range(3, n):
    if i in collatz:
      continue

    val = i
    next_val = val
    while next_val not in collatz:
      next_val = val / 2 if val % 2 == 0 else 3 * val + 1
      collatz[val] = next_val
      val = next_val
    
  return collatz

def get_chain(c: dict[int, int], start: int) -> list[int]:
  chain = []
  val = start
  while val != 1:
    chain.append(val)
    val = c[val]
  chain.append(1)
  return chain

def draw_arrow(screen: pygame.display, start: tuple[float, float], end: tuple[float, float], color=(140, 140, 140)):
  pygame.draw.line(screen, color=color, start_pos=start, end_pos=end, width=1)
  points = []
  for degree in [90, 210, 330]:
    points.append(pygame.Vector2(
      end[0] + 5 * math.cos(degree * math.pi / 180),
      end[1] + 5 * math.sin(degree * math.pi / 180)
    ))
  pygame.draw.polygon(screen, color, points, width=0)

def draw_text_in_circle(screen: pygame.display, text: str, position: tuple[float, float], radius: float, circle_color=(60, 80, 100), font_color=(170, 170, 190)):
  pygame.draw.circle(screen, circle_color, position, radius)
  text_size = max(30 - 5 * len(text), 10)
  font = pygame.freetype.SysFont("helvetica", text_size, bold=True)
  text_rect = font.get_rect(text, size=text_size)
  text_rect.center = position
  font.render_to(screen, text_rect, text, font_color)

if __name__ == "__main__":
  pygame.freetype.init()

  c = collatz_map()
  all_chains = [(0, [], 0), (1, [], 0)]
  chains_by_length = collections.defaultdict(list)
  for i in range(2, 20000):
    chain = get_chain(c, i)
    all_chains.append((i, chain, len(chain)))
    chains_by_length[len(chain)].append(chain)

  args = parser.parse_args()
  screen = pygame.display.set_mode((args.width, args.height))
  screen.fill("black")

  FT_FONT = pygame.freetype.SysFont("helvetica", TEXT_SIZE, bold=True)
  circle_radius = 15
  draw_text_in_circle(screen, "1", (args.width - 30, args.height - 30), circle_radius)

  starting_shift = 400

  
  # x, y, angle
  prev_nodes = {}
  prev_nodes[1] = (args.width - 30, args.height - 30, 90)
  circle_radius = 20
  for i in range(2, 19):
    for j, chain in enumerate(chains_by_length[i][::-1]):
      new_number = chain[0]
      prev_node = prev_nodes[chain[1]]
      x = prev_node[0]
      if new_number %2 == 1:
        x -= (400 - 50 * int(i / 3))
      y = prev_node[1] - 50
      prev_nodes[new_number] = (x, y, 90)
      draw_arrow(screen, (x, y), (prev_node[0], prev_node[1]))
      draw_text_in_circle(screen, str(new_number), (x, y), circle_radius)

      



  # x_locations = {}

  # # Start by going through chains by length.
  # for i in range(2, 16):
  #   y = args.height - 30 - 50 * (i - 1)
  #   for j, chain in enumerate(chains_by_length[i][::-1]):
  #     x = args.width / 2 + 50 * int((j + 1) / 2) * (-1) ** j
  #     x_locations[chain[0]] = x
  #     draw_text_in_circle(screen, str(chain[0]), (x, y), circle_radius)
  #     if i <= 2:
  #       continue

  #     draw_arrow(screen, (x, y + circle_radius), (x_locations[chain[1]], y + circle_radius + 7))



  pygame.display.flip()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit




  for i in range(20):
    print(f"CHAIN LENGTH = {i}\n###############")
    print(len(chains_by_length[i]))
    print("--------")
    print(chains_by_length[i])
    print("###########")
    print("\n")

  # x = list(range(2, 1000))
  # y = [len(get_chain(c, i)) for i in x]
  # plt.scatter(x, y, s=[3 for _ in x])
  # plt.xlabel("Starting point")
  # plt.ylabel("Steps to get to 1")
  # plt.show()

  x = list(range(2, 1000))
  max_so_far = 0
  y = []
  for i in x:
    max_of_chain = max(get_chain(c, i))
    if max_of_chain > max_so_far:
      max_so_far = max_of_chain
    y.append(max_so_far)
  plt.plot(x, y, lw=0.5)
  plt.show()

