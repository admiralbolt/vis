

def linear_rescale(val: float, old_range: tuple[float, float], new_range: tuple[float, float]):
  """Linearly rescale a value from one range to another."""
  scaled = new_range[0] + (new_range[1] - new_range[0]) * (val - old_range[0]) / (old_range[1] - old_range[0])
  # Clip if values are outside of the range.
  return min(max(scaled, new_range[0]), new_range[1])