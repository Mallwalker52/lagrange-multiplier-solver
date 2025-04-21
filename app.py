# app.py

import streamlit as st
from sympy import symbols, diff, solve, Eq, sympify, latex

st.title("Lagrange Multipliers Solver")

# Instructions Section
with st.expander("📚 Instructions (Click to Expand)", expanded=False):
    st.markdown("""
**How to Enter Inputs:**
- **Multiplication** must be explicit: write `2*(x*y)` instead of `2(x*y)` or `2xy`
- **Exponents:** use `^` for powers (e.g., `x^2` means x squared).  
  - Decimal exponents like `x^(0.4)` are supported automatically.
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

# Parse variables early so we can add positivity checkboxes
var_names = [v.strip() for v in vars_input.split(",") if v.strip()]
variables = symbols(var_names)

# Add positivity checkboxes dynamically
st.write("**Optional: Require variables to be positive (≥ 0)**")
positivity_requirements = {}
for v in var_names:
    positivity_requirements[v] = st.checkbox(f"Require {v} ≥ 0", value=False)

if st.button("Solve"):
    try:
        # Preprocess input
        f_input = f_input.replace("^", "**")
        constraint1_input = constraint1_input.replace("^", "**")
        constraint2_input = constraint2_input.replace("^", "**")

        # Parse function
        original_f = sympify(f_input, rational=True)  # rationalize floats

        # Adjust function based on optimization type
        f = original_f

        # Parse constraints
        constraints = []
        if constraint1_input:
            if "=" in constraint1_input:
                left, right = constraint1_input.split("=")
                constraints.append(Eq(sympify(left, rational=True), sympify(right, rational=True)))
            else:
                constraints.append(Eq(sympify(constraint1_input, rational=True), 0))
        if constraint2_input:
            if "=" in constraint2_input:
                left, right = constraint2_input.split("=")
                constraints.append(Eq(sympify(left, rational=True), sympify(right, rational=True)))
            else:
                constraints.append(Eq(sympify(constraint2_input, rational=True), 0))

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
            # Apply positivity filtering
            filtered_solutions = []
            for sol in solutions:
                meets_positivity = True
                for v in var_names:
                    if positivity_requirements[v]:
                        if sol[symbols(v)] < 0:
                            meets_positivity = False
                            break
                if meets_positivity:
                    filtered_solutions.append(sol)

            if not filtered_solutions:
                st.error("No solutions satisfy the positivity constraints.")
            else:
                best_solutions = []
                best_value = None

                for sol in filtered_solutions:
                    f_val = original_f.subs(sol)

                    if optimization_type == "Minimize":
                        if best_value is None or f_val < best_value:
                            best_value = f_val
                            best_solutions = [sol]
                        elif f_val == best_value:
                            best_solutions.append(sol)
                    else:  # Maximize
                        if best_value is None or f_val > best_value:
                            best_value = f_val
                            best_solutions = [sol]
                        elif f_val == best_value:
                            best_solutions.append(sol)

                # Display all best solutions
                st.success(f"Best Solution(s) ({optimization_type}):")
                for idx, sol in enumerate(best_solutions, 1):
                    st.write(f"**Solution {idx}:**")

                    point_vars = []
                    point_vals = []
                    lambdas_display = []

                    for var in all_symbols:
                        if var in sol:
                            var_name = latex(var)
                            value = latex(sol[var])
                            if var_name.startswith('lam'):
                                number = var_name[3:]
                                var_name = f"\\lambda_{{{number}}}"
                                lambdas_display.append(f"{var_name} = {value}")
                            else:
                                point_vars.append(var_name)
                                point_vals.append(value)

                    ordered_pair_latex = "(" + ", ".join(point_vars) + ") = (" + ", ".join(point_vals) + ")"
                    st.latex(ordered_pair_latex)

                    if lambdas_display:
                        st.write("**Lagrange multipliers:**")
                        st.latex(r" \\ ".join(lambdas_display))

                    st.write(f"**Objective function value:**")
                    st.latex(latex(best_value))
                    st.markdown("---")

    except Exception as e:
        st.error(f"Error: {str(e)}")
