import numpy as np
import matplotlib.pyplot as plt
import librosa as lr
import librosa.display

# test
# y: audio time-series

# sr: sampling rate of y

# S: spectrogram

# n_fft: length of the FFT window

# hop_length: number of samples between successive frames. See librosa.core.stft

# win_length: Each frame of audio is windowed by window().
filename = "sample_music.mp3"
y,sr = lr.load(filename) 
time_res = 1024*0.5/sr
slices = np.abs(librosa.stft(y, n_fft=1024, hop_length=512, win_length=1024, window='hann'))
freq_bins, time_slices = slices.shape

logarithmic_bands = [(0,20), (20,60), (60,120), (120,240), (240,512)]
nbands = len(logarithmic_bands)

#stores the final frequency points for each time slice in a dictionary with key=time_slice and value=list of strong frequencies
filtered_spectogram = {}
band_across_time_mean = np.zeros((time_slices, nbands))


#iterate over each time slice
for time_slice in range(time_slices):
    temp_spectrogram = []
    #store temporary spectograms which need to be filtered further
	#contains list of (time_of_occurence, frequency_bin, logarithmic_band_index)
    slice_mean = 0

    for i in range(nbands):
        logband = logarithmic_bands[i]
        fft_slice = slices[logband[0]:logband[1],time_slice]
        idx = np.argmax(fft_slice) # max freq in the band
        band_across_time_mean[time_slice][i] = fft_slice[idx] # mean for the band
        slice_mean += fft_slice[idx]# mean of the slice
        temp_spectrogram.append((time_slice,logband[0]+idx,fft_slice[idx],i))
        

    slice_mean /= nbands

    for poss in temp_spectrogram:
        if not poss[0] in filtered_spectogram.keys():
            filtered_spectogram[poss[0]] = []

        if poss[2] >= slice_mean:
            filtered_spectogram[poss[0]].append((poss[1],poss[2],poss[3]))


# Drop points which are weaker than the mean in it's band
band_across_time_mean = np.mean(band_across_time_mean, axis=0)

for time_slice, data in filtered_spectogram.items(): # time_slice,band[0]+idx,fft_slice[idx],i
    final_f=[]   
    for band in data:
        f_bin, mag, band_no = band[0], band[1], band[2]
        if mag >= band_across_time_mean[band_no]: # if freq >= mean of its band
            final_f.append(f_bin)
    
    filtered_spectogram[time_slice] = final_f


to_plot_x, to_plot_y = [], []
for key, val in filtered_spectogram.items():
    plt.scatter(np.array([key]*len(val))*time_res, val, marker='x', c='r')

for log_band in logarithmic_bands:
    plt.axhline(y=log_band[0], color='k', linestyle='-')
    
plt.ylim(0, freq_bins)
plt.show()
    