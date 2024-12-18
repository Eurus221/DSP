import math
import os

from dsp import ReadSignalFile
from dsp import display
from dsp import open_file
from task4 import compare_signal
import numpy as np
import tkinter as tk
import statistics
import math
def read_Files(path):
    values = []
    with open(path, 'r') as file:
        for line in file:
            values.append(int(line.strip()))
    return values
def corr2(signal1,signal2):
    N = len(signal1)
    output = []
    output_indices = []

    s1Squared = sum(x ** 2 for x in signal1)
    s2Squared = sum(x ** 2 for x in signal2)

    for j in range(N):
        summation = 0
        for n in range(N):
            summation += signal1[n]* signal2[(n + j) % N]
        # Normalize correctly
        correlation_value = summation / math.sqrt(s1Squared * s2Squared)
        output.append(round(correlation_value,8))
        output_indices.append(j)
    compare_signal(6, output_indices, output)
    print(output)
    return output_indices, output

def timeShift(sampling_frequency,s1,s2):
    _,output=corr2(s1,s2)
    index=output.index(max(output))
    Ts= 1/sampling_frequency
    print(index*Ts)

def maxmizer(input, directory):
    outs = []
    # Iterate over files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory,filename)
        if os.path.isfile(file_path):
            signal = read_Files(file_path)
            _,out = corr2(input, signal)
            max_value = max(out)
            outs.append(max_value)
    return sum(outs) / len(outs)

def classify():
    input = read_Files(r"C:\ahmed\college projects\DSP\Test Signals\Test2.txt")  # Read input signal
    classA = maxmizer(input, r"C:\ahmed\college projects\DSP\Class 1")
    classB = maxmizer(input, r"C:\ahmed\college projects\DSP\Class 2")
    if classA > classB:
        print("classA")
    else:
        print("classB")

classify()