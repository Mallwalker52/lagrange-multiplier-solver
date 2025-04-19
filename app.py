# app.py

import streamlit as st
from sympy import symbols, diff, solve, Eq, sympify

st.title("Flexible Lagrange Multipliers Solver (Minimize or Maximize)")

# Instructions Section
with st.expander("📚 Instructions (Click to Expand)", expanded=False):
    st.markdown("""
**How to Enter Inputs:**
- **Multiplication** must be explicit: write `2*(x*y)` instead of `2(x*y)` or `2xy`
- **Exponents:** use `^` for powers (e.g., `x^2` means x squared)
- **Square Roots:** write as `(expression)^(1/2)` (e.g., `(x*y)^(1/2)` means √(xy))
- **Constraints** must use `=` (e.g., `2*(x*y + x*z + y*z) = 48`)
- **Variables** must be separated by commas (e.g., `x, y, z`)
- **If you have no second constraint**, leave it blank
- The app automatically handles `^` by converting it internally to Python powers

If you follow these rules, you should have no issues. Happy solving! 🚀
    """)

st.write("Fill out your function, variables, and constraint(s) below:")

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
        original_f = sympify(f_input)

        # Adjust function based on optimization type
        f = original_f

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
            best_solution = None
            best_value = None

            for sol in solutions:
                f_val = original_f.subs(sol)

                if optimization_type == "Minimize":
                    if best_value is None or f_val < best_value:
                        best_value = f_val
                        best_solution = sol
                else:  # Maximize
                    if best_value is None or f_val > best_value:
                        best_value = f_val
                        best_solution = sol

            # Display best solution
            st.success(f"Best Solution ({optimization_type}):")
            for var in all_symbols:
                if var in best_solution:
                    st.write(f"**{var}** = {best_solution[var]}")
            st.write(f"**Objective function value** = {best_value}")
            st.markdown("---")

    except Exception as e:
        st.error(f"Error: {str(e)}")
