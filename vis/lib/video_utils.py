import cv2
import time

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

  with Bar("Processing", max=total_frames) as bar:
    ret, frame = cap.read()
    while ret:
      loop_start = time.time()
      writer.write(frame_callback(frame))

      bar.next()
      ret, frame = cap.read()
      if debug:
        print(f"Loop took {time.time() - loop_start}s")

  cap.release()
  writer.release()
