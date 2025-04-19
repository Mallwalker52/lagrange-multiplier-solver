# app.py

import gradio as gr
from sympy import symbols, diff, solve, Eq, sympify

def lagrange_solver(f_input, vars_input, constraint1_input, constraint2_input):
    try:
        # Preprocess input: replace ^ with **
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

        # Create system of equations
        system = []
        for v in variables:
            system.append(Eq(diff(L, v), 0))
        for constraint in constraints:
            system.append(constraint)

        # Solve
        all_symbols = list(variables) + list(lambdas)
        solutions = solve(system, all_symbols, dict=True)

        if not solutions:
            return "No solutions found."

        result = ""
        for idx, sol in enumerate(solutions, 1):
            result += f"Solution {idx}:\n"
            for var in all_symbols:
                if var in sol:
                    result += f"  {var} = {sol[var]}\n"
            f_val = f.subs(sol)
            result += f"  Objective function value: {f_val}\n\n"
        
        return result

    except Exception as e:
        return f"Error: {str(e)}"

# Build the Gradio interface
demo = gr.Interface(
    fn=lagrange_solver,
    inputs=[
        gr.Textbox(label="Objective Function (f)"),
        gr.Textbox(label="Variables (comma-separated, e.g., x, y, z)"),
        gr.Textbox(label="Constraint 1 (e.g., x + y + z = 1)"),
        gr.Textbox(label="Constraint 2 (e.g., x - y = 0)")
    ],
    outputs="text",
    title="Lagrange Multipliers Solver",
    description="Enter your function and two constraints. Outputs critical points and objective function value."
)

demo.launch()
