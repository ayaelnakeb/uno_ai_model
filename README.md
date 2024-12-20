# Foobar

A simulation of the classic UNO card game featuring AI agents powered by reinforcement learning techniques, including Q-Learning and Monte Carlo. The project includes an interactive GUI for configuring simulations and visualizing game progress, making it both educational and engaging.

## **Features**

### **AI Agents**
- **Q-Learning Agent:** Learns optimal strategies by iteratively updating Q-values based on the Bellman equation.
- **Monte Carlo Agent:** Enhances decision-making by evaluating sampled episodes to estimate state-action values.

### **Interactive GUI**
- Configure simulation parameters such as:
  - Number of iterations.
  - Reinforcement learning algorithm (Q-Learning or Monte Carlo).
- Visualize win-rate evolution dynamically during gameplay.

### **Tournament Mode**
- Simulate multiple games to assess and compare AI strategies.
- Analyze performance metrics such as win rates and game durations across iterations.

### **Logging**
- Game progress, decisions, and results are logged to `ai_decision_log.log` for analysis.
- Includes details of player actions, turns, and winners.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.
1. **Clone the Repository**

```bash
   git clone https://github.com/your-username/uno_ai_model.git
   cd uno_ai_model
```
2. **Set Up a Virtual Environment**
```bash
  python3 -m venv venv
  source venv/bin/activate    # On Windows, use `venv\Scripts\activate`
```
3. **Install Dependencies**
```bash
  pip install -r requirements.txt
```
4. **Run the Application Start the UNO Card Game Simulator GUI**
```bash
  python run.py
```

## How to Run the GUI

- After running python run.py, the GUI window for the UNO Card Game Simulator will appear.
**Configure Parameters**
Enter the number of iterations (default: 100).
Select the AI algorithm (either Q-Learning or Monte Carlo).

**Start Simulation**

- Click the "Start Simulation" button to begin the simulation.
- The simulation will run the specified number of games and dynamically update the win-rate evolution graph.

**Visualize Results**
- The graph embedded in the GUI shows the win-rate evolution for Player 1 over the iterations, with a baseline win rate of 50% for comparison.


**How to View Logs**

- Open the ai_decision_log.log file in any text editor or IDE to analyze the detailed game flow.



