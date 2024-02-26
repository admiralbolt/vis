import cv2

from multiprocessing import Pool
from progress.bar import Bar

def frame_by_frame_process(input_video, output_video, frame_callback, debug=False):
  """Process a video frame by frame, and generate a new output video."""
  cap = cv2.VideoCapture(input_video)
  total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
  fps = cap.get(cv2.CAP_PROP_FPS)
  height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
  width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

  print(f"{total_frames=}, {fps=}, {height=}, {width=}")

  fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
  writer = cv2.VideoWriter(output_video, fourcc, fps, (int(width), int(height)))

  all_frames = []
  ret, frame = cap.read()
  while ret:
    all_frames.append(frame)
    ret, frame = cap.read()
  cap.release()

  with Pool(processes=16) as pool:
    with Bar("Processing", max=total_frames) as bar:
      for frame in pool.imap(frame_callback, all_frames):
        writer.write(frame)
        bar.next()

  writer.release()

if __name__ == "__main__":
  pass