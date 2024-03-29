import multiprocessing

import cv2
import numpy as np
from progress.bar import Bar

def frame_by_frame_process(input_video, output_video, frame_callback, multi_threaded=False, debug=False):
  """Process a video frame by frame, and generate a new output video."""
  cap = cv2.VideoCapture(input_video)
  total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
  fps = cap.get(cv2.CAP_PROP_FPS)
  height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
  width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

  print(f"{total_frames=}, {fps=}, {height=}, {width=}")

  fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
  writer = cv2.VideoWriter(output_video, fourcc, fps, (int(width), int(height)))

  if multi_threaded:
    all_frames = []
    ret, frame = cap.read()
    while ret:
      all_frames.append(frame)
      ret, frame = cap.read()
    cap.release()

    with multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1) as pool:
      with Bar("Processing", max=total_frames) as bar:
        for frame in pool.imap(frame_callback, all_frames):
          writer.write(frame)
          bar.next()
    writer.release()

    return

  with Bar("Processing", max=total_frames) as bar:
    ret, frame = cap.read()
    while ret:
      bar.next()
      writer.write(frame_callback(frame))
      ret, frame = cap.read()
  cap.release()
  writer.release()


def write_frames_to_video(frames: np.array, output_video: str, fps: int=60):
  """Write image frames to a video file."""
  height, width, channels = frames[0].shape
  fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
  writer = cv2.VideoWriter(output_video, fourcc, fps, (int(width), int(height)))

  for frame in frames:
    writer.write(frame)
  writer.release()

if __name__ == "__main__":
  pass