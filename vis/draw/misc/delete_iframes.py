import argparse
import subprocess

import cv2
import numpy as np
from progress.bar import Bar

def get_iframes(input: str):
  result = subprocess.check_output(["ffprobe", "-select_streams", "v", "-show_frames", "-show_entries", "frame=pict_type", "-of", "csv", input])
  frames = result.split(b"\n")
  indexes = []
  for i, frame_info in enumerate(frames):
    if b"I" in frame_info:
      indexes.append(i)
  return indexes

def delete_iframes(input: str, output: str):
  cap = cv2.VideoCapture(input)
  total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
  fps = cap.get(cv2.CAP_PROP_FPS)
  height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
  width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

  fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
  writer = cv2.VideoWriter(output, fourcc, fps, (int(width), int(height)))

  iframe_indexes = get_iframes(input)
  print(iframe_indexes)
  iframe_indexes.append(-1)
  next_iframe = 0
  current_frame = 0
  with Bar("Processing", max=total_frames) as bar:
    ret, frame = cap.read()
    while ret:
      bar.next()
      if current_frame == iframe_indexes[next_iframe]:
        next_iframe += 1
        print(f"skipping frame: {current_frame}")
      else:
        writer.write(frame)
      ret, frame = cap.read()
      current_frame += 1
  cap.release()
  writer.release()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Storm animation!")
  parser.add_argument("--input", help="Input video!", required=True)
  parser.add_argument("--output", help="Output video!", required=True)
  args = parser.parse_args()
  delete_iframes(args.input, args.output)