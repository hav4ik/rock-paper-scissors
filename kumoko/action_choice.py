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
               rnd_power=1.):
    self.top_k = top_k
    self.rnd = rnd
    self.rnd_power = rnd_power
    self.only_positive = only_positive

  def choose(self, proposed_actions, scores):
    """
    Arguments:
    - poposed_actions: a vector of actions
    - scores: a array [sf, pa] of scores
    """
    action_cum_scores = np.zeros((scores.shape[0], 3,))
    for sf in range(scores.shape[0]):
      for pa in np.argsort(scores[sf][::-1][:self.top_k]):
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

    return proposed_meta_actions



def action_choice_simple_factory(top_k,
                                 only_positive,
                                 rnd,
                                 rnd_power=1.0):
  return partial(ActionChoiceSimple,
                 top_k=top_k,
                 only_positive=only_positive,
                 rnd=rnd,
                 rnd_power=rnd_power)


ACTION_CHOICES = {
    'best': action_choice_simple_factory(
        top_k=1,
        only_positive=True,
        rnd=False),

    'vote': action_choice_simple_factory(
        top_k=None,
        only_positive=True,
        rnd=False),

    'vote5': action_choice_simple_factory(
        top_k=5,
        only_positive=True,
        rnd=False),

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
