import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
import os

from dsp import open_file


# Example window functions
def hamming_window(N):
    return np.hamming(N)


def rectangular_window(N):
    return np.ones(N)


# Compute the impulse response for the Low-pass filter
def low_pass_filter(N, cutoff, fs, window_type='hamming'):
    # Normalize the cutoff frequency
    wc = 2 * np.pi * cutoff / fs
    n = np.arange(N)

    # Ideal low-pass filter (sinc function)
    h = np.sinc(2 * cutoff / fs * (n - (N - 1) / 2))

    # Apply window to the impulse response
    if window_type == 'hamming':
        window = hamming_window(N)
    elif window_type == 'rectangular':
        window = rectangular_window(N)
    else:
        raise ValueError("Unknown window type")

    h *= window  # Apply the window
    return h


# Compute the impulse response for High-pass filter
def high_pass_filter(N, cutoff, fs, window_type='hamming'):
    low_pass = low_pass_filter(N, cutoff, fs, window_type)
    # High-pass filter is the inverted low-pass filter
    h = np.zeros(N)
    h[N // 2] = 1
    h -= low_pass  # Subtract low-pass from delta function
    return h


# Compute the Band-pass filter by combining low and high pass filters
def band_pass_filter(N, low_cutoff, high_cutoff, fs, window_type='hamming'):
    low_pass = low_pass_filter(N, low_cutoff, fs, window_type)
    high_pass = high_pass_filter(N, high_cutoff, fs, window_type)
    return high_pass + low_pass


# Compute the Band-stop filter by combining high and low pass filters
def band_stop_filter(N, low_cutoff, high_cutoff, fs, window_type='hamming'):
    low_pass = low_pass_filter(N, low_cutoff, fs, window_type)
    high_pass = high_pass_filter(N, high_cutoff, fs, window_type)
    return low_pass - high_pass


# Convolve the signal with the FIR filter coefficients
def apply_filter(input_signal, filter_coefficients):
    return convolve(input_signal, filter_coefficients, mode='same')


# Save the filter coefficients to a text file
def save_coefficients_to_file(coefficients, filename="filter_coefficients.txt"):
    with open(filename, 'w') as f:
        for coeff in coefficients:
            f.write(f"{coeff}\n")


# Plot the filtered signal
def plot_signal(signal, title="Filtered Signal"):
    plt.plot(signal)
    plt.title(title)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()


# Main function to execute the filter design and application
def main():
    # Input from the user

    _,input_signal = open_file(1)  # Assumed file contains signal values

    filter_type = input("Enter the filter type (low, high, bandpass, bandstop): ").lower()
    N = int(input("Enter the filter order (N): "))
    fs = float(input("Enter the sampling frequency (fs): "))

    # Filter specifications
    if filter_type == 'low':
        cutoff = float(input("Enter the cutoff frequency (Hz): "))
        window_type = input("Enter window type (hamming/rectangular): ").lower()
        filter_coefficients = low_pass_filter(N, cutoff, fs, window_type)

    elif filter_type == 'high':
        cutoff = float(input("Enter the cutoff frequency (Hz): "))
        window_type = input("Enter window type (hamming/rectangular): ").lower()
        filter_coefficients = high_pass_filter(N, cutoff, fs, window_type)

    elif filter_type == 'bandpass':
        low_cutoff = float(input("Enter the lower cutoff frequency (Hz): "))
        high_cutoff = float(input("Enter the upper cutoff frequency (Hz): "))
        window_type = input("Enter window type (hamming/rectangular): ").lower()
        filter_coefficients = band_pass_filter(N, low_cutoff, high_cutoff, fs, window_type)

    elif filter_type == 'bandstop':
        low_cutoff = float(input("Enter the lower cutoff frequency (Hz): "))
        high_cutoff = float(input("Enter the upper cutoff frequency (Hz): "))
        window_type = input("Enter window type (hamming/rectangular): ").lower()
        filter_coefficients = band_stop_filter(N, low_cutoff, high_cutoff, fs, window_type)

    else:
        print("Invalid filter type")
        return

    # Apply the filter to the input signal
    filtered_signal = apply_filter(input_signal, filter_coefficients)

    # Plot the filtered signal
    plot_signal(filtered_signal)

    # Save the filter coefficients to a text file
    save_coefficients_to_file(filter_coefficients)
    print("Filter coefficients have been saved to filter_coefficients.txt")


if __name__ == "__main__":
    main()
