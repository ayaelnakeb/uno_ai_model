import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from src.game import tournament
import config as conf


class UNOGUISimulator(tk.Tk):
    """
    A GUI-based simulator for the UNO card game using reinforcement learning.
    Allows users to configure simulation settings and visualize win rate evolution.
    """
    
    def __init__(self):
        """
        Initializes the GUI application, sets up the main window, 
        and creates configuration and visualization panels.
        """
        super().__init__()
        self.title("UNO Card Game Simulator")  # Set window title
        self.geometry("800x600")  # Set window dimensions
        
        # Create panels for simulation configuration and visualization
        self.create_config_panel()
        self.create_visualization_panel()
        
    def create_config_panel(self):
        """
        Creates a configuration panel for setting simulation parameters 
        (e.g., number of iterations, algorithm type).
        """
        # Frame for simulation settings
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(side=tk.TOP, fill=tk.X)
        
        # Input field for number of iterations
        tk.Label(frame, text="Iterations:").grid(row=0, column=0, sticky="w")
        self.iterations = tk.Entry(frame)
        self.iterations.insert(0, "100")  # Default value for iterations
        self.iterations.grid(row=0, column=1, padx=5)
        
        # Dropdown for selecting algorithm type
        tk.Label(frame, text="Algorithm:").grid(row=1, column=0, sticky="w")
        self.algorithm = ttk.Combobox(frame, values=["Q-Learning", "Monte Carlo"])
        self.algorithm.set("Q-Learning")  # Default value for algorithm
        self.algorithm.grid(row=1, column=1, padx=5)
        
        # Button to start the simulation
        start_button = tk.Button(frame, text="Start Simulation", command=self.run_simulation)
        start_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    def create_visualization_panel(self):
        """
        Creates a visualization panel to display the win rate evolution 
        using a matplotlib plot embedded in the Tkinter interface.
        """
        # Frame for the plot
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # Create a matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_title("Win Rate Evolution")
        self.ax.set_xlabel("Game Number")
        self.ax.set_ylabel("Win Rate")
        
        # Embed the matplotlib figure into the Tkinter GUI
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def run_simulation(self):
        """
        Executes the simulation based on user inputs, processes results, 
        and updates the visualization panel.
        """
        # Get user inputs for iterations and algorithm
        iterations = int(self.iterations.get())
        algorithm = self.algorithm.get()
        
        # Log the start of the simulation
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info("Starting simulation...")
        
        # Run the tournament simulation
        run = tournament(
            iterations=iterations,
            algo=algorithm,
            comment=False,
            agent_info=conf.params['model']
        )
        
        # Combine results into a DataFrame
        result = pd.concat([
            pd.Series(run[0], name='winner'),  # Winner of each game
            pd.Series(run[1], name='turns')   # Number of turns in each game
        ], axis=1)

        # Map winners to numerical flags (1 for Player 1, 0 for Player 2)
        result["win_flag"] = result["winner"].apply(lambda x: 1 if x == conf.player_name_1 else 0)

        # Calculate cumulative win rate
        result["win_rate"] = result["win_flag"].cumsum() / (result.index + 1)

        # Update the plot with the results
        self.update_plot(result)
    
    def update_plot(self, result):
        """
        Updates the matplotlib plot with new simulation results.

        Args:
            result (pd.DataFrame): DataFrame containing simulation results, 
                                   including win rates and game numbers.
        """
        # Clear the previous plot
        self.ax.clear()
        
        # Plot the win rate evolution
        self.ax.plot(result.index, result["win_rate"], label="Win Rate")
        self.ax.axhline(0.5, color="gray", linestyle="--", label="Baseline (50%)")
        self.ax.set_title("Win Rate Evolution")
        self.ax.set_xlabel("Game Number")
        self.ax.set_ylabel("Win Rate")
        self.ax.legend()
        
        # Redraw the canvas with the updated plot
        self.canvas.draw()


# Run the GUI Application
if __name__ == "__main__":
    app = UNOGUISimulator()
    app.mainloop()
