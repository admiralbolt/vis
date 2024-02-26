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

if __name__ == "__main__":
  pass