import bisect
import librosa
import math
import matplotlib.pyplot as plt
import numpy as np

class AudioAnalyzer:
  """Analyze some audio!"""

  file_name: str
  # Raw audio data.
  time_series: np.array
  # Sample rate! Probably should be 44.1k hz.
  sample_rate: int
  # FFT Window! I.e. how many samples we run a fourier transform over.
  fft_window: int
  # Spectrogram!
  spectrogram: np.array
  # Number of frequency slices in the spectrogram. Each slice corresponds to
  # roughly 93ms of sound if fft_window=2048.
  number_of_slices: int
  # Frequency bins, each index corresponds to a band of hz.
  frequencies: np.array
  # The A-weighting of each frequency. This is roughly how much impact an
  # individual frequency bin has on the overall sound.
  a_weights: np.array
  # Loudness!
  loudness: np.array
  # Estimated tempo!
  tempo: float
  # Beats!
  beat_frames: np.array
  beat_times: np.array
  _max_index: int = -1

  def __init__(self, file_name: str, fft_window: int=2048, sample_rate: int=44100):
    self.file_name = file_name
    self.fft_window = fft_window
    self.sample_rate = sample_rate

  def process_features(self):
    """Process ALL audio features we want to use."""
    print(f"Processing audio features of {self.file_name}")
    self.time_series, _ = librosa.load(self.file_name, sr=self.sample_rate)
    self.duration_seconds = len(self.time_series) / self.sample_rate
    stft = np.abs(librosa.stft(self.time_series, center=False, n_fft=self.fft_window))
    self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
    self.number_of_slices = len(self.spectrogram[0])
    self.frequencies = librosa.fft_frequencies(sr=self.sample_rate, n_fft=self.fft_window)
    self.a_weights = librosa.A_weighting(frequencies=self.frequencies)
    self.loudness = librosa.feature.rms(y=self.time_series)[0]
    self.tempo, self.beat_frames = librosa.beat.beat_track(y=self.time_series, sr=self.sample_rate)
    self.beat_times = librosa.frames_to_time(self.beat_frames)
  
  def on_beat(self, current_seconds: float, width: float=0.012):
    """Are we on a beat?"""
    closest_index = bisect.bisect_left(self.beat_times, current_seconds)
    if closest_index >= len(self.beat_times) or closest_index <= self._max_index:
      return False
    
    if self.beat_times[closest_index] - width <= current_seconds <= self.beat_times[closest_index] + width:
      self._max_index = closest_index
      return True
    
    if closest_index > 0 and (closest_index -1) > self._max_index and self.beat_times[closest_index - 1] - width <= current_seconds <= self.beat_times[closest_index - 1] + width:
      self._max_index = closest_index
      return True

    return False

  def _get_frame(self, current_seconds: float):
    ratio = current_seconds / self.duration_seconds
    return int(min(self.number_of_slices - 1, self.number_of_slices * ratio))

  def get_frequency_slice(self, current_seconds: float):
    """Get the relative DBs of each frequency bin at a given timestamp.
    
    The slice of db values return correspond to the frequency bins in
    self.frequencies. I.e. if we return [-21.1, -31.1, -9.9, ...] those
    corresponds to the frequency bands [0, 21.5, 43, ...]
    """
    return self.spectrogram[:, self._get_frame(current_seconds=current_seconds)]
  
  def get_loudness(self, current_seconds: float) -> float:
    """Get the loudness at a given timestamp."""
    return 20 * math.log(self.loudness[self._get_frame(current_seconds=current_seconds)], 10)
  
  def plot(self, y_axis: str="log"):
    librosa.display.specshow(self.spectrogram, hop_length=self.fft_window / 4,
                             y_axis=y_axis, x_axis="s", n_fft=self.fft_window,
                             sr=self.sample_rate)
    plt.title(self.file_name)
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()

  