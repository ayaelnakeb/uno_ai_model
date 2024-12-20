# Defining the state of the models: states, actions, and rewards
import pandas as pd
import numpy as np
import itertools

def states():
    """
    Generates all possible states for the UNO game. States are defined based on the count 
    of normal, special, and wild cards for each color and their combinations.

    Returns:
        list: A list of tuples representing all valid states in the game.
    """
    # Define the number of each type of card available
    norm_cards = {"RED": 2, "GRE": 2, "BLU": 2, "YEL": 2}  # Normal cards
    spec_cards = {"SKI": 1, "REV": 1, "PL2": 1}  # Special cards
    wild_cards = {"PL4": 1, "COL": 1}  # Wild cards

    # Define the number of playable cards
    norm_cards_play = {"RED#": 1, "GRE#": 1, "BLU#": 1, "YEL#": 1}
    spec_cards_play = {"SKI#": 1, "REV#": 1, "PL2#": 1}

    # Combine all card types into a single dictionary
    states_dict = {
        **norm_cards, 
        **spec_cards, 
        **wild_cards, 
        **norm_cards_play, 
        **spec_cards_play
    }

    # Initialize the states list with colors
    states = [["RED", "GRE", "BLU", "YEL"]]

    # Add possible counts for each card type
    for val in states_dict.values():
        aux = range(0, val + 1)  # Create a range from 0 to max count for each card type
        states.append(aux)

    # Generate all combinations of states
    states = list(itertools.product(*states))
    states_all = list()

    # Filter valid states based on constraints
    for i in range(len(states)):
        if (
            states[i][1] >= states[i][10] and  # RED >= RED#
            states[i][2] >= states[i][11] and  # GRE >= GRE#
            states[i][3] >= states[i][12] and  # BLU >= BLU#
            states[i][4] >= states[i][13] and  # YEL >= YEL#
            states[i][5] >= states[i][14] and  # SKI >= SKI#
            states[i][6] >= states[i][15] and  # REV >= REV#
            states[i][7] >= states[i][16]      # PL2 >= PL2#
        ): 
            states_all.append(states[i])  # Append only valid states

    return states_all


def actions():
    """
    Defines all possible actions in the UNO game.

    Returns:
        list: A list of strings representing the possible actions (card types).
    """
    actions_all = [
        "RED", "GRE", "BLU", "YEL", "SKI", 
        "REV", "PL2", "PL4", "COL"
    ]    
    return actions_all


def rewards(states, actions):
    """
    Generates a rewards table for all state-action pairs. A reward of 1 is given
    if the state indicates a winning condition (no remaining cards).

    Args:
        states (list): A list of all possible states.
        actions (list): A list of all possible actions.

    Returns:
        pd.DataFrame: A DataFrame representing the reward table with states as rows 
        and actions as columns.
    """
    # Initialize the reward matrix with zeros
    R = np.zeros((len(states), len(actions)))

    # Determine if each state is a winning state (sum of card counts is 0 or 1)
    states_t = [min(sum(states[i][1:10]), 1) for i in range(len(states))]

    for i in range(len(states)):
        if states_t[i] == 0:  # Check if the state represents a win
            R[i] = 1  # Assign a reward of 1 for all actions in a winning state

    # Convert the reward matrix to a DataFrame for better readability
    R = pd.DataFrame(
        data=R, 
        columns=actions, 
        index=states
    )

    return R
