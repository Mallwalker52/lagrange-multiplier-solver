# app.py

import streamlit as st
from sympy import symbols, diff, solve, Eq, sympify

st.title("Lagrange Multipliers Solver")

st.write("Enter your objective function and two constraints below:")

# Form inputs
f_input = st.text_input("Objective Function (example: x^2 + y^2 + z^2)", value="x^2 + y^2 + z^2")
vars_input = st.text_input("Variables (comma-separated, example: x, y, z)", value="x, y, z")
constraint1_input = st.text_input("Constraint 1 (example: x + y + z = 1)", value="x + y + z = 1")
constraint2_input = st.text_input("Constraint 2 (example: x - y = 0)", value="x - y = 0")

if st.button("Solve"):
    try:
        # Preprocess input
        f_input = f_input.replace("^", "**")
        constraint1_input = constraint1_input.replace("^", "**")
        constraint2_input = constraint2_input.replace("^", "**")

        # Parse variables
        var_names = [v.strip() for v in vars_input.split(",")]
        variables = symbols(var_names)

        # Parse function
        f = sympify(f_input)

        # Parse constraints
        constraints = []
        for c in [constraint1_input, constraint2_input]:
            if "=" in c:
                left, right = c.split("=")
                constraints.append(Eq(sympify(left), sympify(right)))
            else:
                constraints.append(Eq(sympify(c), 0))

        # Create Lagrangian
        lambdas = symbols(['lam1', 'lam2'])
        L = f
        for lam, constraint in zip(lambdas, constraints):
            L -= lam * (constraint.lhs - constraint.rhs)

        # Set up system of equations
        system = []
        for v in variables:
            system.append(Eq(diff(L, v), 0))
        for constraint in constraints:
            system.append(constraint)

        # Solve
        all_symbols = list(variables) + list(lambdas)
        solutions = solve(system, all_symbols, dict=True)

        if not solutions:
            st.error("No solutions found.")
        else:
            for idx, sol in enumerate(solutions, 1):
                st.success(f"Solution {idx}:")
                for var in all_symbols:
                    if var in sol:
                        st.write(f"**{var}** = {sol[var]}")
                # Evaluate f at solution
                f_val = f.subs(sol)
                st.write(f"**Objective function value** = {f_val}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Error: {str(e)}")
