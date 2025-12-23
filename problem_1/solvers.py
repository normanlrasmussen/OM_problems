import numpy as np

class base_solver():
    def __init__(self, data, max_fuel):
        self.data = data
        self.max_fuel = max_fuel

    def solve(self):
        raise NotImplementedError("Subclasses must implement this method")

    def print_solution(self):
        raise NotImplementedError("Subclasses must implement this method")

    def return_best_cost(self):
        raise NotImplementedError("Subclasses must implement this method")

class city_to_city_solver(base_solver):
    def __init__(self, data, max_fuel):
        super().__init__(data, max_fuel)

    def solve(self):
        # Init
        best_cost = np.full(len(self.data) + 1, np.inf) # Best cost to get to the end
        best_policy = np.zeros_like(best_cost, dtype=int) # Best policy: next location to go to

        # Base Case, we want to end with 0 gas
        best_cost[-1] = 0

        for i in range(len(self.data) - 1, -1, -1):
            
            # For each location ahead (including the final destination), find the cost of filling up to get there
            for j in range(i + 1, len(self.data) + 1):
                
                # Calculate distance from location i to location j
                if j < len(self.data):
                    distance = np.sum(self.data[i:j, 0])
                else:
                    # j is the final destination, sum all remaining distances
                    distance = np.sum(self.data[i:, 0])
                
                # Check if it is within range of Max Fuel
                if distance > self.max_fuel:
                    continue

                # Calculate the cost of filling up exactly the amount needed to get to location j
                cost = self.data[i, 1] * distance

                # Update the best cost and policy
                if best_cost[i] > cost + best_cost[j]:
                    best_cost[i] = cost + best_cost[j]
                    best_policy[i] = j  # Store the next location to go to

        # Save the best cost and policy
        self.best_cost = best_cost
        self.best_policy = best_policy

    def print_solution(self):
        # Print the optimal path
        print(f"Optimal cost: ${self.best_cost[0]:.2f}")
        print("\nOptimal path:")

        i = 0
        while i < len(self.data):
            next_location = self.best_policy[i]
            if next_location < len(self.data):
                distance = np.sum(self.data[i:next_location, 0])
            else:
                distance = np.sum(self.data[i:, 0])
            print(f"Location {i}: Fill up {distance:.0f} gallons")
            i = next_location
    
    def return_best_cost(self):
        return self.best_cost[0]


class gas_to_gas_solver(base_solver):
    def __init__(self, data, max_fuel):
        super().__init__(data, max_fuel)

    def solve(self):
        # Init
        best_cost = np.full((len(self.data) + 1, self.max_fuel + 1), np.inf) # Best cost to get to the end, gas level
        best_policy = np.zeros_like(best_cost, dtype=int) # Best policy: next location to go to

        # Base Case, we want to end with 0 gas
        best_cost[-1, 0] = 0

        # Reverse iterate over each location
        for i in range(len(self.data) - 1, -1, -1):

            # Iterate over each possible gas level
            for g in range(self.max_fuel + 1):
                
                # Iterate over every possible amount of gas to fill up to find the best cost
                for g_use in range(self.max_fuel + 1):

                    # Check if filling up g_use gallons would exceed max capacity
                    if g + g_use > self.max_fuel:
                        continue

                    # Calculate resulting gas level after traveling
                    resulting_gas = int(g + g_use - self.data[i, 0])
                    
                    # Skip if resulting gas level is invalid
                    if resulting_gas < 0 or resulting_gas > self.max_fuel:
                        continue

                    # Get the cost of filling up g_use gallons and going to the next location
                    cost = self.data[i, 1] * g_use + best_cost[i + 1, resulting_gas]

                    # Update the best cost and policy
                    if best_cost[i, g] > cost:
                        best_cost[i, g] = cost
                        best_policy[i, g] = g_use
        
        # Save the best cost and policy
        self.best_cost = best_cost
        self.best_policy = best_policy

    def print_solution(self):
        # Print the optimal path
        print(f"Optimal cost: ${self.best_cost[0, 0]:.2f}")
        print("\nOptimal path:")

        current_gas = 0  # Start with 0 gas at location 0
        for i in range(len(self.data)):
            g_use = self.best_policy[i, current_gas]
            if g_use > 0:
                print(f"Location {i}: Fill up {g_use} gallons")
            
            # Update gas level: current gas + fill up - distance to next location
            current_gas = int(current_gas + g_use - self.data[i, 0])    

    def return_best_cost(self):
        return self.best_cost[0, 0]
