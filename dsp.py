import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


signal = []
indices1, samples1, indices2, samples2 = [], [], [], []  # Variables to store the signals

result_indices,result_samples=[],[]
delay_value=0

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
    i, j = 0, 0
    if operation_type == 1:
        while i < len(ind1) and j < len(ind2):
            if ind1[i] == ind2[j]:
                # Matching indices, add the samples
                result_indices.append(ind1[i])
                result_samples.append(samp1[i] + samp2[j])
                i += 1
                j += 1
            elif ind1[i] < ind2[j]:
                # Append the sample from ind1 as ind1[i] < ind2[j]
                result_indices.append(ind1[i])
                result_samples.append(samp1[i])
                i += 1
            else:
                # Append the sample from ind2 as ind2[j] < ind1[i]
                result_indices.append(ind2[j])
                result_samples.append(samp2[j])
                j += 1
        
        # Step 2: Append remaining elements from ind1 or ind2
        while i < len(ind1):
            result_indices.append(ind1[i])
            result_samples.append(samp1[i])
            i += 1
        
        while j < len(ind2):
            result_indices.append(ind2[j])
            result_samples.append(samp2[j])
            j += 1
        AddSignalSamplesAreEqual("Signal1.txt","Signal2.txt",result_indices,result_samples)
    elif operation_type == 2:
        while i < len(ind1) and j < len(ind2):
            if ind1[i] == ind2[j]:
                # Matching indices, add the samples
                result_indices.append(ind1[i])
                result_samples.append(samp1[i] - samp2[j])
                i += 1
                j += 1
            elif ind1[i] < ind2[j]:
                # Append the sample from ind1 as ind1[i] < ind2[j]
                result_indices.append(ind1[i])
                result_samples.append(samp1[i])
                i += 1
            else:
                # Append the sample from ind2 as ind2[j] < ind1[i]
                result_indices.append(ind2[j])
                result_samples.append(samp2[j])
                j += 1
        
        # Step 2: Append remaining elements from ind1 or ind2
        while i < len(ind1):
            result_indices.append(ind1[i])
            result_samples.append(samp1[i])
            i += 1
        
        while j < len(ind2):
            result_indices.append(ind2[j])
            result_samples.append(samp2[j])
            j += 1
        SubSignalSamplesAreEqual("Signal1.txt","Signal2.txt",result_indices,result_samples)
    WriteSignalFile(result_indices,result_samples,len(result_samples))
    print("result indices",result_indices)
    print("result samples",result_samples)
    
def multiply(ind, samp, val):
    global result_indices, result_samples
    signal= dict(zip(ind,samp))
    result_indices = ind
    result_samples = [signal[i] * float(val) for i in result_indices]
    WriteSignalFile(result_indices,result_samples,len(result_samples))
    MultiplySignalByConst(float(val),result_indices,result_samples)
    print("result indices", result_indices)
    print("result samples", result_samples)

def AddSignalSamplesAreEqual(userFirstSignal,userSecondSignal,Your_indices,Your_samples):
    if(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal2.txt'):
        file_name="add.txt"  # write here the path of the add output file
    expected_indices,expected_samples=ReadSignalFile(file_name)          
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Addition Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Addition Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Addition Test case failed, your signal have different values from the expected one") 
            return
    print("Addition Test case passed successfully")

def ShiftSignalByConst(Shift_value,Your_indices,Your_samples):
    if(Shift_value==3):  #x(n+k)
        file_name="advance3.txt" # write here the path of delay3 output file
    elif(Shift_value==-3): #x(n-k)
        file_name="delay3.txt" # write here the path of advance3 output file
        
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Shift by "+str(Shift_value)+" Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Shift by "+str(Shift_value)+" Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Shift by "+str(Shift_value)+" Test case failed, your signal have different values from the expected one") 
            return
    print("Shift by "+str(Shift_value)+" Test case passed successfully")

def display(ind1=0,samp1=0,ind2=0,samp2=0,coord=1):
    if coord==1:
        plt.figure(figsize=(10, 6))
        plt.plot(ind1, samp1, label='Original signal')
        plt.stem(ind1, samp1, linefmt='r-', markerfmt='ro', basefmt=" ", label="Original signal")
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Signal Plot')
        plt.legend()
        plt.grid(True)
        plt.show()

    elif coord == 2:
        plt.figure(figsize=(10, 6))
        plt.plot(result_indices, result_indices, label='Result signal')
        #plt.stem(result_indices, result_indices, linefmt='r-', markerfmt='ro', basefmt=" ", label="Result")
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Signal Plot')
        plt.legend()
        plt.grid(True)
        plt.show()

def MultiplySignalByConst(User_Const,Your_indices,Your_samples):
    if(User_Const==5):
        file_name="mul5.txt"  # write here the path of the mul5 output file
        
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Multiply by "+str(User_Const)+ " Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Multiply by "+str(User_Const)+" Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Multiply by "+str(User_Const)+" Test case failed, your signal have different values from the expected one") 
            return
    print("Multiply by "+str(User_Const)+" Test case passed successfully")

def SubSignalSamplesAreEqual(userFirstSignal,userSecondSignal,Your_indices,Your_samples):
    if(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal2.txt'):
        file_name="subtract.txt" # write here the path of the subtract output file
        
    expected_indices,expected_samples=ReadSignalFile(file_name)   
    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Subtraction Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Subtraction Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Subtraction Test case failed, your signal have different values from the expected one") 
            return
    print("Subtraction Test case passed successfully")
   
def Folding(Your_indices,Your_samples):
    file_name = "folding.txt"  # write here the path of the folding output file
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Folding Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Folding Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Folding Test case failed, your signal have different values from the expected one") 
            return
    print("Folding Test case passed successfully")
def delay_advance(ind,samp,delayValue,coord):
    global result_indices,result_samples
    delayValue=int(delayValue)
    l=len(ind)
    if coord == 1:
        result_indices=[i - delayValue for i in ind]
        result_samples=samp
        print(result_indices)
        print(result_samples)
        ShiftSignalByConst(delayValue,result_indices,result_samples)
    elif coord == 2:
        result_indices=[i+delayValue for i in ind]
        result_samples=samp
        print(result_indices)
        print(result_samples)
        ShiftSignalByConst(-delayValue,result_indices,result_samples)
    elif coord == 3:
        result_indices=[]
        result_samples=[]
        for i in range(l):
            result_indices.append(ind[l-i-1]*-1)
            result_samples.append(samp[l-i-1])
        print(result_indices)
        print(result_samples)  
        Folding(result_indices,result_samples)
    WriteSignalFile(result_indices,result_samples,len(result_samples))
 
