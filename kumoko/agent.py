import os
import random
import kaggle_environments

from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *

from kumoko.kumoko_meta import MetaKumoko
from kumoko.kumoko_v1 import KumokoV1
from kumoko.ensembles import ENSEMBLES


# Default values
ENSEMBLE = ENSEMBLES['rfind_v1']
USE_META = True
FU_THRESH = None
ACTION_CHOICE = 'vote'

# Read from OS environ
if 'KENSEMBLE' in os.environ:
  ENSEMBLE = ENSEMBLES[os.environ['KENSEMBLE']]
if 'KMETA' in os.environ:
  USE_META = (os.environ['KMETA'] == 'True')
if 'KFU' in os.environ:
  FU_THRESH = int(os.environ['KFU'])
if 'KACHOICE' in os.environ:
  ACTION_CHOICE = os.environ['KACHOICE']

global kumoko_agent
global latest_action
global current_score
latest_action = None
current_score = 0

if USE_META:
  kumoko_agent = MetaKumoko(
      KumokoV1,
      kumoko_args=[ENSEMBLE])
else:
  kumoko_agent = KumokoV1(
      ensemble=ENSEMBLE)


def agent(obs, conf):
  global kumoko_agent
  global latest_action
  global current_score
  # return random.randint(0,2)

  if obs.step == 0:
    s_move = kumoko_agent.next_action(None, None)
  else:
    s_his_last_move = NUM_TO_MOVE[obs.lastOpponentAction]
    s_our_last_move = NUM_TO_MOVE[latest_action]

    if s_his_last_move == BEAT[s_our_last_move]:
      current_score -= 1
    elif s_our_last_move == BEAT[s_his_last_move]:
      current_score += 1

    s_move = kumoko_agent.next_action(
        s_our_last_move, s_his_last_move)

  latest_action = MOVE_TO_NUM[s_move]

  # Surprise motherfucker
  if random.random() < 0.1 or random.randint(3, 40) > obs.step:
    latest_action = random.randint(0, 2)

  # Fuck you!!!
  if FU_THRESH is not None:
    if current_score < -FU_THRESH:
      latest_action = random.randint(0, 2)

  return latest_action


if __name__ == '__main__':
  env = kaggle_environments.make(
      "rps", configuration={"episodeSteps": 100}, debug=True)
  outcomes = env.run([agent, agent])
