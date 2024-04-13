# Given the model's symmetry, we can simplify the calculation
# We know that T1 = T7, T2 = T6, T3 = T5, and T4 is the peak temperature
# We can set up equations based on this symmetry and solve for T1 through T4

def calculate_symmetrical_temperatures(delta_z, k_CFRP, k_adhesive, q_adhesive):
    # Since we have symmetry, T2 = T6 and T3 = T5, we only need to solve for T1, T2, T3, T4
    # Using a simple fixed-point iteration method

    # Initial guesses
    T1 = T2 = T3 = T4 = (processing_temp_min + processing_temp_max) / 2
    
    # Iterative method parameters
    max_iterations = 10000
    tolerance = 1e-5
    for _ in range(max_iterations):
        # Update equations based on current guess values
        T2_new = T1  # Because T1 = T2 due to symmetry
        T3_new = T2 + (q_adhesive * delta_z**2) / (2 * k_CFRP)  # Only half the heat generation term applies at T3
        T4_new = T3 + (q_adhesive * delta_z**2) / k_adhesive
        
        # Check if the new temperatures are within the tolerance
        if all(abs(T - T_new) < tolerance for T, T_new in zip([T2, T3, T4], [T2_new, T3_new, T4_new])):
            break
        # Update temperatures for the next iteration
        T2, T3, T4 = T2_new, T3_new, T4_new
    
    # Check if the temperatures are within the processing range
    if all(processing_temp_min <= T <= processing_temp_max for T in [T2, T3, T4]):
        return T1, T2, T3, T4, True
    else:
        return T1, T2, T3, T4, False

# Search for T1 within the temperature range where T2, T3, and T4 are within the processing temperature range
T1 = T_guess_min  # Start with the minimum processing temperature
found = False
while T1 <= T_guess_max and not found:
    T1, T2, T3, T4, found = calculate_symmetrical_temperatures(delta_z, k_CFRP, k_adhesive, q_adhesive)
    if not found:
        T1 += 0.1  # Increment T1 by 0.1°C

# Construct the symmetrical temperature profile
if found:
    T5 = T3
    T6 = T2
    T7 = T1
    result = (T1, T2, T3, T4, T5, T6, T7)
else:
    result = "No solution found within the temperature guess range."

result
