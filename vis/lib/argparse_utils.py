import argparse
from functools import partial

from vis.lib import image_utils


def add_subparsers(parser: argparse.ArgumentParser):
  filter_parser = parser.add_subparsers(title="filter", dest="filter")
  
  rainbow_edge_parser = filter_parser.add_parser("rainbow_edge", conflict_handler="resolve")
  rainbow_edge_parser.add_argument("--lower_threshold", type=int, default=50, help="Lower threshold for canny edges.")
  rainbow_edge_parser.add_argument("--upper_threshold", type=int, default=100, help="Upper threshold for canny edges.")

  stained_glass_parser = filter_parser.add_parser("stained_glass", conflict_handler="resolve")
  stained_glass_parser.add_argument("--triangle_size", type=int, default=25, help="Size of triangles for Delaunay triangulation.")
  stained_glass_parser.add_argument("--seed", type=int, default=5, help="Seed to use to alter Delaunay triangulation.")

def call_with_args(args: dict):
  return {
    "rainbow_edge": partial(image_utils.get_canny_edges,
                            lower_threshold=args.get("lower_threshold"),
                            upper_threshold=args.get("upper_threshold")),
    "stained_glass": partial(image_utils.stained_glass, 
                             triangle_size=args.get("triangle_size"),
                             seed=args.get("seed"))
  }[args["filter"]]

FILTERS = {
  "rainbow_edge": image_utils.get_canny_edges,
  "stained_glass": image_utils.stained_glass
}
