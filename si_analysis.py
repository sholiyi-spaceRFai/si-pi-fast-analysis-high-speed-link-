import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Signal Integrity Analysis
# -------------------------------

# Parameters
Z0 = 50            # Characteristic impedance (Ohms)
ZL = 75            # Load impedance (Ohms) - mismatch case
V_step = 1.0       # Step input voltage (V)
t = np.linspace(0, 10e-9, 1000)  # Time vector (10 ns)

# Reflection coefficient
Gamma = (ZL - Z0) / (ZL + Z0)

# Incident signal (step)
V_incident = V_step * np.ones_like(t)

# Simulated reflected signal (delayed reflection)
delay = 2e-9  # 2 ns delay
V_reflected = np.zeros_like(t)

for i in range(len(t)):
    if t[i] >= delay:
        V_reflected[i] = Gamma * V_step

# Total voltage
V_total = V_incident + V_reflected

# -------------------------------
# Plotting
# -------------------------------
plt.figure()
plt.plot(t * 1e9, V_incident, linestyle='--', label='Incident Wave')
plt.plot(t * 1e9, V_reflected, linestyle=':', label='Reflected Wave')
plt.plot(t * 1e9, V_total, label='Total Voltage')

plt.xlabel('Time (ns)')
plt.ylabel('Voltage (V)')
plt.title('Signal Integrity: Reflection Due to Impedance Mismatch')
plt.legend()
plt.grid()

plt.savefig("si_plot.png", dpi=300)
plt.show()

# Print key result
print(f"Reflection Coefficient (Gamma): {Gamma:.2f}")
