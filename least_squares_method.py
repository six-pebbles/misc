import numpy as np

# Given data from the image
I_dc = np.array([1.67, 2.4, 3.93, 5.3, 6.52, 7.64, 8.65])  # DC current in Amperes
speed_rpm = np.array([2411, 2356, 2271, 2193, 2127, 2071, 2011])  # Speed in RPM
V_dc = np.array([36] * 7)  # Fixed DC voltage of 36V for all measurements

# Convert speed from RPM to rad/s, ω = 2πn/60
omega_r = 2 * np.pi * speed_rpm / 60

# Create the A matrix
A = np.column_stack((I_dc, omega_r))

# Perform the least squares fit to find R_eq and K_v_eq
coefficients, residuals, rank, s = np.linalg.lstsq(A, V_dc, rcond=None)

# Extract the coefficients
R_eq, K_v_eq = coefficients
R_eq, K_v_eq
