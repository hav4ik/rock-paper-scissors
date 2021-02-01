import random
from time import perf_counter
from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *


class Kumoko:
  def __init__(self,
               ensemble_cls,
               scoring_cls,
               action_choice_cls):
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
    self.action_choice = action_choice_cls()

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

    # Outcomes after each round
    self.outcomes = np.zeros((1000, self.n_all_strats))
    self.outcome_count = 0
    self.kumo_outcomes = []
    self.last_chosen_meta_idx = None

  def next_action(self,
                  our_last_move,
                  his_last_move,
                  verbose=False,
                  prefix='',
                  gotcha=None):
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

    # ------------------------------------------------------------
    # UPDATE SCORES AND METRICS
    # ------------------------------------------------------------

    # Update score and other metrics for the previous game step
    if his_last_move is not None and \
        len(self.proposed_actions) > 0:
      assert len(self.proposed_actions) == self.n_all_strats

      # Save outcomes in the memory and increase step counter
      for pa, proposed_move in enumerate(self.proposed_actions):
        if proposed_move == BEAT[his_last_move]:
          self.outcomes[self.outcome_count, pa] = 1
        elif proposed_move == CEDE[his_last_move]:
          self.outcomes[self.outcome_count, pa] = -1
        else:
          self.outcomes[self.outcome_count, pa] = 0
      self.outcome_count += 1

      if self.our_last_move == BEAT[his_last_move]:
        self.kumo_outcomes.append(1)
      elif self.our_last_move == CEDE[his_last_move]:
        self.kumo_outcomes.append(-1)
      else:
        self.kumo_outcomes.append(0)

      # Meta-strategy selection score
      self.scores[...] = self.scoring.compute_scores(
          self.proposed_actions, his_last_move)

      # Selector selection score
      self.meta_scores[...] = self.scoring.compute_meta_scores(
          self.proposed_meta_actions, his_last_move)

    # ------------------------------------------------------------
    # GENERATE NEXT MOVES
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # ACTION CHOOSING
    # ------------------------------------------------------------

    # For each scoring function (selector), choose the
    # action based on all of our policy actors
    self.proposed_meta_actions, holdout_action = self.action_choice.choose(
        self.proposed_actions, self.scores,
        self.kumo_outcomes, self.last_chosen_meta_idx)

    # Meta-Selector: selecting the scoring function
    if DEBUG_MODE:
      assert len(self.meta_scores) == \
        len(self.proposed_meta_actions)

    best_meta_action_idx = np.argmax(self.meta_scores)
    if self.meta_scores.max() < 1e-4:
      best_meta_action_idx = np.random.randint(len(self.proposed_meta_actions))
    self.our_last_move = \
      self.proposed_meta_actions[best_meta_action_idx]
    self.last_chosen_meta_idx = best_meta_action_idx

    if holdout_action is not None:
      self.our_last_move = holdout_action

    if verbose:
      score_names = self.scoring.get_score_names()
      print(prefix + 'holdout:', (holdout_action is not None))
      print(prefix + f'chosen_scoring: {score_names[best_meta_action_idx]}')
      print(prefix + f'chosen_action: {self.our_last_move}')
      print(prefix + 'proposed:')
      for sf in np.argsort(self.meta_scores)[::-1]:
        print(f'  - {self.proposed_meta_actions[sf]} ' \
                  f'({self.meta_scores[sf]:.2f}) ' \
                  f'{score_names[sf]}:')
        best_args = np.argsort(self.scores[sf])[::-1][:7]
        for idx in best_args:
          print(f'    - {self.proposed_actions[idx]} ' \
                      f'({self.scores[sf, idx]:.2f}) ' \
                      f'{self.strategy_names[idx]}')

    return self.our_last_move
