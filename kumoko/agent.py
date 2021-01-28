import os
import random
import kaggle_environments
from functools import partial

from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *

from kumoko.kumoko_meta import MetaKumoko
from kumoko.kumoko import Kumoko
from kumoko.ensembles import ENSEMBLES
from kumoko.scoring import SCORINGS
from kumoko.geometry_wrapper import GeometryWrapper


class KumokoAgent:
  def __init__(self,
               ensemble_cls=ENSEMBLES['rfind_v1'],
               scoring_cls=SCORINGS['std_dllu_v1'],
               use_meta=True,
               metameta_scoring='std_dllu_v1',
               fuck_you_thresh=None,
               action_choice='best',
               geometric=None,
               verbose=False):

    kumoko_cls = partial(Kumoko,
                         ensemble_cls=ensemble_cls,
                         scoring_cls=scoring_cls,
                         action_choice=action_choice)
    if use_meta:
      self.kumoko_agent = MetaKumoko(
          kumoko_cls,
          metameta_scoring_func=metameta_scoring)
    else:
      self.kumoko_agent = kumoko_cls()

    self.latest_action = None
    self.current_score = 0
    self.fuck_you_thresh = fuck_you_thresh
    self.geometric = geometric
    self.verbose = verbose

    if self.geometric:
      self.geowrapper = GeometryWrapper()

    if self.verbose:
      print('use_meta:', use_meta)
      print('metameta_scoring:', metameta_scoring)
      print('fu thresh:', fuck_you_thresh),
      print('action_choice:', action_choice)
      print('geometric:', geometric)

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
          s_our_last_move, s_his_last_move, self.verbose)

    self.latest_action = MOVE_TO_NUM[s_move]

    if self.geometric is None:
      # Surprise motherfucker
      if random.random() < 0.1 or random.randint(3, 40) > obs.step:
        self.latest_action = random.randint(0, 2)

      # Fuck you!!!
      if self.fuck_you_thresh is not None:
        if self.current_score < -self.fuck_you_thresh:
          self.latest_action = random.randint(0, 2)
    else:
      if obs.step > 0:
        self.latest_action = self.geowrapper(
            MOVE_TO_NUM[s_our_last_move],
            MOVE_TO_NUM[s_his_last_move],
            self.latest_action)

    return self.latest_action
