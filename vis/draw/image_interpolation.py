import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(description="Interpolate the diff between two images.")
parser.add_argument("--images", type=str, nargs="+", help="Starting image")
parser.add_argument("--output", help="Path to output file.")
parser.add_argument("--step", type=float, default=0.05, help="Step size between images.")
parser.add_argument("--bpm", type=float, help="Beats per minute!")
parser.add_argument("--mult", default=4, type=float, help="Multiplier. Default is one image shift per beat. Multiplier of 4 means one image shift every 4 beats.")
parser.add_argument("--fps", default=60, type=int, help="Frames per second.")

def interpolate_diff(image_paths: list[str], output: str="", step: float=0.05, mult: float=4, bpm: float=140, fps: int=60):
  images = [cv2.imread(path) for path in image_paths]
  start = images[0]

  # Need to convert beats per minute => seconds for each image.
  bps = bpm / 60.0
  time_per_image = (1.0 / bps) * mult
  print(time_per_image * fps)
  frames_per_image = round(time_per_image * fps)
  print(frames_per_image)

  # Resize all images to match the start.
  for i in range(1, len(images)):
    images[i] = cv2.resize(images[i], (start.shape[1], start.shape[0]))

  fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
  writer = cv2.VideoWriter(output, fourcc, fps, (start.shape[1], start.shape[0]))

  for i in range(0, len(images) - 1):
    start = images[i]
    end = images[i + 1]
    for mix in np.arange(0, 1, step):
      im = cv2.addWeighted(start, 1 - mix, end, mix, 0)
      for _ in range(frames_per_image):
        writer.write(im)

  writer.release()


if __name__ == "__main__":
  args = parser.parse_args()

  interpolate_diff(image_paths=args.images, output=args.output, step=args.step, mult=args.mult, bpm=args.bpm, fps=args.fps)
