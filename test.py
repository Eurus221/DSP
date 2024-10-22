import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import numpy as np
# Main Window to start the application
def open_task1():
    task1_window()

def main_window():
    main_gui = tk.Tk()
    main_gui.title("Signal Processing Application")
    main_gui.geometry("400x200")
    main_gui.config(bg="#1e1e1e")

    # Configure the grid system to center the buttons
    main_gui.grid_columnconfigure(0, weight=1)  # Add weight to the first (left) column
    main_gui.grid_columnconfigure(3, weight=1)  # Add weight to the third (right) column

    task1_button = tk.Button(main_gui, text="Task 1", width=5, height=1, command=open_task1, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task1_button.grid(row=0, column=1,padx=(5, 2), pady=5)  # Place in the first row and second column (centered)

    task2_button = tk.Button(main_gui, text="Task 2", width=5, height=1, command=task2, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task2_button.grid(row=0, column=2,padx=(2,5),  pady=5)  # Place in the first row and third column (next to Task 1)
    

    main_gui.mainloop()

# Task 1 Window
indices1, samples1, indices2, samples2 = [], [], [], []  # Variables to store the signals
result_indices, result_samples = [], []
delay_value = 0


 
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

def WriteSignalFile(indices, samples, size):
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
    global result_indices, result_samples
    result_indices, result_samples = [], []
    i, j = 0, 0
    if operation_type == 1:  # Addition
        while i < len(ind1) and j < len(ind2):
            if ind1[i] == ind2[j]:
                result_indices.append(ind1[i])
                result_samples.append(samp1[i] + samp2[j])
                i += 1
                j += 1
            elif ind1[i] < ind2[j]:
                result_indices.append(ind1[i])
                result_samples.append(samp1[i])
                i += 1
            else:
                result_indices.append(ind2[j])
                result_samples.append(samp2[j])
                j += 1

        while i < len(ind1):
            result_indices.append(ind1[i])
            result_samples.append(samp1[i])
            i += 1

        while j < len(ind2):
            result_indices.append(ind2[j])
            result_samples.append(samp2[j])
            j += 1
        WriteSignalFile(result_indices, result_samples, len(result_samples))
    elif operation_type == 2:  # Subtraction
        while i < len(ind1) and j < len(ind2):
            if ind1[i] == ind2[j]:
                result_indices.append(ind1[i])
                result_samples.append(samp1[i] - samp2[j])
                i += 1
                j += 1
            elif ind1[i] < ind2[j]:
                result_indices.append(ind1[i])
                result_samples.append(samp1[i])
                i += 1
            else:
                result_indices.append(ind2[j])
                result_samples.append(samp2[j])
                j += 1

        while i < len(ind1):
            result_indices.append(ind1[i])
            result_samples.append(samp1[i])
            i += 1

        while j < len(ind2):
            result_indices.append(ind2[j])
            result_samples.append(samp2[j])
            j += 1
        WriteSignalFile(result_indices, result_samples, len(result_samples))

def multiply(ind, samp, val):
    global result_indices, result_samples
    result_indices = ind
    result_samples = [x * float(val) for x in samp]
    WriteSignalFile(result_indices, result_samples, len(result_samples))

def delay_advance(ind, samp, delay_val, coord):
    global result_indices, result_samples
    delay_val = int(delay_val)
    result_indices = [i - delay_val for i in ind] if coord == 1 else [i + delay_val for i in ind]
    result_samples = samp
    WriteSignalFile(result_indices, result_samples, len(result_samples))

def display(ind1=0, samp1=0, ind2=0, samp2=0, coord=1):
    if coord == 1:
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

def task1_window():
    # Create the main window
    gui = tk.Toplevel()
    gui.title("Signal Reading and Processing Simulation")
    gui.geometry("1000x700")
    gui.config(bg="#1e1e1e")


    # GUI setup for buttons, labels, and entry
    gui.grid_columnconfigure(0, weight=1)
    gui.grid_columnconfigure(1, weight=1)

    openfile1 = tk.Button(gui, text="Choose First File", command=lambda: open_file(1), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    openfile1.grid(row=0, column=0, padx=10, pady=20, ipadx=10, ipady=5, sticky="e")

    openfile2 = tk.Button(gui, text="Choose Second File", command=lambda: open_file(2), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    openfile2.grid(row=0, column=1, padx=10, pady=20, ipadx=10, ipady=5, sticky="w")

    addbtn = tk.Button(gui, text="Add 2 signals", command=lambda: operations(indices1, samples1, indices2, samples2, 1), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    addbtn.grid(row=1, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    subtbtn = tk.Button(gui, text="Subtract 2 signals", command=lambda: operations(indices1, samples1, indices2, samples2, 2), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    subtbtn.grid(row=2, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    multbtn = tk.Button(gui, text="Multiply signal", command=lambda: multiply(indices1, samples1, entry.get()), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    multbtn.grid(row=3, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    delaybtn = tk.Button(gui, text="Delay signal", command=lambda: delay_advance(indices1, samples1, entry.get(), 1), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    delaybtn.grid(row=4, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    entry = tk.Entry(gui, width=20, font=("Arial", 12))
    entry.grid(row=5, column=0, columnspan=2, pady=10)

    displaybtn1 = tk.Button(gui, text="Display Original Signal", command=lambda: display(indices1, samples1, coord=1), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    displaybtn1.grid(row=6, column=0, pady=10, ipadx=10, ipady=5)

    displaybtn2 = tk.Button(gui, text="Display Result Signal", command=lambda: display(result_indices, result_samples, coord=2), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    displaybtn2.grid(row=6, column=1, pady=10, ipadx=10, ipady=5)

    gui.mainloop()

def gen_waves(type,amp,theta,analog_freq,sampling_freq,duration):

    t = np.arange(0,duration,1/sampling_freq)
    if type == 0:
        wave=amp*np.sin(2*np.pi*analog_freq*t+theta)
        return wave
    elif type == 1:
        wave=amp*np.cos(2*np.pi*analog_freq*t+theta)
        return wave
def task2():
    entry

# Start the application
main_window()
