import argparse
import cv2
import imageio
import numpy as np
import os

parser = argparse.ArgumentParser(description="Interpolate the diff between two images.")
parser.add_argument("--start", help="Starting image")
parser.add_argument("--end", help="Ending image")
parser.add_argument("--output", help="Path to output file.")
parser.add_argument("--step", type=float, default=0.05, help="Step size between images.")
parser.add_argument("--bpm", type=float, help="Beats per minute!")

FPS = 60

def interpolate_diff(start_image_path: str="", end_image_path: str="", output: str="", step: float=0.05, bpm: float=140):
  start = cv2.imread(start_image_path)
  end = cv2.imread(end_image_path)

  # Need to convert beats per minute => seconds for each image.
  bps = bpm / 60.0
  time_per_image = (1.0 / bps) * 4
  frames_per_image = int(time_per_image * FPS)
  print(frames_per_image)


  # Resize the end image to match the start.
  end = cv2.resize(end, (start.shape[1], start.shape[0]))

  fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
  writer = cv2.VideoWriter(output, fourcc, FPS, (start.shape[1], start.shape[0]))

  for mix in np.arange(0, 1 + step, step):
    print(mix)
    im = cv2.addWeighted(start, mix, end, 1 - mix, 0)
    for _ in range(frames_per_image):
      writer.write(im)

  writer.release()

  # images = []
  # duration = []
  # for mix in np.arange(0, 1 + step, step):
  #   images.append(cv2.cvtColor(cv2.addWeighted(start, mix, end, 1 - mix, 0), cv2.COLOR_BGR2RGB))
  #   duration.append(time_per_frame)
  # imageio.mimsave(output, images, duration=duration)


if __name__ == "__main__":
  args = parser.parse_args()
  if not os.path.isfile(args.start) or not os.path.isfile(args.end):
    print("--start and --end must be real files.")
    quit()

  interpolate_diff(start_image_path=args.start, end_image_path=args.end, output=args.output, step=args.step, bpm=args.bpm)
  

  

  