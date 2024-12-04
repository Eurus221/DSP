import tkinter as tk
import math
from dsp import open_file
import matplotlib.pyplot as plt
from QuanTest1 import QuantizationTest1
from QuanTest2 import QuantizationTest2
numberOfLevels=0

indicies=[]
samples=[]
quantized=[]
encoded=[]
errors=[]
errorSquared=[]
def calculateNumLevels(power):
    global numberOfLevels
    numberOfLevels=int(math.pow(2,power))
    quantize()
def assignLevels(num):
    global numberOfLevels
    numberOfLevels=num
    quantize()
def quantize():
    global indicies, samples, quantized, encoded, errors, errorSquared
    indicies=[]
    samples=[]
    quantized=[]
    encoded=[]
    errors=[]
    errorSquared=[]
    indicies,samples=open_file(1)
    minimum=min(samples)
    maximum= max(samples)
    delta= (maximum-minimum)/numberOfLevels
    intervals=[minimum]
    midpoints=[]
    intervalIdecies=[]
    for i in range(numberOfLevels):
        num=intervals[i]+delta
        intervals.append(num)
        mid= (intervals[i]+intervals[i+1])/2
        mid=round(mid,2)
        midpoints.append(mid)
    for sample in samples: 
        index=sample-minimum 
        index= int(index/delta)
        index = min(index, numberOfLevels - 1)
        intervalIdecies.append(index+1)
        quantized.append(midpoints[index])
        encoded.append(bin(index)[2:].zfill(int(math.log2(numberOfLevels))))
        error=midpoints[index]-sample
        errors.append(error)
        errorSquared.append(math.pow(error,2))
    print("###########################################")
    print(quantized)
    print(encoded)
    QuantizationTest1("Quan1_Out.txt",encoded,quantized)
    QuantizationTest2("Quan2_Out.txt",intervalIdecies,encoded,quantized,errors)
    display()

           
def display():
    plt.figure(figsize=(10,6))
    plt.subplot(2, 1, 1)  # 2 rows, 1 column, first subplot
    plt.stem(indicies, samples, linefmt='r-', markerfmt='ro', basefmt=" ", label="original")
    plt.legend()
    plt.title("Original Data")

    # Plot the quantized data in the second subplot
    plt.subplot(2, 1, 2)  # 2 rows, 1 column, second subplot
    plt.stem(indicies, quantized, linefmt='b-', markerfmt='bo', basefmt=" ", label="quantized")
    plt.legend()
    plt.title("Quantized Data")

    # Show both plots in the same window
    plt.tight_layout()
    plt.show()



# Functionality placeholder for the buttons
def button_action():
    print("Button clicked")

# Create the main Tkinter window
def task3_window():
    root = tk.Tk()
    root.title("Dark Theme Example")
    root.geometry("400x200")
    root.config(bg="#1e1e1e")

    # Add a text field
    text_field = tk.Entry(root, font=("Arial", 12), width=30, bg="#333333", fg="#ffffff", insertbackground="#ffffff")
    text_field.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    # Add two buttons
    button1 = tk.Button(root, text="# levels", command=lambda:assignLevels(int(text_field.get())), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button1.grid(row=1, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    button2 = tk.Button(root, text="# bits", command=lambda:calculateNumLevels(int(text_field.get())), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button2.grid(row=1, column=1, padx=20, pady=10, ipadx=10, ipady=5)

    # Run the main Tkinter loop
    root.mainloop()
