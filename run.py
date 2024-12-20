import os
import pandas as pd
import numpy as np
import logging
from src.game import tournament
import config as conf

def main() -> None:
    # Setup logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting the tournament...")

    # Check config
    required_keys = ['iterations', 'algorithm', 'logging', 'model']
    missing_keys = [key for key in required_keys if key not in conf.params]
    if missing_keys:
        raise KeyError(f"Missing keys in configuration: {', '.join(missing_keys)}")

    # Run tournament
    run = tournament(
        iterations=conf.params['iterations'],
        algo=conf.params['algorithm'],
        comment=conf.params['logging'],
        agent_info=conf.params['model']
    )

    logger.info("Tournament completed. Processing results...")

    # Process results
    result = pd.concat([
        pd.Series(run[0], name='winner'), 
        pd.Series(run[1], name='turns')
    ], axis=1)
    result["win_rate"] = np.where(result["winner"] == conf.player_name_1, 1, 0)
    result["win_rate"] = result["win_rate"].cumsum() / (result.index + 1)

    # Process Q-values
    q_vals = pd.DataFrame(run[2].q)
    q_vals.index.rename("id", inplace=True)

    # Ensure proper indexing using `.iloc`
    if not result.empty:
        result["win_rate"] = np.where(
            result["winner"].iloc[:] == conf.player_name_1, 1, 0
        )
        result["win_rate"] = result["win_rate"].cumsum() / (result.index + 1)
    
    os.makedirs("assets", exist_ok=True)

    result_path = conf.params.get('result_path', "assets/results.csv")
    q_vals_path = conf.params.get('q_vals_path', "assets/q-values.csv")

    if result.empty:
        logger.warning("Result DataFrame is empty. No data will be saved.")
    else:
        result.to_csv(result_path, index=False)
        logger.info(f"Results saved to {result_path}")

    if q_vals.empty:
        logger.warning("Q-values DataFrame is empty. No data will be saved.")
    else:
        q_vals.to_csv(q_vals_path, index=True)
        logger.info(f"Q-values saved to {q_vals_path}")

