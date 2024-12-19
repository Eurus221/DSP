import math

import numpy as np
import tkinter as tk
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
    if(filterName=="lowPass"):
        Compare_Signals(r"C:\Users\andre\Desktop\dsp\Practical Task\FIR test cases\Testcase 1\LPFCoefficients.txt",Your_indices=indecies,Your_samples=H)
    elif(filterName=="highPass"):
        Compare_Signals(r"C:\Users\andre\Desktop\dsp\Practical Task\FIR test cases\Testcase 3\HPFCoefficients.txt",Your_indices=indecies,Your_samples=H)
    elif(filterName=="bandBass"):
        Compare_Signals(r"C:\Users\andre\Desktop\dsp\Practical Task\FIR test cases\Testcase 5\BPFCoefficients.txt",Your_indices=indecies,Your_samples=H)
    elif(filterName=="bandReject"):
        Compare_Signals(r"C:\Users\andre\Desktop\dsp\Practical Task\FIR test cases\Testcase 7\BSFCoefficients.txt",Your_indices=indecies,Your_samples=H)

    return H,indecies



def res(filterName):
    indecies,signal=open_file(1)
    if(filterName=="lowPass"):
        filter,indeciesFilter=hConstructor("lowPass",1500,500,50,8000)
        out,outIND=conv2(signal,filter,indecies,indeciesFilter)
        Compare_Signals(r"C:\Users\andre\Desktop\dsp\Practical Task\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt",Your_indices=outIND,Your_samples=out)
    elif(filterName=="highPass"):
        filter,indeciesFilter=hConstructor("highPass",1500,500,70,8000)
        out,outIND=conv2(signal,filter,indecies,indeciesFilter)
        Compare_Signals(r"C:\Users\andre\Desktop\dsp\Practical Task\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt",Your_indices=outIND,Your_samples=out)
    elif(filterName=="bandBass"):
        filter,indeciesFilter=hConstructor("bandBass",150,50,60,1000,250)
        out,outIND=conv2(signal,filter,indecies,indeciesFilter)
        Compare_Signals(r"C:\Users\andre\Desktop\dsp\Practical Task\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt",Your_indices=outIND,Your_samples=out)
    elif(filterName=="bandRej"):
        filter,indeciesFilter=hConstructor("bandReject",150,50,60,1000,250)
        out,outIND=conv2(signal,filter,indecies,indeciesFilter)
        Compare_Signals(r"C:\Users\andre\Desktop\dsp\Practical Task\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt",Your_indices=outIND,Your_samples=out)



def task7_window():
    root = tk.Tk()
    root.title("Dark Theme Example")
    root.geometry("400x200")
    root.config(bg="#1e1e1e")


    # Add two buttons
    button1 = tk.Button(root, text="Low Pass", command=lambda:res("lowPass"), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button1.grid(row=0, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    button2 = tk.Button(root, text="High Pass", command=lambda:res("highPass"), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button2.grid(row=0, column=1, padx=20, pady=10, ipadx=10, ipady=5)
    
    button3 = tk.Button(root, text="Band Pass", command=lambda:res("bandBass"), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button3.grid(row=1, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    button4 = tk.Button(root, text="Band Reject", command=lambda:res("bandRej"), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button4.grid(row=1, column=1, padx=20, pady=10, ipadx=10, ipady=5)
    


    root.mainloop()