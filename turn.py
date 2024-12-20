from src.cards import Card
from src.utils import check_win


class Turn(object):
    """
    Manages the process of a single turn in the UNO game, which includes:
        - Initialization of hand cards and an open card before the first turn.
        - The active player's chosen action.
        - Counter actions by the opponent in case of special cards (PL2 or PL4).
    """

    def __init__(self, deck, player_1, player_2, agent):
        """
        Initializes the Turn object with a deck, two players, and an open card.

        Args:
            deck (Deck): The deck of cards used in the game.
            player_1 (Player): The first player in the game.
            player_2 (Player): The second player in the game.
            agent (object): The reinforcement learning agent (if applicable).
        """
        self.deck = deck
        self.player_1 = player_1
        self.player_2 = player_2
        self.card_open = self.deck.draw_from_deck()  # The initial open card
        self.start_up()  # Initialize hands and ensure a valid open card

    def start_up(self):
        """
        Sets up the initial state of the game:
            - Ensures the initial open card is a normal card (0-9).
            - Deals 7 cards to each player.
        """
        while self.card_open.value not in range(0, 10):
            print(f'Initial open card {self.card_open.print_card()} has to be normal')
            self.card_open = self.deck.draw_from_deck()
        
        print(f'Initial open card is {self.card_open.print_card()}\n') 
        
        # Each player draws 7 cards
        for i in range(7):
            self.player_1.draw(self.deck, self.card_open)
            self.player_2.draw(self.deck, self.card_open)
            
    def action(self, player, opponent, agent, algorithm):
        """
        Executes the active player's action during their turn.

        Args:
            player (Player): The active player.
            opponent (Player): The opponent player.
            agent (object): The reinforcement learning agent (if applicable).
            algorithm (str): The algorithm used by the agent ("q-learning" or "monte-carlo").
        """
        player_act = player
        player_pas = opponent
        player_act.evaluate_hand(self.card_open)  # Evaluate the active player's hand

        self.count = 0  # Counter for PL2 and PL4 chains
        
        # (1) Player has a playable card
        if len(player_act.hand_play) > 0:
            # Use RL agent for player 1, random actions for player 2
            if player_act == self.player_1:
                player_act.play_agent(self.deck, self.card_open, agent, algorithm)
            else:
                player_act.play_rand(self.deck)
                
            self.card_open = player_act.card_play  # Update the open card
            player_act.evaluate_hand(self.card_open)  # Reevaluate hand after playing

        # (2) Player must draw a card
        else:
            print(f'{player_act.name} has no playable card')
            player_act.draw(self.deck, self.card_open)
            
            # (2a) If the drawn card is playable
            if len(player_act.hand_play) > 0:
                if player_act == self.player_1:
                    player_act.play_agent(self.deck, self.card_open, agent, algorithm)
                else:
                    player_act.play_rand(self.deck)
                
                self.card_open = player_act.card_play  # Update the open card
                player_act.evaluate_hand(self.card_open)  # Reevaluate hand
            
            # (2b) If the drawn card is not playable, do nothing
            else:
                player_act.card_play = Card(0, 0)
        
        # Check for a winner
        if check_win(player_act):
            return
        if check_win(player_pas):
            return
        
        # Handle special cards (PL4 and PL2)
        if player_act.card_play.value == "PL4":
            self.action_plus(player=player_act, opponent=player_pas, penalty=4)
        
        if player_act.card_play.value == "PL2":
            self.action_plus(player=player_act, opponent=player_pas, penalty=2)
        
    def action_plus(self, player, opponent, penalty):
        """
        Handles the chain reaction when a PL2 or PL4 card is played.
        If the opponent has the same type of card, they can counter, continuing the chain.

        Args:
            player (Player): The player who played the PL2 or PL4 card.
            opponent (Player): The opponent who can counter with the same card.
            penalty (int): The penalty value (2 for PL2, 4 for PL4).
        """
        player_act = player
        player_pas = opponent
        hit, self.count = True, 1  # Track if a counter occurred and the chain count

        # Loop until no counter is played
        while hit:
            hit = False
            # Opponent counters
            for card in player_pas.hand:
                if card.value == "PL" + str(penalty):
                    player_pas.play_counter(self.deck, self.card_open, plus_card=card)
                    hit = True
                    self.count += 1
                    break
                    
            if check_win(player_pas):  # Check if opponent wins after countering
                return 

            # Active player counters
            if hit:
                hit = False
                for card in player_act.hand:
                    if card.value == "PL" + str(penalty):
                        player_act.play_counter(self.deck, self.card_open, plus_card=card)
                        hit = True
                        self.count += 1
                        break
                        
            if check_win(player_act):  # Check if active player wins after countering
                return
        
        # Apply penalty to the player who cannot counter
        if self.count % 2 == 0:
            print(f'\n{player_act.name} has to draw {self.count * penalty} cards')
            for i in range(self.count * penalty):
                player_act.draw(self.deck, self.card_open)
        else:
            print(f'\n{player_pas.name} has to draw {self.count * penalty} cards')
            for i in range(self.count * penalty):
                player_pas.draw(self.deck, self.card_open)
