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
    return output_indices, output
def corr_test():
    _,signal1=open_file(1)
    _,signal2=open_file(1)
    corr2(signal1,signal2)
    
def timeShift(sampling_frequency,s1,s2):
    _,output=corr2(s1,s2)
    index=output.index(max(output))
    Ts= 1/sampling_frequency
    print(index*Ts)
def time_test(sampling_frequency):
    _,signal1=open_file(1)
    _,signal2=open_file(1)
    timeShift(sampling_frequency,signal1,signal2)
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
    input = read_Files(r"C:\Users\andre\Desktop\dsp\OneDrive_2024-12-18\Correlation Task Files\point3 Files\Test Signals\Test1.txt")  # Read input signal
    classA = maxmizer(input, r"C:\Users\andre\Desktop\dsp\OneDrive_2024-12-18\Correlation Task Files\point3 Files\Class 1")
    classB = maxmizer(input, r"C:\Users\andre\Desktop\dsp\OneDrive_2024-12-18\Correlation Task Files\point3 Files\Class 2")
    if classA > classB:
        print("DOWN")
    else:
        print("UP")


def task6_window():
    root = tk.Tk()
    root.title("Dark Theme Example")
    root.geometry("400x200")
    root.config(bg="#1e1e1e")

    # Add a text field
    text_field = tk.Entry(root, font=("Arial", 12), width=30, bg="#333333", fg="#ffffff", insertbackground="#ffffff")
    text_field.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    # Add two buttons
    button1 = tk.Button(root, text="correlation", command=corr_test, bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button1.grid(row=1, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    button2 = tk.Button(root, text="time shift", command=lambda:time_test(int(text_field.get())), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button2.grid(row=1, column=1, padx=20, pady=10, ipadx=10, ipady=5)
    
    button3 = tk.Button(root, text="Classification", command=classify, bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button3.grid(row=2, column=1, padx=20, pady=10, ipadx=10, ipady=5)

    # Run the main Tkinter loop
    root.mainloop()