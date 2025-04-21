# Lagrange Multipliers Solver

This app uses the method of Lagrange multipliers to solve optimization problems with one or two constraints.

Built with [Streamlit](https://streamlit.io/) and [SymPy](https://www.sympy.org/).

---

## Features

- Supports 2 or 3 variables (e.g., `x, y` or `x, y, z`)
- Supports 1 or 2 constraints (e.g., `x + y = 1`)
- Solve for minima or maxima
- Outputs **exact symbolic solutions** (e.g., √2, fractions)
- Displays the value of the objective function at each solution
- Clean and simple interface

---

## How to Use

1. Enter your **objective function** (example: `x^2 + 4*y^2 - 2*x + 8*y`).
2. Enter your **variables**, separated by commas (example: `x, y`).
3. Enter one or two **constraints** (example: `x + 2*y = 7`).
4. Select whether you want to **minimize** or **maximize**.
5. Click **Solve**.
6. Solutions will display with default SymPy formatting.

✅ Multiplication must be explicit, e.g., `2*(x*y)`, not `2(xy)`.  
✅ Use `^` for exponents, e.g., `x^2` means x squared.

---

## Example

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

---

## Installation

```bash
pip install streamlit sympy
```

---

## Running the App

```bash
streamlit run app.py
```

---

## Requirements

- Python 3.8 or higher
- Streamlit
- SymPy

---

## Notes

- Solutions are symbolic by default (like √2, 3/2, etc.).
- No forced decimal approximations — solutions are clean and exact.

---

## License

This project is open-source and free to use under the MIT License.
