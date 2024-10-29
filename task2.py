import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import matplotlib.pyplot as plt

def gen_waves(wave_type, amp, theta, analog_freq, sampling_freq):
    # Convert the input values to the correct data types
    amp = float(amp)
    theta = float(theta)
    analog_freq = float(analog_freq)
    sampling_freq = float(sampling_freq)

    n = np.arange(0, 10,1/sampling_freq)
    t = np.linspace(0, 10, 1000)
    
    if wave_type == 0:  # Sine wave
        analogWave = amp * np.sin(2 * np.pi * analog_freq * t + (theta*np.pi)/180)
        discreteWave = amp * np.sin(2 * np.pi * analog_freq  * n +(theta*np.pi)/180)
        display(analogWave, discreteWave, n, t)
    elif wave_type == 1:  # Cosine wave
        analogWave = amp * np.cos(2 * np.pi * analog_freq * t + theta*np.pi)
        discreteWave = amp * np.cos(2 * np.pi * analog_freq * n + theta*np.pi)
        display(analogWave, discreteWave, n, t)

def display(analogWave, discreteWave, n, t):
    plt.figure(figsize=(10, 6))

    # Plot the continuous wave
    plt.plot(t, analogWave, label="Continuous", color="blue")

    # Plot the discrete wave with vertical lines using plt.stem
    plt.stem(n, discreteWave, linefmt='r-', markerfmt='ro', basefmt=" ", label="Discrete")

    plt.title('Signal Plot')
    plt.legend()
    plt.grid(True)
    plt.show()


# Function to add placeholder (hint) text in Entry fields
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(entry, placeholder))

def clear_placeholder(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg="black")  # Change text color to black when editing

def restore_placeholder(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="gray")  # Change text color to gray for placeholder

def task2_window():
    gui = tk.Toplevel()
    gui.title("Signal Reading and Processing Simulation")
    gui.geometry("1000x700")
    gui.config(bg="#1e1e1e")
    gui.grid_columnconfigure(0, weight=1)
    gui.grid_columnconfigure(1, weight=1)

    # Widgets with padding and placeholders
    wave_type_combo = Combobox(gui, values=["Sine", "Cosine"], state="readonly")
    wave_type_combo.grid(row=0, column=0, padx=10, pady=10, ipady=5)

    amplitude = tk.Entry(gui, width=20, font=("Arial", 12), fg="gray")
    amplitude.grid(row=1, column=0, padx=10, pady=10, ipady=5)
    add_placeholder(amplitude, "Enter amplitude")

    frequency = tk.Entry(gui, width=20, font=("Arial", 12), fg="gray")
    frequency.grid(row=2, column=0, padx=10, pady=10, ipady=5)
    add_placeholder(frequency, "Enter frequency")

    theta = tk.Entry(gui, width=20, font=("Arial", 12), fg="gray")
    theta.grid(row=3, column=0, padx=10, pady=10, ipady=5)
    add_placeholder(theta, "Enter theta")

    samplingFrequency = tk.Entry(gui, width=20, font=("Arial", 12), fg="gray")
    samplingFrequency.grid(row=4, column=0, padx=10, pady=10, ipady=5)
    add_placeholder(samplingFrequency, "Enter sampling frequency")

    displayBTN = tk.Button(gui, text="Display Wave", 
                           command=lambda: gen_waves(
                               wave_type_combo.current(), 
                               amplitude.get(), 
                               theta.get(), 
                               frequency.get(), 
                               samplingFrequency.get()
                           ))
    displayBTN.grid(row=5, column=0, padx=10, pady=10)
    gui.mainloop()


