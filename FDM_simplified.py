from sympy import symbols, solve

# Define the variables
T1, T2, T3, T4 = symbols('T1 T2 T3 T4')

# Derived expressions for T2, T3, T4
T4_expr = T3 - 11.25
T2_expr = T3 + 2025/7000
T1_expr = T3 + 4050/7000

# Initialize values and list to collect results
t3_values = []
t4_values = []
t1_range = []

# Loop over a reasonable range of T1 and calculate T3, T4
for t1_guess in range(100, 300):  # Broad range to find feasible T1
    # Solve for T3 when T1 is set to a guess value
    t3_solution = solve(T1_expr - t1_guess, T3)
    if t3_solution:
        t3 = t3_solution[0].evalf()  # Numerical value of T3
        t4 = T4_expr.subs(T3, t3).evalf()  # Calculate corresponding T4

        # Check if both T3 and T4 are within the desired range
        if 121 <= t3 <= 177 and 121 <= t4 <= 177:
            t3_values.append(t3)
            t4_values.append(t4)
            t1_range.append(t1_guess)

# Results
t1_range, t3_values, t4_values
