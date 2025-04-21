# app.py

import streamlit as st
from sympy import symbols, diff, Eq, nsolve, sympify, latex

st.title("Lagrange Multipliers Solver")

with st.expander("📚 Instructions (Click to Expand)", expanded=False):
    st.markdown("""
**How to Enter Inputs:**
- Use explicit multiplication: `2*(x*y)`, not `2(xy)`
- Use `^` for powers (e.g., `x^2`)
- Fractional powers like `x^(0.4)` are allowed
- Constraints must use `=`
- Separate variables by commas (e.g., `x, y, z`)
- If no second constraint, leave it blank
- Solutions are given as **decimal approximations**.
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

if st.button("Solve"):
    try:
        # Preprocessing
        f_input = f_input.replace("^", "**")
        constraint1_input = constraint1_input.replace("^", "**")
        constraint2_input = constraint2_input.replace("^", "**")

        f = sympify(f_input).evalf()

        constraints = []
        if constraint1_input:
            if "=" in constraint1_input:
                left, right = constraint1_input.split("=")
                constraints.append(Eq(sympify(left).evalf(), sympify(right).evalf()))
            else:
                constraints.append(Eq(sympify(constraint1_input).evalf(), 0))
        if constraint2_input:
            if "=" in constraint2_input:
                left, right = constraint2_input.split("=")
                constraints.append(Eq(sympify(left).evalf(), sympify(right).evalf()))
            else:
                constraints.append(Eq(sympify(constraint2_input).evalf(), 0))

        # Lagrangian
        lambdas = symbols([f"lam{i+1}" for i in range(len(constraints))])
        L = f
        for lam, constraint in zip(lambdas, constraints):
            L -= lam * (constraint.lhs - constraint.rhs)
        L = L.evalf()

        # System of equations
        system = []
        for v in variables:
            system.append(diff(L, v).evalf())
        for constraint in constraints:
            system.append((constraint.lhs - constraint.rhs).evalf())

        all_symbols = list(variables) + list(lambdas)
        guess = [1.0] * len(all_symbols)
        sol = nsolve(system, all_symbols, guess)

        # Force all numeric now
        sol_dict = dict(zip(all_symbols, sol))
        float_sol_dict = {var: float(val.evalf()) for var, val in sol_dict.items()}

        # Positivity filtering
        meets_positivity = True
        for v in var_names:
            if positivity_requirements[v]:
                if float_sol_dict[symbols(v)] < 0:
                    meets_positivity = False
                    break

        if not meets_positivity:
            st.error("The solution does not satisfy the positivity constraints.")
        else:
            st.success(f"Solution ({optimization_type}):")

            # Display ordered pair/triple
            point_vars = []
            point_vals = []
            lambdas_display = []

            for var in all_symbols:
                var_name = latex(var)
                value_num = float(float_sol_dict[var])
                value_str = f"{value_num:.6f}"
                if var_name.startswith('lam'):
                    number = var_name[3:]
                    var_name = f"\\lambda_{{{number}}}"
                    lambdas_display.append(f"{var_name} = {value_str}")
                else:
                    point_vars.append(var_name)
                    point_vals.append(value_str)

            ordered_pair_latex = "(" + ", ".join(point_vars) + ") = (" + ", ".join(point_vals) + ")"
            st.latex(ordered_pair_latex)

            if lambdas_display:
                st.write("**Lagrange multipliers:**")
                st.latex(r" \\ ".join(lambdas_display))

            # Objective function value
            obj_value = f.subs(float_sol_dict)
            obj_value_num = float(obj_value)
            obj_value_str = f"{obj_value_num:.6f}"

            st.write("**Objective function value:**")
            st.latex(obj_value_str)
            st.markdown("---")

    except Exception as e:
        st.error(f"Error: {str(e)}")
