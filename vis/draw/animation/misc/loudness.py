import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

from vis.lib.audio_utils import AudioAnalyzer

# aa = AudioAnalyzer("/Users/admiralbolt/Music/Logic/Bounces/Islands.wav")
# aa.process_features()


y, sr = librosa.load("/Users/admiralbolt/Music/Logic/Bounces/Islands.wav", sr=44100)
rms = librosa.feature.rms(y=y)[0]

print(rms.shape)
print(min(rms))
print(sum(rms) / len(rms))
print(max(rms))
print(np.quantile(rms, [0.25, 0.50, 0.75]))


print(y.shape)
print(min(y))
print(sum(y) / len(y))
print(max(y))

z = y ** 2

# print(z.shape)
# print(min(z))
# print(sum(z) / len(z))
# print(max(z))
# print(np.quantile(z, [0.25, 0.5, 0.75]))


# frames = range(len(rms))
# t = librosa.frames_to_time(frames)

# plt.figure(figsize=(15, 17))

# ax = plt.subplot(3, 1, 1)
# librosa.display.waveshow(y, alpha=0.5, color="blue")
# plt.plot(t, rms, color="r")

# plt.show()

# fig, ax = plt.subplots(nrows=3, sharex=True)
# librosa.display.waveshow(aa.time_series, sr=aa.sample_rate, ax=ax[0], color="blue")
# frames = range(len(aa.loudness))
# t = librosa.frames_to_time(frames)
# ax[0].set(title='Envelope view, mono')
# ax[0].label_outer()
# plt.plot(t, aa.loudness)