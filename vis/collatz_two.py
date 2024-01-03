from pprint import pprint
from matplotlib import pyplot

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

c = collatz_map()

branches_values = {}
leaves_to_branches = {}

branches_values[2] = []
for j in range(1, 20):
  leaf = 2 ** j
  branches_values[2].append(leaf)
  leaves_to_branches[leaf] = 2

for i in range(3, 15000, 2):
  branches_values[i] = []
  for j in range(20):
    leaf = (2 ** j) * i
    branches_values[i].append(leaf)
    leaves_to_branches[leaf] = i

next_branch = {}
for i in range(3, 10000, 2):
  next_value = c[i]
  branch = leaves_to_branches[next_value]
  steps = 0
  while next_value %2 == 0:
    next_value /= 2
    steps += 1
  next_branch[i] = (branch, steps)

x = []
y = []
for key, val in next_branch.items():
  x.append(key)
  y.append(val[0])

# for i in range(3, 1000, 2):
#   print(f"{i} -> {next_branch[i][0]}")

for q in range(201, 231, 2):
  print([int(z) for z in get_chain(c, q) if z % 2 == 1])

# start = 283
# while start != 2:
#   print(start)
#   start = leaves_to_branches[c[start]]

# pyplot.scatter(x, y, s=3)
# pyplot.show()
