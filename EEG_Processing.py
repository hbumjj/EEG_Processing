#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scipy.signal as ssig
import math

class EEG_data:
    def __init__(self,name):
        self.name=name
    
    def load_data(self): # load_data
        file=open(self.name,'r')
        lines=file.readlines()
        time,eeg=[],[]
        for i in lines:
            time.append(float(i.split("\t")[0]))
            eeg.append(float(i.split("\t")[1]))
        return time, eeg
    
    def low_Freq_response(self,data,fs): # Lowpass_filter + freq_response
        b,a=ssig.butter(10,12,btype='low', fs=fs)
        w,h=ssig.freqz(b,a,fs)
        w_hz=w*fs/(2*math.pi)
        low_ecg=ssig.filtfilt(b,a,data)
        return w_hz, abs(h), low_ecg
    
    def high_Freq_response(self,data,fs): # Highpass_filter + freq_response
        b,a= ssig.butter(6,8,btype='high',fs=fs)
        w,h=ssig.freqz(b,a,fs)
        w_hz=w*fs/(2*math.pi)
        high_ecg=ssig.filtfilt(b,a,data)
        return w_hz, abs(h), high_ecg
    
    def show_result(self): # graph option
        time,eeg=EEG_data.load_data(self)
        fs=int(1/(time[1]-time[0]))
        low_hz, low_fr, low_eeg= EEG_data.low_Freq_response(self,eeg,fs)
        high_hz, high_fr, high_eeg=EEG_data.high_Freq_response(self,low_eeg,fs) 
        import matplotlib.pyplot as plt
        plt.figure(figsize=(7,6))
        plt.subplot(4,1,1); plt.plot(time,eeg,'black');plt.title("Original EEG data"); plt.xlabel('time'); plt.ylabel('amplitude');plt.ylim([-200,200])
        plt.subplot(4,2,3); plt.plot(low_hz,low_fr,'black');plt.title("Frequency response"); plt.xlabel('freq'); plt.ylabel('|H(jw)|');plt.xlim([0,20])
        plt.subplot(4,2,4); plt.plot(high_hz,high_fr,'black');plt.title("Frequency response"); plt.xlabel('freq'); plt.ylabel('|H(jw)|');plt.xlim([0,20])
        plt.subplot(4,1,3); plt.plot(time,low_eeg,'black');plt.title("low pass filtering data"); plt.xlabel('time'); plt.ylabel('amplitude');plt.ylim([-200,200])
        plt.subplot(4,1,4); plt.plot(time,high_eeg,'black');plt.title("high pass filtering data"); plt.xlabel('time'); plt.ylabel('amplitude');plt.ylim([-40,40])
        plt.tight_layout(); plt.show()
        # spectrogram
        plt.figure(figsize=(5,5)) 
        plt.specgram(eeg,Fs=fs);plt.title("Spectrogram(before filter)");plt.xlabel("time");plt.ylabel("frequency")
        plt.show()


if __name__=="__main__":
    EEG_data('EEG_data.txt').show_result()


# In[ ]:




