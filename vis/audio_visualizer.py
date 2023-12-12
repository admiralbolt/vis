import argparse
import os
import math

import aubio
import matplotlib.pyplot as plt
import numpy as np
import pygame
import pylab as pl
from scipy.io import wavfile

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

  bucket_size = 5
  buckets = 16

  # frequencies = []
  # for i in sample_range:
  #   # Convert the samples back into usuable indicies.
  #   sample_start = int(i * sample_rate)
  #   sample_end = int((i + args.slice_time) * sample_rate)
  #   signal = audio_data[sample_start:sample_end]
  #   # If we have two channels of data, average them.
  #   if audio_data.shape[1] == 2:
  #     signal = signal.sum(axis = 1) / 2
  #   secs = (sample_end - sample_start) / sample_rate
  #   t = np.arange(0, secs, sample_interval)

  #   # The following section is copy pasted because I can't be bothered to 
  #   # understand it at the current moment in time.
  #   FFT = abs(np.fft(signal))
  #   FFT_side = FFT[range(int((sample_end - sample_start)/2))] # one side FFT range
  #   freqs = np.fftpack.fftfreq(signal.size, t[1]-t[0])
  #   fft_freqs = np.array(freqs)
  #   freqs_side = freqs[range(int((sample_end - sample_start)/2))] # one side frequency range
  #   fft_freqs_side = np.array(freqs_side)

  #   # Put things in buckets.
  #   FFT_side = FFT_side[0:bucket_size*buckets]
  #   fft_freqs_side = fft_freqs_side[0:bucket_size*buckets]
  #   FFT_side = np.array([int(sum(FFT_side[current: current+bucket_size])) for current in range(0, len(FFT_side), bucket_size)])
  #   fft_freqs_side = np.array([int(sum(fft_freqs_side[current: current+bucket_size])) for current in range(0, len(fft_freqs_side), bucket_size)])

  #   # Normalize from 0-1... I guess?
  #   max_value = max(FFT_side)
  #   if (max_value != 0):
  #     FFT_side_norm = FFT_side / max_value

  #   frequencies.append(FFT_side_norm)

  #   pl.plot(t, FFT_side_norm)
  #   pl.xlabel("Frequency(Hz)")

  # p = 20 * np.log10(np.abs(np.fft.rfft(audio_data[:2048, 0])))
  # f = np.linspace(0, sample_rate/2.0, len(p))
  # pl.plot(f, p)
  # pl.xlabel("Frequency(Hz)")
  # pl.ylabel("Power(dB)")
  # pl.show()
  signal = np.mean(audio_data[:int(args.time_slice * sample_rate)], axis=1)
  # ft = np.fft.fft(signal)
  # freq = np.fft.fftfreq(len(ft), d=args.time_slice)

  # plt.subplot(211)
  # plt.plot(freq, ft.real, label="Real part")
  # plt.xlim(-50,50)
  # plt.ylim(-600,600)
  # plt.legend(loc=1)
  # plt.title("FFT in Frequency Domain")

  # plt.subplot(212)
  # plt.plot(freq, ft.imag,label="Imaginary part")
  # plt.legend(loc=1)
  # plt.xlim(-50,50)
  # plt.ylim(-600,600)
  # plt.xlabel("frequency (Hz)")
  # plt.show()

  # print(freq)


  for i in sample_range:
    # Convert the samples back into usuable indicies.
    sample_start = int(i * sample_rate)
    sample_end = int((i + args.time_slice) * sample_rate)
    print(f"{sample_start=}, {sample_end=}, Total Length: {sample_end - sample_start}, About the same as: {args.time_slice * sample_rate}")
    signal = np.mean(audio_data[sample_start:sample_end], axis=1)

    p = 20 * np.log10(np.abs(np.fft.rfft(signal)))
    f = np.linspace(0, sample_rate/2.0, len(p))
    pl.plot(f, p)
    pl.xlabel("Frequency(Hz)")
    pl.ylabel("Power(dB)")
    pl.show()



  exit()

  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  cos_convergence(screen, ratio=args.ratio, depth=args.depth, degree_step=args.degree)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit 