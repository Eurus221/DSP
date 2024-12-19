import math

import numpy as np

from dsp import open_file
from task4 import conv2
from CompareSignal import Compare_Signals
from task5 import idft_dft2
from task5 import phase_height
from task5 import comp_constructor
def rect(N,n):
    return 1

def hanning(N,n):
    return 0.5+0.5*math.cos((2*math.pi*n)/N)

def hamming(N,n):
    return 0.54+0.46*math.cos((2*math.pi*n)/N)

def blackMan(N,n):
   return 0.42+0.5*math.cos((2*math.pi*n)/(N-1))+0.08*math.cos((4*math.pi*n)/(N-1))

def lowPass(n,fc,f):
    if(n==0):
        return 2*fc
    w=2*math.pi*fc
    return 2*fc*(math.sin(n*w)/(n*w))
def highPass(n,fc,f):
    if (n == 0):
        return 1-(2 * fc)
    w=2*math.pi*fc
    return -2*fc*(math.sin(n*w)/(n*w))
def bandPass(n,fLow,fHigh):
    if (n == 0):
        return 2*(fHigh-fLow)
    wlow=2*math.pi*fLow
    wHigh=2*math.pi*fHigh
    return (2*fHigh*math.sin(n*wHigh)/(n*wHigh))-(2*fLow*math.sin(n*wlow)/(n*wlow))
def bandRej(n,fLow,fHigh):
    if (n == 0):
        return 1-2*(fHigh-fLow)
    wlow=2*math.pi*fLow
    wHigh=2*math.pi*fHigh
    return (2*fLow*math.sin(n*wlow)/(n*wlow))-(2*fHigh*math.sin(n*wHigh)/(n*wHigh))

def windowDecider(stopBand):
    if stopBand<=21:
        return rect,0.9
    elif stopBand<=44:
        return hanning,3.1
    elif stopBand<=53:
        return hamming,3.3
    elif stopBand<=74:
        return blackMan,5.5
def filterDecider(filterName,fc1,fc2,window,fs):
    if filterName=="lowPass":
        fcNew=fc1+(window/2)
        fcNew/=fs
        return lowPass,fcNew,fc2
    elif filterName=="highPass":
        fcNew = fc1 - (window / 2)
        fcNew /= fs
        return highPass,fcNew,fc2
    elif filterName=="bandBass":
        fcN1=fc1-(window/2)
        fcN1/=fs
        fcN2 = fc2 + (window / 2)
        fcN2 /= fs
        return bandPass,fcN1,fcN2
    elif filterName=="bandReject":
        fcN1 = fc1 + (window / 2)
        fcN1 /= fs
        fcN2 = fc2 - (window / 2)
        fcN2 /= fs
        return bandRej,fcN1,fcN2

def hConstructor(filterName,fc,transitionWidth,stopBand,fs,freqHigh=0):
    window,width=windowDecider(stopBand)
    filter,fc1,fc2=filterDecider(filterName,fc,freqHigh,transitionWidth,fs)
    N=round(width/(transitionWidth/fs))
    if N%2==0:
        N+=1
    h=[]
    for i in range(int(N/2)+1):
        h.append(filter(i,fc1,fc2)*window(N,i))
    H=h[::-1] + h[1:]

    indecies = np.arange(int(-N/2),int(N/2)+1)
    #for i,x in zip(indecies,H):
    # print(f"index is {i} and value is {x} \n")
    #Compare_Signals(r"C:\ahmed\college projects\DSP\BSFCoefficients.txt",indecies,H)
    return H,indecies

filter,indeciesFilter=hConstructor("bandReject",150,50,60,1000,250)
indecies,signal=open_file(1)
out,outIND=conv2(signal,filter,indecies,indeciesFilter)
Compare_Signals(r"C:\Users\sian\Downloads\OneDrive_2024-12-18 (1)\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt",
                outIND,out)