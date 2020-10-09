import wave
import numpy
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import filtfilt

# open the audio file and extract some information
spf = wave.open('test_voice_male.wav','rb')
(nChannels, sampWidth, sampleRate, nFrames, compType, compName) = spf.getparams()

# extract audio from wav file
input_signal = spf.readframes(-1)
input_signal = numpy.fromstring(input_signal, 'Int16')
amp = 1.0
input_signal = amp * input_signal / max(abs(max(input_signal)),abs(min(input_signal)))
spf.close()

# create the filter
N = 4
nyq = 0.5 * sampleRate
low = 100 / nyq
high = 500 / nyq
b, a = signal.butter(N, [low, high], btype='band')

# apply filter
output_signal = signal.filtfilt(b, a, input_signal)

# create output file
wav_out = wave.open("output.wav", "wb")
wav_out.setparams((nChannels, sampWidth, sampleRate, nFrames, compType, compName))

# write to output file
wav_out.writeframes(output_signal.tobytes())
wav_out.close()

# plot the signals
plt.figure("input")
t = numpy.linspace(0, nFrames/sampWidth, nFrames, endpoint = False)
plt.plot(t, input_signal, label='Input')
plt.figure("output")
plt.plot(t, output_signal, label='Output')
plt.show()
