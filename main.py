import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np
from dsp import task1_window
from task2 import task2_window
from task3 import task3_window
from task4 import task4_window
from task5 import task5_window
from task6 import task6_window
from task7 import task7_window

# Main Window to start the application


def main_window():
    main_gui = tk.Tk()
    main_gui.title("Signal Processing Application")
    main_gui.geometry("400x200")
    main_gui.config(bg="#1e1e1e")

    # Configure the grid system to center the buttons
    main_gui.grid_columnconfigure(0, weight=1)  # Add weight to the first (left) column
    main_gui.grid_columnconfigure(3, weight=1)  # Add weight to the third (right) column

    task1_button = tk.Button(main_gui, text="Task 1", width=5, height=1, command=task1_window, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task1_button.grid(row=0, column=1,padx=(5, 2), pady=5)  # Place in the first row and second column (centered)

    task2_button = tk.Button(main_gui, text="Task 2", width=5, height=1, command=task2_window, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task2_button.grid(row=0, column=2,padx=(2,5),  pady=5)  # Place in the first row and third column (next to Task 1)
    
    task3_button = tk.Button(main_gui, text="Task 3", width=5, height=1, command=task3_window, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task3_button.grid(row=1, column=1,padx=(5, 2), pady=5)  # Place in the first row and second column (centered)
    
    task4_button = tk.Button(main_gui, text="Task 4", width=5, height=1, command=task4_window, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task4_button.grid(row=1, column=2,padx=(5, 2), pady=5)  # Place in the first row and second column (centered)

    task5_button = tk.Button(main_gui, text="Task 5", width=5, height=1, command=task5_window, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task5_button.grid(row=2, column=1,padx=(5, 2), pady=5)  # Place in the first row and second column (centered)
    
    task6_button = tk.Button(main_gui, text="Task 6", width=5, height=1, command=task6_window, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task6_button.grid(row=2, column=2,padx=(5, 2), pady=5)  # Place in the first row and second column (centered)
    
    task5_button = tk.Button(main_gui, text="Task 7", width=5, height=1, command=task7_window, bg="#333333", fg="#ffffff", font=("Arial", 16), activebackground="#222222", activeforeground="#ffffff")
    task5_button.grid(row=3, column=1,padx=(5, 2), pady=5)  # Place in the first row and second column (centered)
    
    main_gui.mainloop()

# Start the application
main_window()
 