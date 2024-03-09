import argparse
import os
import math

import aubio
import matplotlib.pyplot as plt
import numpy as np
import pygame
import pylab as pl
from scipy.io import wavfile
from scipy.fftpack import fft

from vis.utils import drawing_utils

parser = argparse.ArgumentParser(description="Audio visualizer!")
parser.add_argument("--file", type=str, help="Path to file to analyze", required=True)
parser.add_argument("--time_slice", type=float, help="The width at which we integrate!", default=0.1)

HEIGHT = 1000
WIDTH = 1000
CENTER = pygame.Vector2(WIDTH / 2, HEIGHT / 2)

if __name__ == "__main__":
  args = parser.parse_args()
  if not os.path.isfile(args.file):
    print("Ain't no way dawg, pick a file that's real you fuck.")
    exit()

  sample_rate, audio_data = wavfile.read(args.file)
  sample_interval = 1.0 / sample_rate
  print(sample_rate)
  print(audio_data.shape)
  audio_length = audio_data.shape[0] / sample_rate
  print(f"Audio Length: {audio_length}s")

  sample_range = np.arange(0, audio_length, args.time_slice)
  total_samples = len(sample_range)
  sample_size = int(sample_rate * args.time_slice)

  for i in range(1, total_samples):
    single_sample_data = audio_data[i * sample_size:(i + 1) * sample_size, 0]
    N = len(single_sample_data)
    T = 1.0 / sample_rate
    y_freq = fft(single_sample_data)

    for i, freq in enumerate(y_freq):
      print(i, abs(freq))

    domain = len(y_freq) // 2
    print(f"{domain=}")
    print(f"sample_rate / 2 = {sample_rate // 2}")
    print(f"N /2 = {N // 2}")
    print(y_freq)
    print(abs(y_freq[:domain]))
    # x_freq = np.linspace(0, sample_rate // 2, N // 2)
    x_freq = np.linspace(0, 1000, N // 2)
    print(x_freq)
    plt.plot(x_freq, 20 * np.log10(np.abs(y_freq[:domain])), lw=0.15)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Frequency Amplitude")
    plt.show()



  exit()

  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  cos_convergence(screen, ratio=args.ratio, depth=args.depth, degree_step=args.degree)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit 