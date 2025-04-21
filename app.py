# app.py

import streamlit as st
from sympy import symbols, diff, Eq, solve, sympify

st.title("Lagrange Multipliers Solver")

# Fancy About Section
with st.expander("ℹ️ About this App"):
    st.markdown("""
This app uses the **method of Lagrange multipliers** to find minimum or maximum values of a function subject to one or two constraints.

Built with [Streamlit](https://streamlit.io/) and [SymPy](https://www.sympy.org/).
""")

    with st.expander("📋 How to Use"):
        st.markdown("""
1. Enter your **objective function** (example: `x^2 + 4*y^2 - 2*x + 8*y`).
2. Enter your **variables**, separated by commas (example: `x, y`).
3. Enter one or two **constraints** (example: `x + 2*y = 7`).
4. Select whether you want to **minimize** or **maximize**.
5. Click **Solve**.
6. Solutions will display using SymPy's default formatting.

✅ **Multiplication must be explicit:** use `2*(x*y)`, not `2(xy)`  
✅ **Use `^` for exponents:** `x^2` for x squared
""")

    with st.expander("💡 Example"):
        st.markdown("""
**Objective Function:**

```
x^2 + 4*y^2 - 2*x + 8*y
```

**Variables:**

```
x, y
```

**Constraint:**

```
x + 2*y = 7
```
""")

# Optional GitHub link (update the URL if you want)
st.markdown("[📄 View full project on GitHub](https://github.com/yourusername/yourrepository)")

# User Inputs
f_input = st.text_input("Objective Function", value="x^2 + y^2")
vars_input = st.text_input("Variables (comma-separated)", value="x, y")
constraint1_input = st.text_input("Constraint 1 (required)", value="x + y = 1")
constraint2_input = st.text_input("Constraint 2 (optional)", value="")

optimization_type = st.radio("Do you want to minimize or maximize?", ("Minimize", "Maximize"))

var_names = [v.strip() for v in vars_input.split(",") if v.strip()]
variables = symbols(var_names)

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
            st.success(f"Solution(s) ({optimization_type}):")

            for idx, sol in enumerate(solutions, 1):
                st.write(f"**Solution {idx}:**")
                for var in all_symbols:
                    if var in sol:
                        st.write(f"{var} = {sol[var]}")

                # Objective function value
                obj_value = f.subs(sol)
                st.write(f"Objective function value: {obj_value}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Error: {str(e)}")
