import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Create the main window
gui = tk.Tk()
gui.title("Signal Reading and Processing Simulation")
gui.geometry("1000x700")
gui.config(bg="#1e1e1e")

signal = []
indices1, samples1, indices2, samples2 = [], [], [], []  # Variables to store the signals

result_indices,result_samples=[],[]
delay_value=0
# Define function to retrieve input from Entry
def retrieve_input():
    global delay_value
    delay_value = entry.get()
    print(delay_value)

# Function to read and return signal data
def ReadSignalFile(file_name):
    indices = []
    samples = []
    with open(file_name, 'r') as f:
        line = f.readline()
        while line:
            L = line.strip()
            if len(L.split()) == 2:
                V1, V2 = map(float, L.split())
                indices.append(V1)
                samples.append(V2)
            line = f.readline()
    print(indices)
    print(samples)
    return indices, samples
import os
from tkinter import filedialog

def WriteSignalFile(indices, samples,size):
    # Get the current working directory (project directory)
    project_directory = os.getcwd()

    # Prompt user to choose where to save the file, opening in the project directory
    file_path = filedialog.asksaveasfilename(
        initialdir=project_directory,  # Open the dialog in the project directory
        defaultextension=".txt",  # Ensures the file is saved as a .txt file
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    if file_path:  # Proceed only if a file path was selected
        with open(file_path, 'w') as f:
            # Optionally, write the two initial zeros if needed
            f.write('0\n0\n')  # Writing the two zeros at the beginning
            f.write(f"{size}\n")
            # Write the signal data
            for i, s in zip(indices, samples):
                f.write(f"{i} {s}\n")  # Write the index and sample, separated by space

        print(f"Signal written to {file_path}")
    else:
        print("No file path selected. Operation canceled.")

# Function to open a file and read the signal
def open_file(file_num):
    file_path = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if file_path:
        try:
            indices, samples = ReadSignalFile(file_path)
            if file_num == 1:
                global indices1, samples1
                indices1, samples1 = indices, samples
            elif file_num == 2:
                global indices2, samples2
                indices2, samples2 = indices, samples
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

# Function for performing operations (add or subtract)
def operations(ind1, samp1, ind2, samp2, operation_type):
    global result_indices,result_samples
    signal1 = dict(zip(ind1, samp1))
    signal2 = dict(zip(ind2, samp2))
    result_indices = sorted(set(ind1).intersection(set(ind2)))

    if operation_type == 1:
        result_samples= [signal1[i] + signal2[i] for i in result_indices]
    elif operation_type == 2:
        result_samples= [signal1[i] - signal2[i] for i in result_indices]
    WriteSignalFile(result_indices,result_samples,len(result_samples))
    print("result indices",result_indices)
    print("result samples",result_samples)
    
def multiply(ind, samp, val):
    global result_indices, result_samples
    signal= dict(zip(ind,samp))
    result_indices = ind
    result_samples = [signal[i] * float(val) for i in result_indices]
    WriteSignalFile(result_indices,result_samples,len(result_samples))
    print("result indices", result_indices)
    print("result samples", result_samples)


def display(ind1=0,samp1=0,ind2=0,samp2=0,coord=1):
    if coord==1:
        plt.figure(figsize=(10, 6))
        plt.plot(ind1, samp1, label='Original signal')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Signal Plot')
        plt.legend()
        plt.grid(True)
        plt.show()

    elif coord == 2:
        plt.figure(figsize=(10, 6))
        plt.plot(ind2, samp2, label='Result signal')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Signal Plot')
        plt.legend()
        plt.grid(True)
        plt.show()
    

def delay_advance(ind,samp,delayValue,coord):
    global result_indices,result_samples
    delayValue=int(delayValue)
    l=len(ind)
    if coord == 1:
        result_indices=[i + delayValue for i in ind]
        result_samples=samp
        print(result_indices)
        print(result_samples)
    elif coord == 2:
        result_indices=[i-delayValue for i in ind]
        result_samples=samp
        print(result_indices)
        print(result_samples)
    elif coord == 3:
        result_indices=[]
        result_samples=[]
        for i in range(l):
            result_indices.append(ind[l-i-1]*-1)
            result_samples.append(samp[l-i-1])
        print(result_indices)
        print(result_samples)  
    WriteSignalFile(result_indices,result_samples,len(result_samples))
          
# Configure rows and columns for centering
gui.grid_columnconfigure(0, weight=1)  # Center everything by expanding column 0
gui.grid_columnconfigure(1, weight=1)  # Center everything by expanding column 1

# Create buttons for choosing two different files, placed in row 0, columns 0 and 1
openfiletxt1 = "Choose First File"
openfile1 = tk.Button(gui, text=openfiletxt1, command=lambda: open_file(1), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
openfile1.grid(row=0, column=0, padx=10, pady=20, ipadx=10, ipady=5, sticky="e")

openfiletxt2 = "Choose Second File"
openfile2 = tk.Button(gui, text=openfiletxt2, command=lambda: open_file(2), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
openfile2.grid(row=0, column=1, padx=10, pady=20, ipadx=10, ipady=5, sticky="w")

# Create buttons for operations, centered across both columns
addbtntxt = "Add 2 signals"
addbtn = tk.Button(gui, text=addbtntxt, command=lambda: operations(indices1, samples1, indices2, samples2, 1), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
addbtn.grid(row=1, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

subtBtnTxt = "Subtract 2 signals"
subtBtn = tk.Button(gui, text=subtBtnTxt, command=lambda: operations(indices1, samples1, indices2, samples2, 2), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
subtBtn.grid(row=2, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

multBtnTxt = "Multiply signal"
multBtn = tk.Button(gui, text=multBtnTxt, command=lambda: multiply(indices1,samples1,delay_value), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
multBtn.grid(row=3, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)
# Label for value to delay or advance, centered across both columns
title_label = tk.Label(gui, text="Value to delay or advance of first signal", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#ffffff")
title_label.grid(row=4, column=0, columnspan=2, pady=2)

# Create a frame to hold the Entry and Button next to each other, centered across both columns
frame = tk.Frame(gui, bg="#1e1e1e")
frame.grid(row=5, column=0, columnspan=2, pady=(5, 0))

# Create an Entry widget for single-line input, inside the frame
entry = tk.Entry(frame, font=("Arial", 12), bg="#333333", fg="#ffffff", insertbackground="#ffffff")
entry.pack(side="left", padx=10, ipadx=10, ipady=5)

# Create a button to read the input, inside the frame
read_input_button = tk.Button(frame, text="Read Input", command=retrieve_input, bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
read_input_button.pack(side="left", ipadx=10, ipady=5)

delaytxt="Delay Signal"
delayBtn=tk.Button(gui,text=delaytxt,command= lambda:delay_advance(indices1,samples1,delay_value,1),bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
delayBtn.grid(row=6,column=0,padx=10, pady=20, ipadx=10, ipady=5, sticky="e")

advancetxt="Advance Signal"
advanceBtn=tk.Button(gui,text=advancetxt,command= lambda:delay_advance(indices1,samples1,delay_value,2),bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
advanceBtn.grid(row=6,column=1,padx=10, pady=20, ipadx=10, ipady=5, sticky="w")

foldtxt="Fold Signal"
advanceBtn=tk.Button(gui,text=foldtxt,command= lambda:delay_advance(indices1,samples1,delay_value,3),bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
advanceBtn.grid(row=6,column=2,padx=10, pady=20, ipadx=10, ipady=5, sticky="e")

displayOriginalSignaltxt="Display Original Signal"
displayOriginalSignalBtn=tk.Button(gui,text=displayOriginalSignaltxt,command= lambda:display(indices1,samples1),bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
displayOriginalSignalBtn.grid(row=7,column=0,padx=10, pady=20, ipadx=10, ipady=5, sticky="e")

displayresultTxt="Display Result Signal"
displayResultBtn=tk.Button(gui,text=displayresultTxt,command= lambda:display(indices1,samples1,result_indices,result_samples,2),bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
displayResultBtn.grid(row=7,column=1,padx=10, pady=20, ipadx=10, ipady=5, sticky="w")
# Start the main loop
gui.mainloop()
