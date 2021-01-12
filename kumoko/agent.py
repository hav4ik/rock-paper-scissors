import os
import random
import kaggle_environments

from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *

from kumoko.kumoko_meta import MetaKumoko
from kumoko.kumoko_v1 import KumokoV1
from kumoko.ensembles import ENSEMBLES


# Default values
ENSEMBLE = ENSEMBLES['4_strats_v1']
USE_META = True

# Read from OS environ
if 'KENSEMBLE' in os.environ:
  ENSEMBLE = ENSEMBLES[os.environ['KENSEMBLE']]
if 'KMETA' in os.environ:
  USE_META = bool(os.environ['KMETA'])

global kumoko_agent
global latest_action
latest_action = None

if USE_META:
  kumoko_agent = MetaKumoko(
      KumokoV1,
      kumoko_args=[
        ENSEMBLE.strategies(),
        ENSEMBLE.scoring_funcs()
      ])
else:
  kumoko_agent = KumokoV1(
      ENSEMBLE.strategies(),
      ENSEMBLE.scoring_funcs())


def agent(obs, conf):
  global kumoko_agent
  global latest_action
  # return random.randint(0,2)

  if obs.step == 0:
    s_move = kumoko_agent.next_action(None, None)
  else:
    s_his_last_move = NUM_TO_MOVE[obs.lastOpponentAction]
    s_our_last_move = NUM_TO_MOVE[latest_action]
    s_move = kumoko_agent.next_action(
        s_our_last_move, s_his_last_move)

  latest_action = MOVE_TO_NUM[s_move]

  # Surprise motherfucker
  if random.random() < 0.1 or random.randint(3, 40) > obs.step:
    latest_action = random.randint(0, 2)
  return latest_action


if __name__ == '__main__':
  env = kaggle_environments.make(
      "rps", configuration={"episodeSteps": 100}, debug=True)
  outcomes = env.run([agent, agent])
