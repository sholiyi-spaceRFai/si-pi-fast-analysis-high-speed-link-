import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Power Integrity Analysis
# -------------------------------

# Parameters
V_supply = 1.0          # Supply voltage (V)
I_step = 0.5            # Transient current (A)
t = np.linspace(0, 5e-6, 1000)  # Time (5 us)

# Capacitor values
C_small = 1e-6   # 1 uF
C_large = 10e-6  # 10 uF

# Current step starts at 1 us
t_step = 1e-6

# Voltage droop function
def voltage_droop(C):
    V = np.ones_like(t) * V_supply
    for i in range(len(t)):
        if t[i] >= t_step:
            dt = t[i] - t_step
            V[i] = V_supply - (I_step * dt / C)
    return V

V_small = voltage_droop(C_small)
V_large = voltage_droop(C_large)

# -------------------------------
# Plotting
# -------------------------------
plt.figure()
plt.plot(t * 1e6, V_small, label='1 uF Decoupling Cap')
plt.plot(t * 1e6, V_large, linestyle='--', label='10 uF Decoupling Cap')

plt.xlabel('Time (µs)')
plt.ylabel('Voltage (V)')
plt.title('Power Integrity: Voltage Droop Under Transient Load')
plt.legend()
plt.grid()

plt.savefig("pi_plot.png", dpi=300)
plt.show()

# Print insight
print("Larger capacitance reduces voltage droop and improves power stability.")
