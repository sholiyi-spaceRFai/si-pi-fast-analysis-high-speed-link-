import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Parameters
# -------------------------------
V_supply = 1.0
t = np.linspace(0, 2e-6, 2000)  # 2 us time window

# Load transient
I_step = 1.0        # Higher current → worse PI
t_step = 0.5e-6

# Decoupling network
C = 1e-6            # 1 uF
ESR = 0.05          # 50 mOhm (resistance)
ESL = 1e-9          # 1 nH (inductance)

dt = t[1] - t[0]

# -------------------------------
# Initialize variables
# -------------------------------
V = np.ones_like(t) * V_supply
I_L = 0             # Inductor current
V_C = V_supply      # Capacitor voltage

# -------------------------------
# Time-domain simulation
# -------------------------------
for i in range(1, len(t)):

    # Load current
    if t[i] >= t_step:
        I_load = I_step
    else:
        I_load = 0

    # Inductor voltage: V = L di/dt
    dI_L = (V[i-1] - V_C) / ESL * dt
    I_L += dI_L

    # Capacitor current
    I_C = I_L - I_load

    # Capacitor voltage update
    dV_C = I_C / C * dt
    V_C += dV_C

    # ESR drop
    V[i] = V_C - I_C * ESR

# -------------------------------
# Ideal Case (for comparison)
# -------------------------------
V_ideal = np.ones_like(t) * V_supply
for i in range(len(t)):
    if t[i] >= t_step:
        V_ideal[i] = V_supply - (I_step * (t[i] - t_step) / C)

# -------------------------------
# Plot Results
# -------------------------------
plt.figure()

plt.plot(t * 1e6, V_ideal, linestyle='--', label='Ideal Capacitor')
plt.plot(t * 1e6, V, label='With ESR + ESL (Degraded PI)')

plt.xlabel('Time (µs)')
plt.ylabel('Voltage (V)')
plt.title('Power Integrity Degradation: ESR & ESL Effects')
plt.legend()
plt.grid()

plt.savefig("pi_degraded.png", dpi=300)
plt.show()

print("Degraded PI simulation complete.")
