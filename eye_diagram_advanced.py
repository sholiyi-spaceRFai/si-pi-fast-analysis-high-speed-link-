import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# -------------------------------
# Parameters
# -------------------------------
bit_rate = 5e9
samples_per_bit = 100
fs = bit_rate * samples_per_bit
num_bits = 300
bit_period = 1 / bit_rate

# Noise & jitter parameters
noise_std = 0.05        # Voltage noise level (V)
jitter_std = 0.02       # Fraction of UI (timing jitter)

# -------------------------------
# Generate NRZ Signal
# -------------------------------
bits = np.random.randint(0, 2, num_bits)
signal = np.repeat(bits, samples_per_bit).astype(float)

# -------------------------------
# Channel (Low-pass filter)
# -------------------------------
def low_pass_filter(x, cutoff_freq, fs):
    nyq = 0.5 * fs
    norm_cutoff = cutoff_freq / nyq
    b, a = butter(2, norm_cutoff, btype='low')
    return lfilter(b, a, x)

cutoff = 4e9
signal_filtered = low_pass_filter(signal, cutoff, fs)

# -------------------------------
# Add Timing Jitter
# -------------------------------
def apply_jitter(signal, samples_per_bit, jitter_std):
    jittered_signal = np.zeros_like(signal)
    num_bits = int(len(signal) / samples_per_bit)

    for i in range(num_bits):
        start = i * samples_per_bit
        end = start + samples_per_bit

        # Random shift per bit
        shift = int(np.random.normal(0, jitter_std * samples_per_bit))

        src_start = max(0, start + shift)
        src_end = min(len(signal), end + shift)

        dst_start = start
        dst_end = start + (src_end - src_start)

        if src_end > src_start:
            jittered_signal[dst_start:dst_end] = signal[src_start:src_end]

    return jittered_signal

signal_jittered = apply_jitter(signal_filtered, samples_per_bit, jitter_std)

# -------------------------------
# Add Voltage Noise
# -------------------------------
noise = np.random.normal(0, noise_std, len(signal))
signal_noisy = signal_jittered + noise

# -------------------------------
# Eye Diagram Function
# -------------------------------
def plot_eye(ax, sig, samples_per_bit, title):
    window = 2 * samples_per_bit
    num_segments = int(len(sig) / samples_per_bit) - 1

    for i in range(num_segments):
        start = i * samples_per_bit
        end = start + window
        if end < len(sig):
            segment = sig[start:end]
            time_axis = np.linspace(0, 2, len(segment))
            ax.plot(time_axis, segment, alpha=0.12)

    ax.set_title(title)
    ax.set_xlabel('Time (Unit Intervals)')
    ax.set_ylabel('Voltage (V)')
    ax.grid()

# -------------------------------
# Plot Comparison
# -------------------------------
fig, axs = plt.subplots(1, 3)

plot_eye(axs[0], signal, samples_per_bit, "Ideal Signal")
plot_eye(axs[1], signal_filtered, samples_per_bit, "4 GHz Channel")
plot_eye(axs[2], signal_noisy, samples_per_bit, "4 GHz + Jitter + Noise")

plt.tight_layout()
plt.savefig("eye_advanced.png", dpi=300)
plt.show()

print("Advanced eye diagram generated with jitter and noise.")
