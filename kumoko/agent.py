import os
import random
import kaggle_environments

from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *

from kumoko.kumoko_meta import MetaKumoko
from kumoko.kumoko import Kumoko
from kumoko.ensembles import ENSEMBLES
from kumoko.scoring import SCORINGS


class KumokoAgent:
  def __init__(self,
               ensemble=ENSEMBLES['rfind_v1'],
               scoring=SCORINGS['std_dllu_v1'],
               use_meta=True,
               fuck_you_thresh=None,
               action_choice='best'):
    if use_meta:
      self.kumoko_agent = MetaKumoko(
          Kumoko,
          metameta_scoring_func=scoring.get_metameta_scoring(),
          kumoko_kwargs={
            'ensemble': ensemble,
            'scoring': scoring,
            'action_choice': action_choice,
          })
    else:
      self.kumoko_agent = Kumoko(
          ensemble=ensemble,
          scoring=scoring,
          action_choice=action_choice)

    self.latest_action = None
    self.current_score = 0
    self.fuck_you_thresh = fuck_you_thresh


  def __call__(self, obs, conf):
    if obs.step == 0:
      s_move = self.kumoko_agent.next_action(None, None)
    else:
      s_his_last_move = NUM_TO_MOVE[obs.lastOpponentAction]
      s_our_last_move = NUM_TO_MOVE[self.latest_action]

      if s_his_last_move == BEAT[s_our_last_move]:
        self.current_score -= 1
      elif s_our_last_move == BEAT[s_his_last_move]:
        self.current_score += 1

      s_move = self.kumoko_agent.next_action(
          s_our_last_move, s_his_last_move)

    self.latest_action = MOVE_TO_NUM[s_move]

    # Surprise motherfucker
    if random.random() < 0.1 or random.randint(3, 40) > obs.step:
      self.latest_action = random.randint(0, 2)

    # Fuck you!!!
    if self.fuck_you_thresh is not None:
      if self.current_score < -self.fuck_you_thresh:
        self.latest_action = random.randint(0, 2)

    return self.latest_action
