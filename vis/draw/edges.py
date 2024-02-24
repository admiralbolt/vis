import cv2
import numpy as np
import random

input_video = "/Users/admiralbolt/Movies/Instagram/MISC/My Foolish Heart.mp4"

cap = cv2.VideoCapture(input_video)
count = 0
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

print(total_frames)
print(fps)
print(height)
print(width)

fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
writer = cv2.VideoWriter("/tmp/edges.mp4", fourcc, fps, (int(width), int(height)))

print("HMMMMM")
first_frame = None

while cap.isOpened():
  ret, frame = cap.read()
  if first_frame is None:
    first_frame = frame]
  # Process frame here.
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  canny_output = cv2.Canny(gray, 50, 100)
  contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
  for i in range(len(contours)):
    color = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
    cv2.drawContours(drawing, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)
  writer.write(drawing)

  count += 1
  if count == total_frames:
    break

cap.release()
writer.release()