import argparse

import cv2

def emboss(plate_file, stamp_file, output_file):
  plate = cv2.imread(plate_file)
  stamp = cv2.imread(stamp_file)
  height, width, channels = stamp.shape
  
  # Create a mask of the stamp that is just the good bits.
  # This will probably need to be file dependent.
  gray = cv2.cvtColor(stamp, cv2.COLOR_BGR2GRAY)
  _, stamp_mask = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
  stamp_mask = cv2.bitwise_not(stamp_mask)
  cv2.imshow("stamp_mask", stamp_mask)

  # Get a place slice that matches the stamp size.
  background = plate[350:350+height, 30:30+width]
  cv2.imshow("background", background)

  mix = cv2.addWeighted(stamp, 0.6, background, 0.4, 0)
  foreground = cv2.bitwise_and(mix, mix, mask=stamp_mask)
  background = cv2.bitwise_and(background, background, mask=cv2.bitwise_not(stamp_mask))
  cv2.imshow("mix", mix)

  final = cv2.add(foreground, background)
  cv2.imshow("final", final)

  cv2.waitKey(0)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Test effect.")
  parser.add_argument("--plate_file", type=str, help="Background plate")
  parser.add_argument("--stamp_file", type=str, help="Stamp")
  parser.add_argument("--output_file", type=str, help="Output file")
  args = parser.parse_args()

  emboss(args.plate_file, args.stamp_file, args.output_file)