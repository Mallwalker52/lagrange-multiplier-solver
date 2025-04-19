# app.py

import streamlit as st
from sympy import symbols, diff, solve, Eq, sympify

st.title("Flexible Lagrange Multipliers Solver (Minimize or Maximize)")

st.write("Enter your objective function and one or two constraints below:")

# Form inputs
f_input = st.text_input("Objective Function (example: x^2 + y^2 + z^2)", value="x^2 + y^2 + z^2")
vars_input = st.text_input("Variables (comma-separated, e.g., x, y, z)", value="x, y, z")
constraint1_input = st.text_input("Constraint 1 (required, e.g., x + y + z = 1)", value="x + y + z = 1")
constraint2_input = st.text_input("Constraint 2 (optional, e.g., x - y = 0)", value="")

optimization_type = st.radio("Do you want to minimize or maximize?", ("Minimize", "Maximize"))

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

        # Adjust function based on optimization type
        if optimization_type == "Maximize":
            f = -f

        # Parse constraints
        constraints = []
        if constraint1_input:
            if "=" in constraint1_input:
                left, right = constraint1_input.split("=")
                constraints.append(Eq(sympify(left), sympify(right)))
            else:
                constraints.append(Eq(sympify(constraint1_input), 0))
        if constraint2_input:
            if "=" in constraint2_input:
                left, right = constraint2_input.split("=")
                constraints.append(Eq(sympify(left), sympify(right)))
            else:
                constraints.append(Eq(sympify(constraint2_input), 0))

        # Create Lagrangian
        lambdas = symbols([f"lam{i+1}" for i in range(len(constraints))])
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
                f_val = sympify(f_input).subs(sol)
                st.write(f"**Objective function value** = {f_val}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Error: {str(e)}")
