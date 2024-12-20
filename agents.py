import pandas as pd
import numpy as np
import random

import src.state_action_reward as sar


class Agent(object):
    """
    A base agent class for reinforcement learning.
    
    Attributes:
        epsilon: Exploration rate for the epsilon-greedy policy.
        step_size: Learning rate for Q-value updates.
        states: All possible states in the environment.
        actions: All possible actions in the environment.
        R: Reward table for state-action pairs.
        q: Q-table initialized to zeros.
        visit: Tracks the number of times each state-action pair is visited.
    """

    def __init__(self, agent_info: dict):
        """
        Initializes the agent with provided parameters and creates an empty Q-table.
        
        Args:
            agent_info (dict): A dictionary containing 'epsilon' and 'step_size'.
        """
        self.epsilon = agent_info["epsilon"]
        self.step_size = agent_info["step_size"]
        self.states = sar.states()
        self.actions = sar.actions()
        self.R = sar.rewards(self.states, self.actions)

        # Initialize Q-table and visit count table
        self.q = pd.DataFrame(
            data=np.zeros((len(self.states), len(self.actions))),
            columns=self.actions,
            index=self.states
        )
        self.visit = self.q.copy()


class QLearningAgent(Agent):
    """
    An agent implementing the Q-Learning algorithm.
    """

    def __init__(self, agent_info: dict):
        """
        Initializes the Q-Learning agent.
        
        Args:
            agent_info (dict): A dictionary containing 'epsilon' and 'step_size'.
        """
        super().__init__(agent_info)
        self.prev_state = 0  # Tracks the previous state
        self.prev_action = 0  # Tracks the previous action

    def step(self, state_dict, actions_dict):
        """
        Chooses the next action based on the epsilon-greedy policy.
        
        Args:
            state_dict (dict): The current state as a dictionary.
            actions_dict (dict): The available actions and their feasibility.

        Returns:
            str: The chosen action.
        """
        # Transform state dictionary into a tuple representation
        state = tuple(state_dict.values())

        # Epsilon-greedy policy
        if random.random() < self.epsilon:
            # Exploration: Random action
            actions_possible = [key for key, val in actions_dict.items() if val != 0]
            action = random.choice(actions_possible)
        else:
            # Exploitation: Action with maximum Q-value
            actions_possible = [key for key, val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = -float('inf')
            for i in actions_possible:
                val = self.q.loc[[state], i].iloc[0]
                if val >= val_max:
                    val_max = val
                    action = i

        return action

    def update(self, state_dict, action):
        """
        Updates Q-values using the Bellman equation.
        
        Args:
            state_dict (dict): The current state as a dictionary.
            action (str): The action taken.
        """
        state = tuple(state_dict.values())

        # Update Q-values if not the first turn
        if self.prev_state != 0:
            prev_q = self.q.loc[self.prev_state, self.prev_action]
            this_q = self.q.loc[state, action]
            reward = self.R.loc[state, action]

            # Bellman equation for Q-value update
            if reward == 0:
                self.q.loc[self.prev_state, self.prev_action] = (
                    prev_q + self.step_size * (reward + this_q - prev_q)
                )
            else:
                self.q.loc[self.prev_state, self.prev_action] = (
                    prev_q + self.step_size * (reward - prev_q)
                )

            # Increment visit count
            self.visit.loc[self.prev_state, self.prev_action] += 1

        # Update previous state and action
        self.prev_state = state
        self.prev_action = action


class MonteCarloAgent(Agent):
    """
    An agent implementing the Monte Carlo method for reinforcement learning.
    """

    def __init__(self, agent_info: dict):
        """
        Initializes the Monte Carlo agent.
        
        Args:
            agent_info (dict): A dictionary containing 'epsilon' and 'step_size'.
        """
        super().__init__(agent_info)
        self.state_seen = []  # States visited in the current episode
        self.action_seen = []  # Actions taken in the current episode
        self.q_seen = []  # State-action pairs seen in the current episode

    def step(self, state_dict, actions_dict):
        """
        Chooses the next action based on the epsilon-greedy policy.
        
        Args:
            state_dict (dict): The current state as a dictionary.
            actions_dict (dict): The available actions and their feasibility.

        Returns:
            str: The chosen action.
        """
        # Transform state dictionary into a tuple representation
        state = tuple(state_dict.values())

        # Epsilon-greedy policy
        if random.random() < self.epsilon:
            # Exploration: Random action
            actions_possible = [key for key, val in actions_dict.items() if val != 0]
            action = random.choice(actions_possible)
        else:
            # Exploitation: Action with maximum Q-value
            actions_possible = [key for key, val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = -float('inf')
            for i in actions_possible:
                val = self.q.loc[state, i]
                if val >= val_max:
                    val_max = val
                    action = i

        # Track state-action pairs visited during the episode
        if (state, action) not in self.q_seen:
            self.state_seen.append(state)
            self.action_seen.append(action)

        self.q_seen.append((state, action))
        self.visit.loc[state, action] += 1

        return action

    def update(self, state_dict, action):
        """
        Updates Q-values for all state-action pairs seen in the episode.
        
        Args:
            state_dict (dict): The current state as a dictionary.
            action (str): The action taken.
        """
        state = tuple(state_dict.values())
        reward = self.R.loc[state, action]

        # Update Q-values for all visited state-action pairs
        for s, a in zip(self.state_seen, self.action_seen):
            self.q.loc[s, a] += self.step_size * (reward - self.q.loc[s, a])

        # Clear episode-specific tracking
        self.state_seen.clear()
        self.action_seen.clear()
        self.q_seen.clear()
