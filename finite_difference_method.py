import numpy as np

# Constants
k_CFRP = 7  # W/(m*K)
k_adhesive = 0.2  # W/(m*K)
q_adhesive = 4.5e5  # W/m^3
delta_z = 0.001  # m
T_processing_min = 121  # °C
T_processing_max = 177  # °C

# Number of temperatures we are solving for
num_temps = 7

# Initialize temperatures, assuming a linear distribution as a first guess
T = np.linspace(T_processing_min, T_processing_max, num_temps)

# Set up the equations as lambda functions
equations = [
    lambda T: (T[0] - 2*T[1] + T[2])/delta_z**2,
    lambda T: k_CFRP*(T[1] - T[2])/delta_z + k_adhesive*(T[3] - T[2])/delta_z + q_adhesive*delta_z/2,
    lambda T: (T[2] - 2*T[3] + T[4])/delta_z**2 + q_adhesive/k_adhesive,
    lambda T: k_adhesive*(T[3] - T[4])/delta_z + k_CFRP*(T[5] - T[4])/delta_z + q_adhesive*delta_z/2,
    lambda T: (T[4] - 2*T[5] + T[6])/delta_z**2
]

# Iteration settings
max_iterations = 1000
tolerance = 1e-5

# Perform the iteration
for iteration in range(max_iterations):
    # Update T2 to T6 based on the equations
    T[1] = 2*T[2] - T[3]  # From equation 1
    T[2] = (k_CFRP*T[1] + k_adhesive*T[3] + q_adhesive*delta_z/2) * delta_z / (k_CFRP + k_adhesive) + T[3]  # From equation 2
    T[4] = 2*T[3] - T[5] - q_adhesive*delta_z**2/k_adhesive  # From equation 4
    T[5] = (k_adhesive*T[4] + k_CFRP*T[6] + q_adhesive*delta_z/2) * delta_z / (k_adhesive + k_CFRP) + T[4]  # From equation 5

    # Check if T3, T4, T5 are within the processing temperature range
    if all(T_processing_min <= T[i] <= T_processing_max for i in range(2, 5)):
        break

    # Check if T1 or T7 need to be adjusted
    if T[2] < T_processing_min:
        T[0] += (T_processing_min - T[2]) / 2
        T[6] = T[0]  # Assuming T1 = T7
    elif T[4] > T_processing_max:
        T[0] -= (T[4] - T_processing_max) / 2
        T[6] = T[0]  # Assuming T1 = T7

    # Check for convergence
    residuals = [equation(T) for equation in equations]
    max_residual = max(abs(res) for res in residuals)
    if max_residual < tolerance:
        break

if iteration == max_iterations - 1:
    print("Max iterations reached without convergence.")
else:
    print(f"Converged after {iteration} iterations.")

# Output the temperatures
T
