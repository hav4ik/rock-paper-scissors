from kumoko.kumoko_base import *
from abc import ABC, abstractmethod
from functools import partial
import numpy as np
import random


class BaseActionChoice:
  @abstractmethod
  def choose(self, proposed_actions, scores):
    return NotImplemented


class ActionChoiceSimple(BaseActionChoice):
  def __init__(self,
               top_k=1,
               only_positive=False,
               rnd=False,
               rnd_power=1.,
               holdout_trigger=None,
               holdout_patience=None):
    self.top_k = top_k
    self.rnd = rnd
    self.rnd_power = rnd_power
    self.only_positive = only_positive

    self.holdout_trigger = holdout_trigger
    self.holdout_counter = 0
    self.holdout_patience = holdout_patience
    self.holdout_scores = None
    assert (holdout_trigger is None and holdout_patience is None) or (
        holdout_trigger is not None and holdout_patience is not None)

  def choose(self, proposed_actions, scores, kumo_outcomes, last_chosen_meta_idx):
    """
    Arguments:
    - poposed_actions: a vector of actions
    - scores: a array [sf, pa] of scores
    """
    if self.holdout_trigger is not None:
      # trigger holdout mode if we had bad outcomes OR is already in one
      if self.holdout_counter == 0 \
          and len(kumo_outcomes) >= self.holdout_trigger \
          and np.sum(kumo_outcomes[-self.holdout_trigger:]) == -self.holdout_trigger:
        self.holdout_counter += 1
        if last_chosen_meta_idx is not None:
          scores[last_chosen_meta_idx] = self.holdout_scores[last_chosen_meta_idx]
      # If not in holdout mode, just save the last scores
      elif self.holdout_counter == 0:
        self.holdout_scores = scores.copy()
      # If we're over that period, stop
      elif self.holdout_counter == self.holdout_patience:
        self.holdout_counter = 0
        self.holdout_scores = scores
      else:
        self.holdout_counter += 1
        if last_chosen_meta_idx is not None:
          scores[last_chosen_meta_idx] = self.holdout_scores[last_chosen_meta_idx]

    action_cum_scores = np.zeros((scores.shape[0], 3,))
    for sf in range(scores.shape[0]):
      for pa in np.argsort(scores[sf])[::-1][:self.top_k]:
        if self.only_positive and scores[sf, pa] < 0.0:
          break
        action = proposed_actions[pa]
        action_cum_scores[sf, MOVE_TO_NUM[action]] += \
            scores[sf, pa]

      if action_cum_scores[sf].sum() < 1e-4:
        # If every strategy is not winning, do a random choice
        action_cum_scores[sf, ...] = 0.
        action_cum_scores[random.randint(0, 2)] = 1.

    if not self.rnd:
      # Deterministic choice
      proposed_meta_actions = [
          NUM_TO_MOVE[voted_a]
          for voted_a in np.argmax(action_cum_scores, axis=1)]
    else:
      # Use the scores as random distribution
      action_cum_scores[np.isnan(action_cum_scores)] = 0.
      def norm_or_rand(a, power=self.rnd_power):
        aaa = np.power(a, power)
        if aaa.sum() < 1e-5:
          aa = np.random.rand(*aaa.shape)
          assert aa.shape == aaa.shape
        else:
          return aaa / aaa.sum()
      proposed_meta_actions = [
          np.random.choice(['R', 'P', 'S'], p=norm_or_rand(cum_scores, 3))
          for cum_scores in action_cum_scores]

    holdout_action = None
    if self.holdout_counter > 0 and last_chosen_meta_idx is not None:
      # If we're in holdout mode, we need to play a move that loses to our strats
      holdout_action = CEDE[proposed_meta_actions[last_chosen_meta_idx]]
    return proposed_meta_actions, holdout_action


def action_choice_simple_factory(top_k,
                                 only_positive,
                                 rnd,
                                 rnd_power=None,
                                 holdout_trigger=None,
                                 holdout_patience=None):
  return partial(ActionChoiceSimple,
                 top_k=top_k,
                 only_positive=only_positive,
                 rnd=rnd,
                 rnd_power=rnd_power,
                 holdout_trigger=holdout_trigger,
                 holdout_patience=holdout_patience)


ACTION_CHOICES = {
    'best': action_choice_simple_factory(
        top_k=1,
        only_positive=True,
        rnd=False),

    'best_hld_v1': action_choice_simple_factory(
        top_k=1,
        only_positive=True,
        rnd=False,
        holdout_trigger=2,
        holdout_patience=3),

    'vote': action_choice_simple_factory(
        top_k=None,
        only_positive=True,
        rnd=False),

    'vote5': action_choice_simple_factory(
        top_k=5,
        only_positive=True,
        rnd=False),

    'vote5_hld_v1': action_choice_simple_factory(
        top_k=5,
        only_positive=True,
        rnd=False,
        holdout_trigger=2,
        holdout_patience=3),

    'vote5rnd': action_choice_simple_factory(
        top_k=5,
        only_positive=True,
        rnd=True,
        rnd_power=2.0),

    'vote10': action_choice_simple_factory(
        top_k=10,
        only_positive=True,
        rnd=False),

    'vote10rnd': action_choice_simple_factory(
        top_k=10,
        only_positive=True,
        rnd=True,
        rnd_power=2.0),
}
