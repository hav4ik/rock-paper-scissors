import random
from time import perf_counter
from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *


class Kumoko:
  def __init__(self,
               ensemble_cls,
               scoring_cls,
               action_choice='best'):
    """
    Arguments:
      ensemble: implementation of EnsembleBase interface
      action_choice: either 'best', 'vote', or 'stochastic'
    """
    self.proposed_actions = []
    self.proposed_meta_actions = []
    self.our_last_move = None
    self.holistic_history = HolisticHistoryHolder()
    self.strategies, self.do_rotations = ensemble_cls().generate()
    self.scoring = scoring_cls()
    self.action_choice = action_choice

    # Assert that all strats are unique objects
    strat_ids = set()
    for strategy in self.strategies:
      strat_ids.add(id(strategy.next_action))
    assert len(strat_ids) == len(self.strategies)

    # Count strategies with rotation
    self.n_strats_with_rots = 0
    for x in self.do_rotations:
      if x is True:
        self.n_strats_with_rots += 1
    self.n_all_strats = \
      len(self.strategies) + 2 * self.n_strats_with_rots
    self.scoring.set_num_strategies(self.n_all_strats)

    # Add initial actions for each strategy in the list
    self.scores = self.scoring.get_initial_scores()
    self.proposed_actions = [
      random.choice('RPS')] * self.scores.shape[1]

    # Get the names for each strategy
    self.strategy_names = [
        strategy.name for strategy in self.strategies]
    for st, do_rotation in enumerate(self.do_rotations):
      if do_rotation is True:
        self.strategy_names.append(
            self.strategies[st].name + '^1')
    for st, do_rotation in enumerate(self.do_rotations):
      if do_rotation is True:
        self.strategy_names.append(
            self.strategies[st].name + '^2')
    assert len(self.strategy_names) == len(self.proposed_actions)

    # Add initial meta-actions for each scoring
    self.meta_scores = self.scoring.get_initial_meta_scores()
    self.proposed_meta_actions = [
        random.choice('RPS')] * self.meta_scores.shape[0]

  def next_action(self,
                  our_last_move,
                  his_last_move,
                  verbose=False,
                  prefix=''):
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

    # If verbose, we output a YAML at each step for debugging
    if verbose:
      print(f'step: {len(self.holistic_history)}')

    # Update score for the previous game step
    if his_last_move is not None and \
        len(self.proposed_actions) > 0:

      assert len(self.proposed_actions) == \
        self.n_all_strats

      # Meta-strategy selection score
      self.scores[...] = self.scoring.compute_scores(
          self.proposed_actions, his_last_move)

      # Selector selection score
      self.meta_scores[...] = self.scoring.compute_meta_scores(
          self.proposed_meta_actions, his_last_move)

    # Generate next move for each strategy
    if len(self.proposed_actions) == 0:
      self.proposed_actions = \
          [random.choice('RPS')] * (len(self.strategies) * 3)
    else:
      strats_with_rots_counter = 0
      for st in range(len(self.strategies)):
        # Proposed actions for each strategy
        proposed_action = \
          self.strategies[st].next_action(self.holistic_history)

        if proposed_action is not None:
          # Rotation = 0
          self.proposed_actions[st] = proposed_action

          # Generate rotations
          if self.do_rotations[st]:
            # Rotation = 1
            self.proposed_actions[
                strats_with_rots_counter + \
                len(self.strategies)] = \
              BEAT[self.proposed_actions[st]]
            # Rotation = 2
            self.proposed_actions[
                strats_with_rots_counter + \
                self.n_strats_with_rots + \
                len(self.strategies)] = \
              CEDE[self.proposed_actions[st]]
            # Index shift counter
            strats_with_rots_counter += 1

    # For each scoring function (selector), choose the
    # action based on all of our policy actors
    if self.action_choice == 'best':
      # Simply choose the action with best score
      best_actions_idx = np.argmax(self.scores, axis=1)
      self.proposed_meta_actions = [
          self.proposed_actions[idx]
          for idx in best_actions_idx]

    elif self.action_choice == 'vote':
      # Vote by summing the score for each action
      action_cum_scores = np.zeros(
          shape=(self.scores.shape[0], 3))

      for sf in range(self.scores.shape[0]):
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

    if verbose:
      print(prefix + 'proposed:')
      score_names = self.scoring.get_score_names()
      for sf in np.argsort(self.meta_scores)[::-1]:
        print(f'  - {self.proposed_meta_actions[sf]} ' \
                  f'({self.meta_scores[sf]:.2f}) ' \
                  f'{score_names[sf]}:')
        best_args = np.argsort(self.scores[sf])[::-1][:7]
        for idx in best_args:
          print(f'    - {self.proposed_actions[idx]} ' \
                      f'({self.scores[sf, idx]:.2f}) ' \
                      f'{self.strategy_names[idx]}')

      print(prefix + f'chosen_scoring: {score_names[best_meta_action_idx]}')
      print(prefix + f'chosen_action: {self.our_last_move}')

    return self.our_last_move
