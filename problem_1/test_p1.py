from solvers import city_to_city_solver, gas_to_gas_solver
from or_solver import or_solver
import numpy as np

data = np.array([
    [100, 3.2],
    [100, 3.5],
    [100, 3.7],
    [100, 3.4],
    [100, 3.6],
    [100, 3.3],
    [100, 3.8],
])

# Parameters
MAX_FUEL = 200

# Solve the problem
city_solver = city_to_city_solver(data, MAX_FUEL)
city_solver.solve()
city_solver.print_solution()
# print(f"Optimal cost: ${city_solver.return_best_cost():.2f}")

print(" ")

gas_solver = gas_to_gas_solver(data, MAX_FUEL)
gas_solver.solve()
gas_solver.print_solution()
# print(f"Optimal cost: ${gas_solver.return_best_cost():.2f}")

print(" ")

or_solver = or_solver(data, MAX_FUEL)
or_solver.solve()
or_solver.print_solution()
# print(f"Optimal cost: ${or_solver.return_best_cost():.2f}")