import os
from argparse import ArgumentParser

import pandas as pd
import kaggle_environments
from datetime import datetime
import multiprocessing as pymp
from tqdm import tqdm


# function to return score
def get_result(match_settings):
    start = datetime.now()
    outcomes = kaggle_environments.evaluate(
        'rps',
        [match_settings[0], match_settings[1]],
        num_episodes=match_settings[2],
        configuration={
          'debug': True
        })
    won, lost, tie, avg_score = 0, 0, 0, 0.
    for outcome in outcomes:
        score = outcome[0]
        if score > 0: won += 1
        elif score < 0: lost += 1
        else: tie += 1
        avg_score += score
    elapsed = datetime.now() - start
    opponent_name = os.path.basename(match_settings[1])
    opponent_name = os.path.splitext(opponent_name)[0]
    print(f'{opponent_name:<30} --- {won:2d}/{tie:2d}/{lost:2d} --- {avg_score}')
    return match_settings[1], won, lost, tie, elapsed, float(avg_score) / float(match_settings[2])


def eval_agent_against_baselines(agent, baselines, num_episodes=10):
    print('')
    print(f'Evaluating {agent}:')
    print('-' * (30 + 5 + 8 + 5 + 7))
    print(f'{"opponent_name":<30} --- {"w":>2}/{"t":>2}/{"l":>2} --- {"avg"}')
    print('-' * (30 + 5 + 8 + 5 + 7))
    df = pd.DataFrame(
        columns=['wins', 'loses', 'ties', 'total time', 'avg. score'],
        index=baselines)

    matches = [[agent, baseline, num_episodes] for baseline in baselines]

    results = []
    if args.multiprocessing:
        pool = pymp.Pool()
        for content in pool.imap_unordered(get_result, matches):
            results.append(content)
    else:
        for match_cfg in matches:
            results.append(get_result(match_cfg))

    for baseline_agent, won, lost, tie, elapsed, avg_score in results:
        df.loc[baseline_agent, 'wins'] = won
        df.loc[baseline_agent, 'loses'] = lost
        df.loc[baseline_agent, 'ties'] = tie
        df.loc[baseline_agent, 'total time'] = elapsed
        df.loc[baseline_agent, 'avg. score'] = avg_score

    return df


if __name__ == '__main__':
  # Parse cmd line input
  parser = ArgumentParser()
  parser.add_argument('-m', '--multiprocessing', action='store_true')
  args = parser.parse_args()

  # Form list of enemies
  agents = [
      os.path.join('opponents', agent_file)
      for agent_file in os.listdir('opponents')
      if os.path.splitext(agent_file)[-1] == '.py']

  # Agent to eval
  agent_to_eval = os.path.join('kumoko', 'agent.py')
  df = eval_agent_against_baselines(agent_to_eval, agents)
