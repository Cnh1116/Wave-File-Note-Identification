# Author: Carson Holland
# File Name: Wav_File_Note_Identifier.py
#
# Purpose: This Python Program first reads the contents of a .wav file within the same directory as this file. The file name of the .wav
# file is then hard-coded into a audioFileName string. The contents of the .wav file are read, FFT is performed, the frequency that generates the
# greatest amplitude is then thrown into a note identification algorithm to determine the pitch of the audio file.
#
#Huge thanks to Metallicode on YouTube for the tutorial!

#Imports----------------------------------------------------------------------------------------------------------------------------------
import scipy.io.wavfile as wavfile
import wave
import scipy
import scipy.fftpack as fftpk
import numpy as np
from matplotlib import pyplot as plt

#Grabbing the audio signal data-------------------------------------------------------------------------------------------------------------------

#Name of the Audio File
audioFileName = "Ocarina_C4.wav"

#Open the audio file
audioObject = wave.open(audioFileName, 'rb') #rb = Read Binary

#Getting the parameters
sample_freq = audioObject.getframerate()
n_samples = audioObject.getnframes()
signal_wave = audioObject.readframes(-1) #-1 Reads all frames
n_channels = audioObject.getnchannels()

#Close the audio Object
audioObject.close()

#Time = number of frames / Fs
t_audio = n_samples / sample_freq
print("Audio length: ", t_audio, " seconds")

#The signal----------------------------------------------------
signal = np.frombuffer(signal_wave, dtype=np.int16)

#List of times for the plot. Goes from 0 to max time in sample amount of increments
times = np.linspace(0,t_audio,n_samples*n_channels) 

#Plotting the Audio Signal - time domain
plt.plot(times, signal)
plt.title("Time Domaiain Response of " + audioFileName)
plt.xlabel("Time")
plt.ylabel("Signal")
plt.show()

#Performing FFT---------------------------------------------------------------------------------------------------------------------------
FFT = abs(fftpk.fft(signal))
freqs = fftpk.fftfreq(len(FFT), (1.0/sample_freq))

#Plotting the frequency response----------------------------------------------------------------------------------------------------------
plt.plot(freqs[range(len(FFT)//2)], FFT[range(len(FFT)//2)])
plt.title("Frequency Response of " + audioFileName)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (dB)")
plt.show()

#Grabbing the frequency that generated the greatest response
amp_Freq = np.array([FFT, freqs])
amp_position = amp_Freq[0, :].argmax()
maximumFreq = amp_Freq[1, amp_position]

print("Max Frequency: ", maximumFreq)


#Note Identification Algorithm----------------------------------------------------------------------------------------------------------
referenceFrequency = 440 #Middle A
noteList = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B'] #Index 0 - 11
noteRelationship = 2**(1/12)
errorAllowed = 0.025 #2.5% Error Allowed
noteIndex = 9 #Middle A Starts at index 9
currentOctave = 4 #Starting in the 4th octave



def PercentError(maximumFreq, currentFreq):
    error = (abs((maximumFreq-currentFreq)/currentFreq))
    percentError = error * 100
    #print("Percent difference between ", maximumFreq, " and ", currentFreq, " is ", error, " or ", percentError, "%")
    return error

#Max Frequency is Middle A
if (PercentError(maximumFreq, referenceFrequency) <= errorAllowed):
    print("Your note is Middle A: ", noteList[9])

#Max Frequency is Lower than Middle A
elif (maximumFreq < referenceFrequency):
    currentFreq = referenceFrequency

    while(PercentError(maximumFreq, currentFreq) > errorAllowed):
        currentFreq = currentFreq / noteRelationship
        #print("Current Frequency = ", currentFreq)
        if(noteIndex == 0): #If we are on C, then jump to B, one octave lower
            noteIndex = 11
            currentOctave = currentOctave -1
        else:
            noteIndex -= 1

    print("Your note was: ", noteList[noteIndex], " in octave: ", currentOctave)

#Max Frequency is Higher than Middle A
elif (maximumFreq > referenceFrequency):
    currentFreq = referenceFrequency

    while(PercentError(maximumFreq, currentFreq) > errorAllowed):
        currentFreq = currentFreq * noteRelationship
        #print("Current Frequency = ", currentFreq)
        if(noteIndex == 11): #If we are on B, then jump to C, one octave higher
            noteIndex = 0
            currentOctave += 1
        else:
            noteIndex += 1

    print("Your note was: ", noteList[noteIndex], " in octave: ", currentOctave)






