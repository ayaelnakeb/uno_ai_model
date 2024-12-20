import logging
import time
from src.agents import QLearningAgent, MonteCarloAgent
from src.players import Player
from src.turn import Turn
from src.cards import Card, Deck
from src.utils import check_win, block_print, enable_print, bold
import config as conf

# Configure logging to log game decisions and outcomes
logging.basicConfig(
    filename='ai_decision_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Game(object):
    """
    Represents a single UNO game. The game progresses in iterations of turns until one player wins
    by having 0 cards in their hand. 

    Attributes:
        player_1 (Player): The first player in the game.
        player_2 (Player): The second player in the game.
        turn (Turn): Manages the current turn and game mechanics.
        turn_no (int): Tracks the number of turns taken.
        winner (str): The name of the winning player.
    """

    def __init__(self, player_1_name, player_2_name, starting_name, agent, algorithm, comment):
        """
        Initializes the Game object with two players, a turn object, and manages the game loop.

        Args:
            player_1_name (str): Name of player 1.
            player_2_name (str): Name of player 2.
            starting_name (str): The name of the player who starts the game.
            agent (object): The agent (QLearningAgent or MonteCarloAgent) used in the game.
            algorithm (str): The algorithm used by the agent ("q-learning" or "monte-carlo").
            comment (bool): Whether to enable or disable print outputs.
        """
        if not comment:
            block_print()

        # Initialize players and the turn object
        self.player_1 = Player(player_1_name, agent=agent)
        self.player_2 = Player(player_2_name, agent=agent)
        self.turn = Turn(
            deck=Deck(),
            player_1=self.player_1,
            player_2=self.player_2,
            agent=agent
        )

        self.turn_no = 0  # Tracks the turn number
        self.winner = 0  # Tracks the winner of the game

        # Log the start of the game
        logging.info("Starting a new game between %s and %s", player_1_name, player_2_name)

        # Game loop
        while self.winner == 0:
            self.turn_no += 1
            card_open = self.turn.card_open  # The current open card
            logging.info("Turn %d: Current open card: %s", self.turn_no, card_open.print_card())

            # Determine the active and passive players based on the turn number
            if starting_name == self.player_1.name:
                if self.turn_no % 2 == 1:
                    player_act, player_pas = self.player_1, self.player_2
                else:
                    player_act, player_pas = self.player_2, self.player_1
            else:
                if self.turn_no % 2 == 0:
                    player_act, player_pas = self.player_1, self.player_2
                else:
                    player_act, player_pas = self.player_2, self.player_1

            logging.info("Player %s's turn. Hand: %s", player_act.name, player_act.hand)

            # Execute the player's action
            self.turn.action(
                player=player_act,
                opponent=player_pas,
                agent=agent,
                algorithm=algorithm
            )

            logging.info("Player %s played: %s", player_act.name, player_act.card_play)

            # Check for a winner
            if check_win(player_act):
                self.winner = player_act.name
                logging.info("%s has won!", player_act.name)
                break

            if check_win(player_pas):
                self.winner = player_pas.name
                logging.info("%s has won!", player_pas.name)
                break

            # Handle special cards that affect turn flow
            if player_act.card_play.value in ["REV", "SKIP"]:
                logging.info("%s gets another turn due to card: %s", player_act.name, player_act.card_play.value)
                self.turn_no -= 1

            if self.turn.count > 0 and self.turn.count % 2 == 0:
                logging.info("%s gets another turn", player_act.name)
                self.turn_no -= 1

        # Update the agent's knowledge after the game ends
        self.player_1.identify_state(card_open)
        agent.update(self.player_1.state, self.player_1.action)

        if not comment:
            enable_print()


def tournament(iterations, algo, comment, agent_info):
    """
    Runs multiple games in a tournament and collects summary statistics.

    Args:
        iterations (int): The number of games to simulate.
        algo (str): The reinforcement learning algorithm to use ("q-learning" or "monte-carlo").
        comment (bool): Whether to enable or disable print outputs during games.
        agent_info (dict): Information for initializing the agent (e.g., epsilon, step size).

    Returns:
        tuple: Contains the list of winners, the number of turns in each game, 
               and the agent's final Q-table.
    """
    timer_start = time.time()  # Start the tournament timer

    # Initialize the agent based on the specified algorithm
    global agent, algorithm
    algorithm = algo

    if algo == "q-learning":
        agent = QLearningAgent(agent_info)
    else:
        agent = MonteCarloAgent(agent_info)

    # Lists to track game outcomes
    winners, turns, coverage = list(), list(), list()

    logging.info("Starting tournament with %d iterations and algorithm %s", iterations, algo)

    # Simulate the specified number of games
    for i in range(iterations):
        time.sleep(0.01)  # Slight delay to reduce processing speed

        # Alternate starting player
        if i % 2 == 1:
            starting_name = conf.player_name_2
        else:
            starting_name = conf.player_name_1

        # Run a single game
        game = Game(
            player_1_name=conf.player_name_1,
            player_2_name=conf.player_name_2,
            starting_name=starting_name,
            agent=agent,
            algorithm=algo,
            comment=comment
        )

        # Record game statistics
        winners.append(game.winner)
        turns.append(game.turn_no)
        coverage.append((agent.q != 0).values.sum())

        logging.info("Game %d completed. Winner: %s, Turns: %d", i + 1, game.winner, game.turn_no)

    # Calculate tournament duration
    timer_end = time.time()
    timer_dur = timer_end - timer_start
    logging.info(
        "Tournament completed in %.2f minutes (%.2f games per second)",
        timer_dur / 60,
        iterations / timer_dur
    )

    return winners, turns, agent
