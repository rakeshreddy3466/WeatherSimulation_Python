import numpy as np


class WeatherSimulation:

    def __init__(self, transition_probabilities, holding_times):
        self.current_value_state = 'sunny'
        # Initialize with the current state as 'sunny'
        self.tran_probs = transition_probabilities
        # Dictionary to store transition probabilities between weather states
        self.list_of_states = list(transition_probabilities)
        self.holdings = holding_times
        # Dictionary to store holding times for each weather state
        self.remaining_time = 0
        # Variable to store the remaining time in the current weather state

        # Validate that transition probabilities sum to 1 for each state
        for i, j in self.tran_probs.items():
            if not np.isclose(sum(j.values()), 1.0):
                raise RuntimeError(f"Incorrect transition probabilities detected for state '{i}': The total must equal 1.")

    def get_states(self):
        # Returns a list of all possible states in the weather simulation.
        return self.list_of_states

    def current_state(self):
        # Returns the current weather state for the simulation.
        return self.current_value_state

    def next_state(self):
        # Define a generator function named 'iterable()' that yields the current state
        # during each call, allowing the simulation to progress with each 'next()' call.
        if self.remaining_time <= 0:
            probabilities = self.tran_probs[self.current_value_state]
            self.current_value_state = np.random.choice(
                self.list_of_states, p=list(probabilities.values()))
            self.remaining_time = self.holdings[self.current_state()]
            self.remaining_time -= 1
        else:
            self.remaining_time -= 1

    def set_state(self, new_state):
        # Updates the current simulation state to the specified 'new_state'
        if new_state not in self.list_of_states:
            raise ValueError(f"Provided State was invalid state: {new_state}.")
        else:
            self.current_value_state = new_state
            self.remaining_time = self.holdings[new_state]

    def current_state_remaining_hours(self):
        # Calculates and returns the remaining hours in the current weather state
        return self.remaining_time

    def iterable(self):
        # Generates and yields the current state while progressing to the next state in the simulation using next().
        while True:
            yield self.current_value_state
            self.next_state()

    def simulate(self, hours):
        # Simulates for the specified duration and computes state occurrence percentages based on initial state order.
        state_counts = {}
        for hr in range(hours):
            self.next_state()
            if self.current_value_state in state_counts:
                state_counts[self.current_value_state] += 1
            else:
                state_counts[self.current_value_state] = 1

        state_percentages = [state_counts[state]*100 / hours for state in self.list_of_states]
        state_percentages = [round(i, 2) for i in state_percentages]
        return state_percentages