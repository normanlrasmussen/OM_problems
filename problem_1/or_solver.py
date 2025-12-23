from ortools.sat.python import cp_model
from solvers import base_solver
import numpy as np

class or_solver(base_solver):
    def __init__(self, data, max_fuel, max_solver_time:int=60):
        super().__init__(data, max_fuel)
        self.max_solver_time = max_solver_time

    def solve(self):

        # Conver data to lists
        gas_costs = [int(row[1] * 1000) for row in self.data] # Scale gas by 1000 to avoid floating point errors
        distances = [int(row[0]) for row in self.data]

        # Create model
        model = cp_model.CpModel()

        # Create variables for gas fill up at each location
        gas_vars = []
        for i in range(len(self.data)):
            gas_vars.append(model.NewIntVar(0, self.max_fuel, f'gas_{i}'))

        # Set up the fuel vars
        fuel_vars = []
        for i in range(len(self.data)):
            fuel_vars.append(model.NewIntVar(0, self.max_fuel, f'fuel_{i}'))

            # Add the rule of what fuel is 
            if i == 0:
                model.Add(fuel_vars[i] == gas_vars[i])
            else:
                model.Add(fuel_vars[i] == fuel_vars[i - 1] + gas_vars[i] - distances[i - 1])

            # Make sure that the fuel is reachable to the next location
            model.Add(fuel_vars[i] >= distances[i])
        
        # Make sure that amount of gas is equal to the total distance
        model.Add(sum(gas_vars) == sum(distances))

        # Add the cost
        cost = model.NewIntVar(0, sum(distances) * max(gas_costs), 'cost')
        model.Add(cost == sum(gas_vars[i] * gas_costs[i] for i in range(len(self.data))))

        # Add the objective
        model.Minimize(cost)

        # Create solver and solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.max_solver_time
        status = solver.Solve(model)

        # Check if solution was found
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # Extract the policy (gas fill-up amounts at each location)
            self.best_policy = np.array([solver.Value(gas_vars[i]) for i in range(len(self.data))])
            
            # Extract the total cost
            self.best_cost = solver.Value(cost) / 1000 # Convert back to dollars
        else:
            raise ValueError("No solution found")

    def print_solution(self):
        # Print the optimal path
        print(f"Optimal cost: ${self.best_cost:.2f}")
        print("\nOptimal path:")
        
        for i in range(len(self.data)):
            if self.best_policy[i] > 0:
                print(f"Location {i}: Fill up {self.best_policy[i]:.0f} gallons")

    def return_best_cost(self):
        return self.best_cost

        




if __name__ == "__main__":
    data = np.array([
        [100, 3.2],
        [100, 3.5],
        [100, 3.7],
        [100, 3.4],
        [100, 3.6],
        [100, 3.3],
        [100, 3.8],
    ])
    MAX_FUEL = 200
    or_solver = or_solver(data, MAX_FUEL)
    or_solver.solve()
    or_solver.print_solution()