from dsp import ReadSignalFile
from dsp import display
from dsp import open_file
from signalcompare import SignalComaprePhaseShift
from signalcompare import SignalComapreAmplitude

import matplotlib.pyplot as plt
import numpy as np 
import tkinter as tk
def idft_dft(decider,freq):
   x1,x=open_file(1)
   imag=-1j
   if decider==0:#idft
      x= comp_constructor(x1,x)
      imag=1j

      print(x)
   out=[]
   for k in range(len(x)):
      sum=0
      for n in range(len(x)):
        res=x[n]*np.exp(imag*k*2*np.pi*n/len(x))
        sum+=res 
      out.append(sum)

   if decider==1: #dft
      phase_height(out,freq)
   else:
      length=len(out)
      out=[i/length for i in out]
      _,ans=open_file(1)
      if SignalComapreAmplitude(ans,out):
        print("passed IDFT !!!!!!!!!!!")
        display(coord=2,samp2=out,ind2=range(len(out)))
      else: 
         print("failed IDFT !!!!!!!!!!!")

    

def phase_height(out,freq):
    magnitudes=[np.abs(z) for z in out]
    phases=[np.arctan2(z.imag,z.real) for z in out]
    step = (2*np.pi)/len(out)/freq
    x_axis=[i*step for i in range(len(out))]
    ampAnswer,phaseAnswer=open_file(1)
    if SignalComapreAmplitude(ampAnswer,magnitudes) and SignalComaprePhaseShift(phaseAnswer,phases):
       print("passed DFT !!!!!!!!!!!!!")
       display(coord=2, samp2=magnitudes,ind2=x_axis)
       display(coord=2, samp2=phases,ind2=x_axis)
    else: 
       print("Failed DFT!!!!!!!!!!!")

def comp_constructor(a,p):
    a= np.array(a)
    p= np.array(p)
    complex_numbers = a * np.exp(1j * p)
    return complex_numbers.tolist()

def task5_window():
    root = tk.Tk()
    root.title("Dark Theme Example")
    root.geometry("400x200")
    root.config(bg="#1e1e1e")

    # Add a text field
    text_field = tk.Entry(root, font=("Arial", 12), width=30, bg="#333333", fg="#ffffff", insertbackground="#ffffff")
    text_field.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    # Add two buttons
    button1 = tk.Button(root, text="DFT", command=lambda:idft_dft(1,int(text_field.get())), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button1.grid(row=1, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    button2 = tk.Button(root, text="IDFT", command=lambda:idft_dft(0,int(text_field.get())), bg="#333333", fg="#ffffff", font=("Arial", 12), activebackground="#222222", activeforeground="#ffffff")
    button2.grid(row=1, column=1, padx=20, pady=10, ipadx=10, ipady=5)
    

    # Run the main Tkinter loop
    root.mainloop()

      