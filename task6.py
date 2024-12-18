from dsp import ReadSignalFile
from dsp import display
from dsp import open_file
from task4 import compare_signal
import numpy as np
import tkinter as tk

def corr():
    indecies,signal1=open_file(1)
    indecies2,signal2=open_file(1)
    output_length=len(signal1) + len(signal2)-1
    output = [0] * output_length
    len1=len(signal1)
    first= indecies[0]
    outputIndecies=[]
    for n in range(output_length):
        #outputIndecies.append(first+n)
        for k in range(len(signal2)): 
            output[n]+=signal1[n]*signal2[(n+k)%n]
        output[n]/=len1
    
    return output

def corr2():
    # Read signals
    indices1, signal1 = open_file(1)
    indices2, signal2 = open_file(1)

    # Ensure signals are the same length
    N = len(signal1)
    output = []
    output_indices = []
    k=len(signal2)
    # Compute correlation for each lag (j)
    for j in range(N):  # Lag range from 0 to N-1
        summation = 0
        for n in range(N):  # Iterate over all values in the signals
            # Wrap around signal2 using modular arithmetic
            summation += signal1[n] * signal2[(n + j) % N]
        
        # Normalize by the length N
        correlation_value = summation / N
        output.append(correlation_value)
        output_indices.append(j)  # Lag indices
    compare_signal(6,output_indices,output)
    return output_indices, output

corr2()