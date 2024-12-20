import sys
import os

def block_print():
    """
    Redirects the standard output to null, effectively blocking any print statements.
    This is useful for suppressing print outputs during simulations or testing.
    """
    sys.__stdout__ = sys.stdout  # Save the original standard output
    sys.stdout = open(os.devnull, "w")  # Redirect standard output to null
    
def enable_print(): 
    """
    Restores the standard output to its original state, enabling print statements again.
    """
    sys.stdout = sys.__stdout__  # Restore the original standard output

def bold(string):
    """
    Prints a given string in bold formatting.

    Args:
        string (str): The string to be printed in bold.
    """
    chr_start = "\033[1m"  # ANSI escape code for bold text
    chr_end = "\033[0m"    # ANSI escape code to reset text formatting
    print(chr_start + string + chr_end)
    
def underline(string):
    """
    Prints a given string with underline formatting.

    Args:
        string (str): The string to be printed with an underline.
    """
    chr_start = "\033[4m"  # ANSI escape code for underlined text
    chr_end = "\033[0m"    # ANSI escape code to reset text formatting
    print(chr_start + string + chr_end)

def check_win(player):
    """
    Checks if a player has won the game. A player wins if their hand contains no cards.

    Args:
        player (Player): The player object whose hand is being checked.

    Returns:
        bool: True if the player has won (no cards left in hand), otherwise False.
    """
    if len(player.hand) == 0:  # Check if the player's hand is empty
        return True
