import numpy as np
import matplotlib.pyplot as plt
import librosa as lr
import librosa.display


# y: audio time-series

# sr: sampling rate of y

# S: spectrogram

# n_fft: length of the FFT window

# hop_length: number of samples between successive frames. See librosa.core.stft

# win_length: Each frame of audio is windowed by window().
filename = "sample_music1.mp3"
y,sr = lr.load(filename,sr=11025) # Returns: y:np.ndarray [shape=(n_mels, t)]

window_size = 1024
window = np.hanning(window_size)
stft  = librosa.core.spectrum.stft(y, n_fft=window_size, hop_length=512, window=window)



for each in stft:
    out = 2 * np.abs(each) / np.sum(window)
    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(111)
    librosa.display.specshow(librosa.amplitude_to_db(out, ref=np.max), ax=ax, y_axis='log', x_axis='time')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    plt.show()
# Compute a mel-scaled spectrogram.
# If a spectrogram input S is provided, then it is mapped directly onto the mel basis by mel_f.dot(S).
# If a time-series input y, sr is provided, then its magnitude spectrogram S is first computed, and then mapped onto the mel scale by mel_f.dot(S**power).
# By default, power=2 operates on a power spectrum.

