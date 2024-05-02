import argparse

import cv2


def emboss(background_image, foreground_image, output_image):
  background = cv2.imread(background_image)
  foreground = cv2.imread(foreground_image)
  height, width, channels = foreground.shape

  background = background[:height, :width]

  # Mask our foreground image.
  foreground_gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
  foreground_invert = cv2.bitwise_not(foreground_gray)
  _, foreground_mask = cv2.threshold(foreground_invert, 40, 255, cv2.THRESH_BINARY)  

  mix = cv2.addWeighted(foreground, 0.6, background, 0.4, 0)

  mix_masked = cv2.bitwise_and(mix, mix, mask=foreground_mask)
  background_masked = cv2.bitwise_and(background, background, mask=cv2.bitwise_not(foreground_mask))

  final = cv2.add(mix_masked, background_masked)
  cv2.imshow("final", final)
  cv2.waitKey(0)



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="")
  parser.add_argument("--background", type=str, help="Background image.")
  parser.add_argument("--foreground", type=str, help="Foreground image.")
  parser.add_argument("--output", type=str, help="Output image.")
  args = parser.parse_args()
  
  emboss(args.background, args.foreground, args.output)