import random
from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *


class Kumoko:
  def __init__(self, ensemble, scoring, action_choice='best'):
    """
    Arguments:
      ensemble: implementation of EnsembleBase interface
      action_choice: either 'best', 'vote', or 'stochastic'
    """
    self.proposed_actions = []
    self.proposed_meta_actions = []
    self.our_last_move = None
    self.holistic_history = HolisticHistoryHolder()
    self.strategies = ensemble.generate()
    self.scoring_funcs = scoring.generate_normal()
    self.action_choice = action_choice

    # Assert that all strats are unique objects
    strat_ids = set()
    for strategy in self.strategies:
      strat_ids.add(id(strategy))
    assert len(strat_ids) == len(self.strategies)

    # Add initial scores for each strategy in the list
    self.scores = 3. * np.ones(
        shape=(len(self.scoring_funcs),
               3 * len(self.strategies)))
    self.proposed_actions = [
      random.choice('RPS')] * self.scores.shape[1]

    # Add meta-scores for each of the scoring function
    self.meta_scoring_func = scoring.get_meta_scoring()

    self.meta_scores = 3. * np.ones(
        shape=(len(self.scoring_funcs)))
    self.proposed_meta_actions = [
        random.choice('RPS')] * self.meta_scores.shape[0]

  def next_action(self, our_last_move, his_last_move):
    """Generate next move based on opponent's last move"""

    # Force last move, so that we can use Kumoko as part of
    # a larger meta-agent
    self.our_last_move = our_last_move

    # Update game history with the moves from previous
    # game step
    if his_last_move is not None:
      if DEBUG_MODE:
        assert self.our_last_move is not None
      self.holistic_history.add_moves(
          self.our_last_move, his_last_move)

    # Update score for the previous game step
    if his_last_move is not None and \
        len(self.proposed_actions) > 0:

      if DEBUG_MODE:
        assert len(self.proposed_actions) == \
          3 * len(self.strategies)
        assert len(self.proposed_meta_actions) == \
          len(self.meta_scores)
        assert self.scores.shape[0] == \
          len(self.scoring_funcs)

      # Meta-strategy selection score
      for sf in range(len(self.scoring_funcs)):
        for pa in range(len(self.proposed_actions)):
          self.scores[sf, pa] = self.scoring_funcs[sf](
              self.scores[sf, pa],
              self.proposed_actions[pa],
              his_last_move)

      # Selector selection score
      for sf in range(len(self.scoring_funcs)):
        self.meta_scores[sf] = self.meta_scoring_func(
            self.meta_scores[sf],
            self.proposed_meta_actions[sf],
            his_last_move)

    # Generate next move for each strategy
    if len(self.proposed_actions) == 0:
      self.proposed_actions = \
          [random.choice('RPS')] * (len(self.strategies) * 3)
    else:
      for st in range(len(self.strategies)):
        proposed_action = \
          self.strategies[st](self.holistic_history)
        if proposed_action is not None:
          self.proposed_actions[st] = proposed_action
          self.proposed_actions[st + len(self.strategies)] = \
            BEAT[self.proposed_actions[st]]
          self.proposed_actions[st + 2 * len(self.strategies)] = \
            CEDE[self.proposed_actions[st]]

    # For each scoring function (selector), choose the
    # action based on all of our policy actors

    if self.action_choice == 'best':
      # Simply choose the action with best score
      best_actions_idx = np.argmax(self.scores, axis=1)
      if DEBUG_MODE:
        assert best_actions_idx.shape == \
          (len(self.scoring_funcs), )

      self.proposed_meta_actions = [
          self.proposed_actions[idx]
          for idx in best_actions_idx]

    elif self.action_choice == 'vote':
      # Vote by summing the score for each action
      action_cum_scores = np.zeros(
          shape=(len(self.scoring_funcs), 3))

      for sf in range(len(self.scoring_funcs)):
        for pa, action in enumerate(self.proposed_actions):
          action_cum_scores[sf, MOVE_TO_NUM[action]] += \
              self.scores[sf, pa]

      self.proposed_meta_actions = [
          NUM_TO_MOVE[voted_a]
          for voted_a in np.argmax(action_cum_scores, axis=1)]

    else:
      # Not implemented
      raise NotImplementedError(
        f'Action choice {self.action_choice} is not implemented.')

    # Meta-Selector: selecting the scoring function
    if DEBUG_MODE:
      assert len(self.meta_scores) == \
        len(self.proposed_meta_actions)

    best_meta_action_idx = np.argmax(self.meta_scores)
    self.our_last_move = \
      self.proposed_meta_actions[best_meta_action_idx]

    return self.our_last_move
