# app.py

import streamlit as st
from sympy import symbols, diff, Eq, solve, sympify

st.title("Lagrange Multipliers App")

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

