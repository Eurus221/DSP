from dsp import open_file
import matplotlib.pyplot as plt
import numpy as np 
import tkinter as tk
from dsp import ReadSignalFile
from dsp import display
def movingAverage(windowSize):
    indecies,signal=open_file(1)
    output=[]
    for i in range(len(signal)-windowSize+1):
        sum=0
        for j in range (i, i+windowSize):
            sum+=signal[j]
            val =sum/windowSize
            if(val==int(val)):
                val=int(val)
            else:
                val= round(val,3)
        output.append(val)
    test=0
    if(windowSize==3):
        test=1
    elif(windowSize==5):
        test=2
    print("########################")
    print(output)
    print("########################")
    compare_signal(test,indecies,output)
  
    return output

#y(n) = x(n)- x(n-1)
def firstDerivative():
    indecies,signal=open_file(1)
    output=[]
    for i in range(1,len(signal)):
        output.append(signal[i]-signal[i-1])
    compare_signal(3,indecies,output)
    return output

#y(n)= x(n+1)-2x(n)+x(n-1)
def secondDerivative():
    indecies,signal=open_file(1)
    output=[]
    for i in range(1,len(signal)-1):
        firstTerm= signal[i+1]
        seconndTerm= 2*signal[i]
        thirdTerm= signal[i-1]
        output.append(firstTerm-seconndTerm+thirdTerm)
    compare_signal(4,indecies,output)
    return output

def conv():
    indecies,signal1=open_file(1)
    indecies2,signal2=open_file(1)
    output_length=len(signal1)+len(signal2)-1
    output = [0] * output_length
    len1=len(signal1)
    first= indecies[0]
    outputIndecies=[]
    for n in range(output_length):
        outputIndecies.append(first+n)
        for k in range(len(signal2)):
            if 0<=n-k<len1:
                output[n]+=signal1[n-k]*signal2[k]
    compare_signal(5,outputIndecies,output)
    return output
def conv2(signal1,signal2,indecies,indecies2):
    output_length = len(signal1) + len(signal2) - 1
    output = [0] * output_length
    len1 = len(signal1)
    first = indecies2[0]
    outputIndecies = []
    for n in range(output_length):
        outputIndecies.append(first + n)
        for k in range(len(signal2)):
            if 0 <= n - k < len1:
                output[n] += signal1[n - k] * signal2[k]
    #compare_signal(5, outputIndecies, output)
    return output,outputIndecies

def compare_signal(testNum,indecies,signal):
    if(testNum==1):
        indeciesOut,signalout= ReadSignalFile("MovingAvg_out1.txt")
        if(signal==signalout):
            print("passed moving average 1")
            display(coord=2, samp2= signal,ind2=indeciesOut)
        else:
            print("failed moving average 1")
    elif(testNum==2):
        indeciesOut,signalout= ReadSignalFile("MovingAvg_out2.txt")
        if(signal==signalout):
            print("passed moving average 2")
            display(coord=2, samp2= signal,ind2=indeciesOut)
        else:
            print("failed moving average 2")
    elif(testNum==3):
        indeciesOut,signalout= ReadSignalFile("1st_derivative_out.txt")
        if(signal==signalout):
            print("passed first derivative")
            display(coord=2, samp2= signal,ind2=indeciesOut)
        else:
            print("failed first derivative")
    elif(testNum==4):
        indeciesOut,signalout= ReadSignalFile("2nd_derivative_out.txt")
        if(signal==signalout):
            print("passed second derivative")
            display(coord=2, samp2= signal,ind2=indeciesOut)
        else:
            print("failed second derivative")
    elif(testNum==5):
        indeciesOut,signalout= ReadSignalFile("Conv_output.txt")
        if(indeciesOut!=indecies):
            print("wrong indecies")
            return
        if(signal==signalout):
            print("passed conv")
            display(coord=2, samp2= signal,ind2=indeciesOut)
        else:
            print("failed conv")
    elif(testNum==6):
        indeciesOut,signalout=ReadSignalFile("CorrOutput.txt")
        if(signal==signalout):
            print("passed Correlation")
            display(coord=2, samp2= signal,ind2=indeciesOut)



def task4_window():
    root = tk.Tk()
    root.title("Dark Theme Example")
    root.geometry("400x200")
    root.config(bg="#1e1e1e")

    # Add a text field
    text_field = tk.Entry(root, font=("Arial", 12), width=30, bg="#333333", fg="#ffffff", insertbackground="#ffffff")
    text_field.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    # Add two buttons
    button1 = tk.Button(root, text="Moving Average", command=lambda:movingAverage(int(text_field.get())), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button1.grid(row=1, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    button2 = tk.Button(root, text="First Derivative", command=firstDerivative, bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button2.grid(row=1, column=1, padx=20, pady=10, ipadx=10, ipady=5)
    
    button3 = tk.Button(root, text="second derivative", command=secondDerivative, bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button3.grid(row=2, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    button4 = tk.Button(root, text="Convolve", command=conv, bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button4.grid(row=2, column=1, padx=20, pady=10, ipadx=10, ipady=5)

    # Run the main Tkinter loop
    root.mainloop()