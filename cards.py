import random


class Card(object):
    """
    Represents a card in the UNO game with properties for 'color' and 'value'.
    Provides methods to evaluate playability, display, and print card information.
    
    Attributes:
        color (str): The color of the card (e.g., RED, GRE, BLU, YEL, WILD).
        value (str or int): The value of the card (e.g., 0-9, SKI, REV, PL2, COL, PL4).
    """

    def __init__(self, c, v):
        """
        Initializes a card with the specified color and value.
        
        Args:
            c (str): The color of the card.
            v (str or int): The value of the card.
        """
        self.color = c
        self.value = v
        
    def __str__(self):
        """
        Returns a string representation of the card.
        
        Returns:
            str: The card as "color value".
        """
        return f"{self.color} {self.value}"

    def __repr__(self):
        """
        Returns the same string representation for debugging or printing.
        
        Returns:
            str: The card as "color value".
        """
        return self.__str__()
    
    def evaluate_card(self, open_c, open_v):
        """
        Evaluates if the card is playable based on the open card's color and value.
        
        Args:
            open_c (str): The color of the open card.
            open_v (str or int): The value of the open card.
        
        Returns:
            bool: True if the card is playable, otherwise False.
        """
        if (
            (self.color == open_c) or 
            (self.value == open_v) or 
            (self.value in ["COL", "PL4"])
        ):
            return True
    
    def show_card(self):
        """
        Prints the card's color and value to the console.
        """
        print(self.color, self.value)
    
    def print_card(self):
        """
        Returns a string combining the card's color and value.
        
        Returns:
            str: The card as "color value".
        """
        return str(self.color) + " " + str(self.value)


class Deck(object):
    """
    Represents the deck of cards in the UNO game. Handles deck operations such as building,
    shuffling, drawing, and discarding cards.
    
    Attributes:
        cards (list): The list of cards currently in the deck.
        cards_disc (list): The list of discarded cards.
    """

    def __init__(self):
        """
        Initializes the deck with a standard set of UNO cards and shuffles them.
        """
        self.cards = []  # Cards in the deck
        self.cards_disc = []  # Discarded cards
        self.build()
        self.shuffle()
    
    def build(self):
        """
        Builds the deck with the standard set of UNO cards.
        """
        colors = ["RED", "GRE", "BLU", "YEL"]

        # Create cards of various types
        cards_zero = [Card(c, 0) for c in colors]
        cards_normal = [Card(c, v) for c in colors for v in range(1, 10)] * 2
        cards_action = [Card(c, v) for c in colors for v in ["SKI", "REV", "PL2"]] * 2
        cards_wild = [Card("WILD", v) for v in ["COL", "PL4"]] * 4
        
        # Combine all cards into a single list
        cards_all = cards_normal + cards_action + cards_zero + cards_wild
        for card in cards_all:
            self.cards.append(card)
    
    def discard(self, card):
        """
        Moves a card to the discard pile.
        
        Args:
            card (Card): The card to discard.
        """
        self.cards_disc.append(card)
    
    def shuffle(self):
        """
        Shuffles the cards in the deck.
        """
        random.shuffle(self.cards)

    def draw_from_deck(self):
        """
        Draws a card from the deck. If the deck is empty, the discard pile is used to rebuild the deck.
        
        Returns:
            Card: The drawn card.
        """
        if len(self.cards) == 0:
            # Rebuild the deck from the discard pile
            self.cards = self.cards_disc
            self.cards_disc = []
            
        return self.cards.pop()
    
    def show_deck(self):
        """
        Displays all cards currently in the deck.
        """
        for c in self.cards:
            c.show_card()
    
    def show_discarded(self):
        """
        Displays all cards currently in the discard pile.
        """
        for c in self.cards_disc:
            c.show_card()
