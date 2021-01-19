import os
import uuid
from argparse import ArgumentParser

import pandas as pd
import kaggle_environments
from datetime import datetime
import multiprocessing as pymp
from tqdm import tqdm
import random

from kumoko.agent import KumokoAgent
from kumoko.ensembles import ENSEMBLES
from kumoko.scoring import SCORINGS


# Generate a full Kumoko agent file, with uuid
def generate_kumoko_file(ensemble_cls,
                         scoring_cls,
                         use_meta,
                         metameta_scoring,
                         fu_thresh,
                         action_choice,
                         verbose=False,
                         name=None,
                         tmp_dir='/tmp/kumoko/'):
  if not os.path.isdir(tmp_dir):
    os.makedirs(tmp_dir)
  if name is None:
    name = uuid.uuid4().hex
  kumoko_tmp_path = os.path.join(tmp_dir, f'kumoko_{name}.py')
  code = f"""# This agent is generated
from kumoko.agent import KumokoAgent
from kumoko.ensembles import ENSEMBLES
from kumoko.scoring import SCORINGS

global kumoko_agent
kumoko_agent = KumokoAgent(
      ensemble_cls=ENSEMBLES['{ensemble_cls}'],
      scoring_cls=SCORINGS['{scoring_cls}'],
      use_meta={use_meta},
      metameta_scoring='{metameta_scoring}',
      fuck_you_thresh={fu_thresh},
      action_choice='{action_choice}',
      verbose=True)

def agent(obs, cfg):
  global kumoko_agent
  return kumoko_agent(obs, cfg)
"""
  with open(kumoko_tmp_path, 'w') as f:
    f.write(code)
  return kumoko_tmp_path


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
    avg_scopre = float(avg_score) / float(match_settings[2])
    print(f'{opponent_name:<30} --- {won:2d}/{tie:2d}/{lost:2d} --- {avg_score}')
    return match_settings[1], won, lost, tie, elapsed, avg_score


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
  parser.add_argument('dojo')
  parser.add_argument('-m', '--multiprocessing', action='store_true')

  kumoko_grp = parser.add_argument_group('kumoko args')
  kumoko_grp.add_argument('-e', '--ensemble', default='rfind_v1')
  kumoko_grp.add_argument('-s', '--scoring', default='std_dllu_v1')
  kumoko_grp.add_argument('-w', '--metameta_scoring', default='std_dllu_v1')
  kumoko_grp.add_argument('-u', '--use_meta', action='store_true')
  kumoko_grp.add_argument('-f', '--fu_thresh', type=int, default=None)
  kumoko_grp.add_argument('-c', '--action_choice', default='best')
  args = parser.parse_args()

  # Agent to eval
  if args.dojo == 'perf':
    agent_to_eval = generate_kumoko_file(
        ensemble_cls=args.ensemble,
        scoring_cls=args.scoring,
        use_meta=args.use_meta,
        metameta_scoring=args.metameta_scoring,
        fu_thresh=args.fu_thresh,
        action_choice=args.action_choice,
        verbose=True)
    trivial_opponent = lambda obs, cfg: random.randint(0, 2)
    env = kaggle_environments.make(
        "rps", configuration={"episodeSteps": 1000}, debug=True)
    outcomes = env.run([agent_to_eval, trivial_opponent])

  else:
    agent_to_eval = generate_kumoko_file(
        ensemble_cls=args.ensemble,
        scoring_cls=args.scoring,
        use_meta=args.use_meta,
        metameta_scoring=args.metameta_scoring,
        fu_thresh=args.fu_thresh,
        action_choice=args.action_choice)

    # Form list of enemies
    if args.dojo == 'test':
      env = kaggle_environments.make(
          "rps", configuration={"episodeSteps": 100}, debug=True)
      outcomes = env.run([agent_to_eval, agent_to_eval])

    elif args.dojo == 'all':
      agents = [
          os.path.join('opponents', agent_file)
          for agent_file in os.listdir('opponents')
          if os.path.splitext(agent_file)[-1] == '.py']
      df = eval_agent_against_baselines(agent_to_eval, agents)

    elif args.dojo == 'trivial':
      agents = [
          'opponents/pi.py',
          'opponents/konami_code.py',
      ]
      df = eval_agent_against_baselines(
          agent_to_eval, agents, num_episodes=3)

    elif args.dojo == 'tiny':
      agents = [
          'opponents/centrifugal_bumblepuppy_13.py',
          'opponents/centrifugal_bumblepuppy_16h.py',
          'opponents/dllu1.py',
          'opponents/iocaine_powder.py',
          'opponents/memory_patterns_v7.py',
          'opponents/rps_meta_fix.py',
          'opponents/testinonmo.py',
          'opponents/statistical_prediction.py',
          'opponents/geometry.py',
      ]
      df = eval_agent_against_baselines(agent_to_eval, agents)

    elif args.dojo == 'small':
      agents = [
          'opponents/centrifugal_bumblepuppy_1000.py',
          'opponents/centrifugal_bumblepuppy_13.py',
          'opponents/centrifugal_bumblepuppy_16h.py',
          'opponents/centrifugal_bumblepuppy_4.py',
          'opponents/centrifugal_bumblepuppy_5.py',
          'opponents/dllu1.py',
          'opponents/iocaine_powder.py',
          'opponents/memory_patterns_v7.py',
          'opponents/rps_meta_fix.py',
          'opponents/testinonmo.py',
          'opponents/statistical_prediction.py',
          'opponents/geometry.py',
      ]
      df = eval_agent_against_baselines(agent_to_eval, agents)

    elif args.dojo == 'kumo':
      cfgs = [
          {
            'name': '4_strats_v1a',
            'kwargs': {
              'ensemble_cls': '4_strats_v1a',
              'scoring_cls': 'std_dllu_v1',
              'metameta_scoring': 'std_dllu_v1',
              'use_meta': True,
              'fu_thresh': None,
              'action_choice': 'best',
            }
          },
          {
            'name': '4_strats_v2b',
            'kwargs': {
              'ensemble_cls': '4_strats_v2b',
              'scoring_cls': 'std_dllu_v1',
              'metameta_scoring': 'std_dllu_v1',
              'use_meta': True,
              'fu_thresh': None,
              'action_choice': 'best',
            }
          },
          {
            'name': '5_strats_v2b',
            'kwargs': {
              'ensemble_cls': '5_strats_v2b',
              'scoring_cls': 'std_dllu_v1',
              'metameta_scoring': 'std_dllu_v1',
              'use_meta': True,
              'fu_thresh': None,
              'action_choice': 'best',
            }
          },
      ]
      agents = [
          generate_kumoko_file(name=cfg['name'], **cfg['kwargs'])
          for cfg in cfgs]
      df = eval_agent_against_baselines(agent_to_eval, agents)

    elif args.dojo == 'cmp_score':
      cfgs = [
          {
            'name': 'std_dllu_v1',
            'kwargs': {
              'ensemble_cls': 'rfind_v1',
              'scoring_cls': 'std_dllu_v1',
              'metameta_scoring': 'std_dllu_v1',
              'use_meta': True,
              'fu_thresh': None,
              'action_choice': 'best',
            }
          },
          {
            'name': 'static_wnd_v1',
            'kwargs': {
              'ensemble_cls': 'rfind_v1',
              'scoring_cls': 'static_wnd_v1',
              'metameta_scoring': 'std_dllu_v1',
              'use_meta': True,
              'fu_thresh': None,
              'action_choice': 'best',
            }
          },
      ]
      agents = [
          generate_kumoko_file(name=cfg['name'], **cfg['kwargs'])
          for cfg in cfgs]
      df = eval_agent_against_baselines(agent_to_eval, agents)

    else:
      raise NotImplementedError(f'Wtf is {args.dojo}?')
