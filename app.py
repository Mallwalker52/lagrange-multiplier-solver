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
- If no second constraint, leave blank
- All solutions will be given as **decimal approximations**.
    """)

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

        lambdas = symbols([f"lam{i+1}" for i in range(len(constraints))])
        L = f
        for lam, constraint in zip(lambdas, constraints):
            L -= lam * (constraint.lhs - constraint.rhs)
        L = L.evalf()

        system = []
        for v in variables:
            system.append(diff(L, v).evalf())
        for constraint in constraints:
            system.append((constraint.lhs - constraint.rhs).evalf())

        all_symbols = list(variables) + list(lambdas)
        guess = [1.0] * len(all_symbols)
        sol = nsolve(system, all_symbols, guess)

        sol_dict = dict(zip(all_symbols, sol))

        meets_positivity = True
        for v in var_names:
            if positivity_requirements[v]:
                if sol_dict[symbols(v)] < 0:
                    meets_positivity = False
                    break

        if not meets_positivity:
            st.error("The solution does not satisfy the positivity constraints.")
        else:
            st.success(f"Solution ({optimization_type}):")

            point_vars = []
            point_vals = []
            lambdas_display = []

            for var in all_symbols:
                var_name = latex(var)
                value = latex(sol_dict[var].evalf(6))
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

            obj_value = f.evalf(subs=sol_dict, n=6)  # <--- this is the correct fix
            st.write("**Objective function value:**")
            st.latex(latex(obj_value))
            st.markdown("---")

    except Exception as e:
        st.error(f"Error: {str(e)}")
