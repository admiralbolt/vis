import argparse
from functools import partial

from vis.lib import image_utils


def add_subparsers(parser: argparse.ArgumentParser):
  filter_parser = parser.add_subparsers(title="filter", dest="filter")

  color_pop_parser = filter_parser.add_parser("color_pop", conflict_handler="resolve")
  color_pop_parser.add_argument("--lower_b", type=int, default=0, help="Lower threshold for blue channel.")
  color_pop_parser.add_argument("--lower_g", type=int, default=0, help="Lower threshold for green channel.")
  color_pop_parser.add_argument("--lower_r", type=int, default=0, help="Lower threshold for red channel.")
  color_pop_parser.add_argument("--upper_b", type=int, default=125, help="Upper threshold for blue channel.")
  color_pop_parser.add_argument("--upper_g", type=int, default=125, help="Upper threshold for green channel.")
  color_pop_parser.add_argument("--upper_r", type=int, default=125, help="Upper threshold for red channel.")

  kmeans_parser = filter_parser.add_parser("kmeans", conflict_handler="resolve")
  kmeans_parser.add_argument("--k", type=int, default=10, help="Number of colors to keep in final image.")
  kmeans_parser.add_argument("--max_iter", type=int, default=50, help="Max iterations to use for quantization algorithm.")
  kmeans_parser.add_argument("--epsilon", type=float, default=0.1, help="Epsilon to use for quantization algorithm.")
  
  rainbow_edge_parser = filter_parser.add_parser("rainbow_edge", conflict_handler="resolve")
  rainbow_edge_parser.add_argument("--lower_threshold", type=int, default=50, help="Lower threshold for canny edges.")
  rainbow_edge_parser.add_argument("--upper_threshold", type=int, default=100, help="Upper threshold for canny edges.")

  stained_glass_parser = filter_parser.add_parser("stained_glass", conflict_handler="resolve")
  stained_glass_parser.add_argument("--triangle_size", type=int, default=25, help="Size of triangles for Delaunay triangulation.")
  stained_glass_parser.add_argument("--seed", type=int, default=5, help="Seed to use to alter Delaunay triangulation.")

def call_with_args(args: dict):
  return {
    "color_pop": partial(image_utils.color_pop,
                         lower_b=args.get("lower_b"),
                         lower_g=args.get("lower_g"),
                         lower_r=args.get("lower_r"),
                         upper_b=args.get("upper_b"),
                         upper_g=args.get("upper_g"),
                         upper_r=args.get("upper_r")),
    "kmeans": partial(image_utils.kmeans,
                      k=args.get("k"),
                      max_iter=args.get("max_iter"),
                      epsilon=args.get("epsilon")),
    "rainbow_edge": partial(image_utils.get_canny_edges,
                            lower_threshold=args.get("lower_threshold"),
                            upper_threshold=args.get("upper_threshold")),
    "stained_glass": partial(image_utils.stained_glass, 
                             triangle_size=args.get("triangle_size"),
                             seed=args.get("seed"))
  }[args["filter"]]

FILTERS = {
  "color_pop": image_utils.color_pop,
  "kmeans": image_utils.kmeans,
  "rainbow_edge": image_utils.get_canny_edges,
  "stained_glass": image_utils.stained_glass
}
