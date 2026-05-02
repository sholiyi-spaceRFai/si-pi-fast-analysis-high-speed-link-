import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# -------------------------------
# Parameters
# -------------------------------
bit_rate = 5e9                 # 5 Gbps
samples_per_bit = 100          # Resolution
fs = bit_rate * samples_per_bit
num_bits = 300                 # More bits → smoother eye

bit_period = 1 / bit_rate

# Time vector
t = np.arange(0, num_bits * bit_period, 1/fs)

# -------------------------------
# Generate NRZ signal
# -------------------------------
bits = np.random.randint(0, 2, num_bits)
signal = np.repeat(bits, samples_per_bit).astype(float)

# -------------------------------
# Low-pass filter (channel model)
# -------------------------------
def low_pass_filter(x, cutoff_freq, fs):
    nyq = 0.5 * fs
    norm_cutoff = cutoff_freq / nyq
    b, a = butter(2, norm_cutoff, btype='low')
    return lfilter(b, a, x)

# Two channel conditions
cutoff1 = 2.5e9   # Worse channel
cutoff2 = 4e9     # Better channel

signal_filt_1 = low_pass_filter(signal, cutoff1, fs)
signal_filt_2 = low_pass_filter(signal, cutoff2, fs)

# -------------------------------
# Eye Diagram Function
# -------------------------------
def plot_eye(ax, sig, samples_per_bit, title):
    window = 2 * samples_per_bit  # 2 UI window
    num_segments = int(len(sig) / samples_per_bit) - 1

    for i in range(num_segments):
        start = i * samples_per_bit
        end = start + window
        if end < len(sig):
            segment = sig[start:end]
            time_axis = np.linspace(0, 2, len(segment))  # in UI
            ax.plot(time_axis, segment, alpha=0.15)

    ax.set_title(title)
    ax.set_xlabel('Time (Unit Intervals)')
    ax.set_ylabel('Voltage (V)')
    ax.grid()

# -------------------------------
# Plot Side-by-Side Comparison
# -------------------------------
fig, axs = plt.subplots(1, 2)

plot_eye(axs[0], signal_filt_1, samples_per_bit, "Eye Diagram (2.5 GHz Channel)")
plot_eye(axs[1], signal_filt_2, samples_per_bit, "Eye Diagram (4 GHz Channel)")

plt.tight_layout()
plt.savefig("eye_comparison.png", dpi=300)
plt.show()

# -------------------------------
# Overlay Comparison (Optional but powerful)
# -------------------------------
plt.figure()

window = 2 * samples_per_bit
num_segments = int(len(signal_filt_1) / samples_per_bit) - 1

for i in range(num_segments):
    start = i * samples_per_bit
    end = start + window
    if end < len(signal_filt_1):
        t_axis = np.linspace(0, 2, window)

        plt.plot(t_axis, signal_filt_1[start:end], alpha=0.08, label='2.5 GHz' if i == 0 else "")
        plt.plot(t_axis, signal_filt_2[start:end], alpha=0.08, linestyle='--', label='4 GHz' if i == 0 else "")

plt.xlabel('Time (Unit Intervals)')
plt.ylabel('Voltage (V)')
plt.title('Overlay Eye Diagram Comparison')
plt.legend()
plt.grid()

plt.savefig("eye_overlay.png", dpi=300)
plt.show()

print("Eye diagram comparison complete: 2.5 GHz vs 4 GHz channel.")
