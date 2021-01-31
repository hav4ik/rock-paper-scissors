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
from kumoko.action_choice import ACTION_CHOICES
from kumoko.strategies.geobot_beater import GeobotBeater


class KumokoAgent:
  def __init__(self,
               ensemble_cls=ENSEMBLES['rfind_v1'],
               scoring_cls=SCORINGS['std_dllu_v1'],
               action_choice_cls=ACTION_CHOICES['best'],
               use_meta=True,
               metameta_scoring='std_dllu_v1',
               fuck_you_thresh=None,
               geometric=None,
               antigeo_thresh=20,
               verbose=False):

    kumoko_cls = partial(Kumoko,
                         ensemble_cls=ensemble_cls,
                         scoring_cls=scoring_cls,
                         action_choice_cls=action_choice_cls)
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

    self.antigeo_thresh = antigeo_thresh
    if self.antigeo_thresh is not None:
      # Monitor geobeater
      self.geobeater = GeobotBeater()
      self.geobeater_score = 0
      self.geobeater_last_move = None
      self.should_use_geobeater = False

    # Monitor kumoko
    self.kumo_score = 0
    self.kumo_last_move = None

    if self.verbose:
      print('use_meta:', use_meta)
      print('metameta_scoring:', metameta_scoring)
      print('fu thresh:', fuck_you_thresh),
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

    # Update geobot actions before making changes to self.latest_actions
    if self.antigeo_thresh is not None and obs.step > 0:
      # Calculate geobeater's score
      if self.geobeater_last_move is not None:
        s_geobeater_last_move = NUM_TO_MOVE[self.geobeater_last_move]
        if s_geobeater_last_move == BEAT[s_his_last_move]:
          self.geobeater_score += 1
        elif s_geobeater_last_move == CEDE[s_his_last_move]:
          self.geobeater_score -= 1
      # Get geobeater's last action
      self.geobeater_last_move = self.geobeater(
          obs.step, self.latest_action, obs.lastOpponentAction)

    # Update kumoko actions before making changes to kumo_last_move
    if obs.step > 0:
      if self.kumo_last_move == (obs.lastOpponentAction + 1) % 3:
        self.kumo_score += 1
      elif self.kumo_last_move == (obs.lastOpponentAction + 2) % 3:
        self.kumo_score += -1

    # Update the self.latest_action
    self.kumo_last_move = MOVE_TO_NUM[s_move]
    self.latest_action = self.kumo_last_move

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
            self.latest_action,
            self.geometric)

    # # Maybe we should do it here?
    # self.kumo_last_move = self.latest_action

    # Try to understand if we can use anti-geometric strat (it's very subtle)
    if self.antigeo_thresh is not None and obs.step > 0:
      # If it's already winning, it is clearly up to something
      # if (self.geobeater_score >= self.antigeo_thresh and \
      #     self.current_score < self.geobeater_score) or \
      #     self.current_score <= -self.antigeo_thresh:
      if self.kumo_score < self.geobeater_score and self.geobeater_score > self.antigeo_thresh:
        # Unleash the geobeater
        self.latest_action = self.geobeater_last_move

    return self.latest_action
