import librosa
import matplotlib.pyplot as plt
import numpy as np
import pygame

from vis.lib.drawing_utils import get_rainbow

# getting information from the file
filename = "TEST2.wav"
fft_window = 2048

time_series, sample_rate = librosa.load(filename, sr=44100)
duration_seconds = len(time_series) / sample_rate
# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, center=False, n_fft=fft_window))
# converting the matrix to decibel matrix
# If I understand correctly, the spectrogram data is a 2d matrix corresponding
# time and freq => val.
# The buckets themselves are defined by the librosa.fft_frequences function.
# SO
# The first bucket frequencies[0] = 0Hz, has a value of time series points in spectrogram[0]
# The second bucket frequncies[1] = 21Hz, has a value of time series points in spectrogram[1]
# ...
spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
frequencies = librosa.fft_frequencies(sr=sample_rate, n_fft=fft_window)
print(f"SPECTRO SHAPE: {spectrogram.shape}")
print(f"FREQUENCIES: {len(frequencies)}")


print(f"SPECTRO[0]: {len(spectrogram[0])}")


# The entire spectogram is calculated up front, but we can get slices of it
# by checking where we are given a particular value in seconds.
def get_frequency_slice(spectrogram: np.array, current_seconds: float, duration_seconds: float):
  ratio = current_seconds / duration_seconds
  time_index = int(min(len(spectrogram[0]) - 1, (len(spectrogram[0]) * ratio)))
  return spectrogram[:, time_index]

print(f"TOTAL SECONDS: {duration_seconds}")
print(get_frequency_slice(spectrogram, 6.5, duration_seconds))

# up_to = 10
# print(frequencies[:up_to])
# for second in np.arange(0, 2, 0.05):
#   slice = get_frequency_slice(spectrogram, second, duration_seconds)
#   print(slice[:up_to])

librosa.display.specshow(spectrogram, hop_length=fft_window / 4,
                         y_axis='log', x_axis='s', n_fft=fft_window, sr=sample_rate)
plt.title('Sleight')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()

pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w)
screen_h = int(infoObject.current_w/2)

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])

t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(filename)
pygame.mixer.music.play(0)

# bar_width = int(screen_w / len(frequencies))
bar_width = 5
min_decible = -80
max_decible = 0
decible_ratio = 700 / 80

# Run until the user asks to quit
running = True
while running:

  t = pygame.time.get_ticks()
  deltaTime = (t - getTicksLastFrame) / 1000.0
  getTicksLastFrame = t

  # Did the user click the window close button?
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Fill the background with black.
  screen.fill((0, 0, 0))

  # Get the frequency db slice based on the current pos of the mixer:
  print(pygame.mixer.music.get_pos() / 1000.0)
  slice = get_frequency_slice(spectrogram, pygame.mixer.music.get_pos() / 1000.0, duration_seconds)
  max_index = len(slice) - 1
  # DRAW!
  for i, freq_db in enumerate(slice):
    height = (80 + freq_db) * decible_ratio
    # print(f"RECT: {(bar_width * i, 700 - height, bar_width, height)}")
    
    pygame.draw.rect(screen, get_rainbow(i, max_index), (bar_width * i, 700 - height, bar_width, height))
    # pygame.draw.rect(screen, (255, 255, 255), (bar_width * i, 700 - height, bar_width, height))

  # Flip the display
  pygame.display.flip()

# Done! Time to quit.
pygame.quit()