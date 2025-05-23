# app.py

import streamlit as st
from sympy import symbols, diff, Eq, solve, sympify, latex

# Title
st.title("Lagrange Multipliers Solver")

# Instructions Section
with st.expander("📚 Instructions (Click to Expand)", expanded=False):
    st.markdown("""
**How to Enter Inputs:**
- Use explicit multiplication: `2*(x*y)`, not `2(xy)`
- Use `^` for powers (e.g., `x^2`)
- Fractional powers like `x^(0.4)` are allowed
- Constraints must use `=`
- Separate variables by commas (e.g., `x, y, z`)
- If no second constraint, leave it blank
- Outputs include **exact values** and **decimal approximations**.
    """)

# User Inputs
f_input = st.text_input("Objective Function (example: x^2 + y^2 + z^2)", value="x^2 + y^2 + z^2")
vars_input = st.text_input("Variables (comma-separated)", value="x, y, z")
constraint1_input = st.text_input("Constraint 1 (required)", value="x + y + z = 1")
constraint2_input = st.text_input("Constraint 2 (optional)", value="")

optimization_type = st.radio("Do you want to minimize or maximize?", ("Minimize", "Maximize"))

var_names = [v.strip() for v in vars_input.split(",") if v.strip()]
variables = symbols(var_names)

st.write("**Optional: Require variables to be positive (≥ 0)**")
positivity_requirements = {}
for v in var_names:
    positivity_requirements[v] = st.checkbox(f"Require {v} ≥ 0", value=False)

# Solve button
if st.button("Solve"):
    try:
        # Preprocessing
        f_input = f_input.replace("^", "**")
        constraint1_input = constraint1_input.replace("^", "**")
        constraint2_input = constraint2_input.replace("^", "**")

        f = sympify(f_input)

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

        # Lagrangian
        lambdas = symbols([f"lam{i+1}" for i in range(len(constraints))])
        L = f
        for lam, constraint in zip(lambdas, constraints):
            L -= lam * (constraint.lhs - constraint.rhs)

        # System of equations
        system = []
        for v in variables:
            system.append(diff(L, v))
        for constraint in constraints:
            system.append(constraint.lhs - constraint.rhs)

        all_symbols = list(variables) + list(lambdas)
        solutions = solve(system, all_symbols, dict=True)

        if not solutions:
            st.error("No solutions found.")
        else:
            # Filter positivity first
            filtered_solutions = []
            for sol in solutions:
                meets_positivity = True
                for v in var_names:
                    if positivity_requirements[v]:
                        if sol[symbols(v)].evalf() < 0:
                            meets_positivity = False
                            break
                if meets_positivity:
                    filtered_solutions.append(sol)

            if not filtered_solutions:
                st.error("No solutions satisfy the positivity constraints.")
            else:
                # Evaluate objective function at each solution
                scored_solutions = []
                for sol in filtered_solutions:
                    obj_value = f.subs(sol).evalf()
                    scored_solutions.append((obj_value, sol))

                # Pick best based on Minimize or Maximize
                if optimization_type == "Minimize":
                    best_solution = min(scored_solutions, key=lambda x: x[0])
                else:
                    best_solution = max(scored_solutions, key=lambda x: x[0])

                best_value, best_sol = best_solution

                st.success(f"Best Solution ({optimization_type}):")

                # Exact and Decimal Display
                exact_display = []
                decimal_display = []

                for var in all_symbols:
                    if var in best_sol:
                        var_name = latex(var)
                        var_value = best_sol[var]
                        var_value_decimal = var_value.evalf(6)

                        if var_name.startswith('lam'):
                            number = var_name[3:]
                            var_name = f"\\lambda_{{{number}}}"
                        exact_display.append(f"{var_name} = {latex(var_value)}")
                        decimal_display.append(f"{var_name} ≈ {var_value_decimal}")

                st.write("**Exact Values:**")
                st.latex(r" \\ ".join(exact_display))

                st.write("**Decimal Approximations:**")
                st.latex(r" \\ ".join(decimal_display))

                # Objective function value
                obj_value_exact = f.subs(best_sol)
                obj_value_decimal = obj_value_exact.evalf(6)

                st.write("**Objective function value:**")
                st.latex(f"\\text{{Exact: }} {latex(obj_value_exact)}")
                st.latex(f"\\text{{Approx: }} {obj_value_decimal}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Error: {str(e)}")
