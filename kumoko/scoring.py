from kumoko.kumoko_base import *
from abc import ABC, abstractmethod
from functools import partial


class BaseScoringOracle:
  @abstractmethod
  def set_num_strategies(self, n):
    raise NotImplemented

  @abstractmethod
  def compute_scores(self, proposed_moves, his_move):
    return NotImplemented

  @abstractmethod
  def compute_meta_scores(self, proposed_meta_moves, his_move):
    return NotImplemented

  @abstractmethod
  def get_initial_scores(self):
    return NotImplemented

  @abstractmethod
  def get_initial_meta_scores(self):
    return NotImplemented

  @abstractmethod
  def get_score_names(self):
    return NotImplemented


class StandardDllu(BaseScoringOracle):
  """DLLU scoring, as in the blog
  """
  def __init__(self, scoring_configs, meta_scoring_config):
    super().__init__()

    # Add DLLU's scoring methods from his blog
    # https://daniel.lawrence.lu/programming/rps/
    self.scoring_funcs = [
        get_dllu_scoring(*cfg) for cfg in scoring_configs]
    self.meta_scoring_func = get_dllu_scoring(*meta_scoring_config)
    self.score_names = []
    for cfg in scoring_configs:
      score_name = f'dllu_[{cfg[0]:.2f}]_' \
                   f'[{cfg[1]:.1f}]_[{cfg[2]:.1f}]_[{cfg[3]:.1f}]_' \
                   f'[{cfg[4]:.1f}]'
      if cfg[5]:
        score_name += '_dd'
      if cfg[6]:
        score_name += '_cz'
      self.score_names.append(score_name)

    self.num_strategies = -1
    self.scores = None
    self.meta_scores = None

  def set_num_strategies(self, n):
    self.num_strategies = n
    self.scores = np.zeros((len(self.scoring_funcs), n))
    self.meta_scores = np.zeros((len(self.scoring_funcs), ))

  def compute_scores(self, proposed_moves, his_move):
    """Calculate scores for each strategy
    """
    assert len(proposed_moves) == self.num_strategies
    for sf in range(len(self.scoring_funcs)):
      for pa in range(len(proposed_moves)):
        self.scores[sf, pa] = self.scoring_funcs[sf](
            self.scores[sf, pa],
            proposed_moves[pa], his_move)
    return self.scores

  def compute_meta_scores(self, proposed_moves, his_move):
    """Generates a meta scoring function
    """
    assert len(proposed_moves) == len(self.meta_scores)
    assert len(proposed_moves) == len(self.scoring_funcs)
    for sf in range(len(self.scoring_funcs)):
      self.meta_scores[sf] = self.meta_scoring_func(
          self.meta_scores[sf],
          proposed_moves[sf], his_move)
    return self.meta_scores

  def get_initial_scores(self):
    """Initial scores at step 0"""
    assert self.scores.shape[0] == len(self.scoring_funcs)
    assert self.scores.shape[1] == self.num_strategies
    return self.scores

  def get_initial_meta_scores(self):
    """Initial meta-scores at step 0"""
    assert len(self.meta_scores) == len(self.scoring_funcs)
    return self.meta_scores

  def get_score_names(self):
    return self.score_names


def standard_dllu_factory(scoring_configs,
                          meta_scoring_config):
  return partial(StandardDllu,
                 scoring_configs,
                 meta_scoring_config)


class StaticWindow(BaseScoringOracle):
  def __init__(self, window_sizes, meta_scoring_config, safeguard=None):
    super().__init__()
    self.window_sizes = np.array(window_sizes)
    self.num_strategies = -1
    self.outcomes = None
    self.step = 0
    self.meta_scoring_func = get_dllu_scoring(*meta_scoring_config)
    self.safeguard = safeguard

  def set_num_strategies(self, n):
    self.num_strategies = n
    self.outcomes = np.zeros((1000, n))
    self.scores = np.zeros((len(self.window_sizes), n))
    self.meta_scores = np.zeros((len(self.window_sizes), ))

  def compute_scores(self, proposed_moves, his_move):
    """Calculate scores for each strategy
    """
    # Save outcomes in the memory and increase step counter
    assert len(proposed_moves) == self.num_strategies
    for pa, proposed_move in enumerate(proposed_moves):
      if proposed_move == BEAT[his_move]:
        self.outcomes[self.step, pa] = 1
      elif proposed_move == CEDE[his_move]:
        self.outcomes[self.step, pa] = -1
      else:
        self.outcomes[self.step, pa] = 0
    self.step += 1

    # Calculating the values of before/after windows
    for ws, window_size in enumerate(self.window_sizes):
      if window_size > self.step:
        self.scores[ws, ...] = np.random.random_sample(
            self.scores[ws, ...].shape)
      else:
        self.scores[ws, ...] = np.sum(
            self.outcomes[
              self.step - window_size:self.step], axis=0)
        if self.safeguard is not None:
          self.scores[ws][self.scores[ws] < self.safeguard * window_size] = 0.
    return self.scores

  def compute_meta_scores(self, proposed_moves, his_move):
    """Generates a meta scoring function
    """
    assert len(proposed_moves) == len(self.meta_scores)
    assert len(proposed_moves) == len(self.window_sizes)
    for sf in range(len(self.window_sizes)):
      self.meta_scores[sf] = self.meta_scoring_func(
          self.meta_scores[sf],
          proposed_moves[sf], his_move)
    return self.meta_scores

  def get_initial_scores(self):
    """Initial scores at step 0"""
    assert self.scores.shape[0] == len(self.window_sizes)
    assert self.scores.shape[1] == self.num_strategies
    return self.scores

  def get_initial_meta_scores(self):
    """Initial meta-scores at step 0"""
    assert len(self.meta_scores) == len(self.window_sizes)
    return self.meta_scores

  def get_score_names(self):
    return [f'static_wnd_{ws}' for ws in self.window_sizes]


def static_window_factory(window_sizes,
                          meta_scoring_config,
                          safeguard=None):
  return partial(StaticWindow,
                 window_sizes,
                 meta_scoring_config,
                 safeguard)


class RiskManagement(BaseScoringOracle):
  def __init__(self,
               window_sizes,
               score_decays,
               loss_penalty_alphas,
               meta_scoring_config,
               safeguard=None):
    super().__init__()
    self.window_sizes = np.array(window_sizes)
    self.num_strategies = -1
    self.outcomes = None
    self.step = 0
    self.score_decays = score_decays
    self.meta_scoring_func = get_dllu_scoring(*meta_scoring_config)
    self.safeguard = safeguard
    self.loss_penalty_alphas = loss_penalty_alphas
    assert len(self.score_decays) == len(self.window_sizes)
    assert len(self.loss_penalty_alphas) == len(self.window_sizes)
    self.score_names = []
    for ws in range(len(self.window_sizes)):
      score_name = f'risk_mng_[{window_sizes[ws]}]' \
                   f'_[{score_decays[ws]:.2f}]' \
                   f'_[{loss_penalty_alphas[ws]:.2f}]'
      self.score_names.append(score_name)

  def set_num_strategies(self, n):
    self.num_strategies = n
    self.outcomes = np.zeros((1000, n))
    self.scores = np.zeros((len(self.window_sizes), n))
    self.meta_scores = np.zeros((len(self.window_sizes), ))

  def compute_scores(self, proposed_moves, his_move):
    """Calculate scores for each strategy
    """
    # Save outcomes in the memory and increase step counter
    assert len(proposed_moves) == self.num_strategies
    for pa, proposed_move in enumerate(proposed_moves):
      if proposed_move == BEAT[his_move]:
        self.outcomes[self.step, pa] = 1
      elif proposed_move == CEDE[his_move]:
        self.outcomes[self.step, pa] = -1
      else:
        self.outcomes[self.step, pa] = 0
    self.step += 1

    # Calculating the values of before/after windows
    for ws, window_size in enumerate(self.window_sizes):
      # Also, we need to store number of losses for penalty
      losses = np.zeros((self.num_strategies, ))
      assert losses.shape[0] == self.scores.shape[1]

      # Moving average with decay inside each window
      self.scores[ws, ...] = 0.
      for stp in range(max(0, self.step - window_size), self.step):
        self.scores[ws, ...] = \
            self.scores[ws, ...] * self.score_decays[ws] + self.outcomes[stp]
        # Count losses at each step
        losses[self.outcomes[stp] == -1] += 1.

      # Additional penalty for variance in outcome
      self.scores[ws, ...] -= self.loss_penalty_alphas[ws] * losses

      # Safeguard to remove weak strategies
      decayed_size = 0.
      for _ in range(window_size):
        decayed_size = self.score_decays[ws] * decayed_size + 1.
      if self.safeguard is not None:
        self.scores[ws][self.scores[ws] < self.safeguard * decayed_size] = 0.

    # Resulting scores
    return self.scores

  def compute_meta_scores(self, proposed_moves, his_move):
    """Generates a meta scoring function
    """
    assert len(proposed_moves) == len(self.meta_scores)
    assert len(proposed_moves) == len(self.window_sizes)
    for sf in range(len(self.window_sizes)):
      self.meta_scores[sf] = self.meta_scoring_func(
          self.meta_scores[sf],
          proposed_moves[sf], his_move)
    return self.meta_scores

  def get_initial_scores(self):
    """Initial scores at step 0"""
    assert self.scores.shape[0] == len(self.window_sizes)
    assert self.scores.shape[1] == self.num_strategies
    return self.scores

  def get_initial_meta_scores(self):
    """Initial meta-scores at step 0"""
    assert len(self.meta_scores) == len(self.window_sizes)
    return self.meta_scores

  def get_score_names(self):
    return self.score_names


def risk_management_factory(window_sizes,
                            score_decays,
                            loss_penalty_alphas,
                            meta_scoring_config,
                            safeguard=None):
  return partial(RiskManagement,
                 window_sizes,
                 score_decays,
                 loss_penalty_alphas,
                 meta_scoring_config,
                 safeguard)


class CombinedScoring(BaseScoringOracle):
  def __init__(self,
               scoring_strategies,
               meta_scoring_config,
               local_meta_scores=False):
    super().__init__()
    self.scoring_strategies = [
        SCORINGS[scoring_clsname]()
        for scoring_clsname in scoring_strategies]
    self.score_names = []
    for scoring_strategy in self.scoring_strategies:
      self.score_names.extend(scoring_strategy.get_score_names())
    self.meta_scoring_func = get_dllu_scoring(*meta_scoring_config)

    self.num_strategies = -1
    self.combined_scores = None
    self.concatenated_scores = None
    self.meta_scores = None
    self.ranges = []
    self.local_meta_scores = local_meta_scores

  def set_num_strategies(self, n):
    self.num_strategies = n

    # Initialize num strats on each child scoring
    for scoring_strategy in self.scoring_strategies:
      scoring_strategy.set_num_strategies(n)

    # Combined scores collects all scoring matrices
    # from each scoring strategy
    self.combined_scores = [
        scoring_strategy.get_initial_scores()
        for scoring_strategy in self.scoring_strategies]
    range_counter = 0

    num_scoring_funcs = np.sum([
      scores.shape[0] for scores in self.combined_scores])

    if self.local_meta_scores:
      for scores in self.combined_scores:
        self.ranges.append(
            (range_counter, range_counter + scores.shape[0]))
        range_counter += scores.shape[0]
      for i, r in enumerate(self.ranges[:-1]):
        assert self.ranges[i+1][0] == self.ranges[i][1]
        assert self.ranges[i][0] < self.ranges[i][1]
      for i, r in enumerate(self.ranges):
        assert len(self.combined_scores[i]) == r[1] - r[0]
      assert self.ranges[-1][1] == num_scoring_funcs
      assert len(self.ranges) == len(self.scoring_strategies)

    # the len of meta scores still have to be as long as all strats
    self.meta_scores = np.zeros((num_scoring_funcs, ))

  def compute_scores(self, proposed_moves, his_move):
    """Calculate scores for each strategy"""
    assert len(proposed_moves) == self.num_strategies
    # Combined scores collects all scoring matrices
    # from each scoring strategy
    self.combined_scores = [
        scoring_strategy.compute_scores(proposed_moves, his_move)
        for scoring_strategy in self.scoring_strategies]
    self.scores = np.concatenate(
        self.combined_scores, axis=0)
    assert len(self.scores.shape) == 2
    assert self.scores.shape[1] == self.num_strategies
    return self.scores

  def compute_meta_scores(self, proposed_moves, his_move):
    """Generates a meta scoring function
    """
    if not self.local_meta_scores:
      # Flat score computing
      assert len(proposed_moves) == len(self.meta_scores)
      for sf in range(len(self.meta_scores)):
        self.meta_scores[sf] = self.meta_scoring_func(
            self.meta_scores[sf],
            proposed_moves[sf], his_move)
      return self.meta_scores
    else:
      # Using meta scores of each group, and only apply global
      # scoring after that
      assert len(proposed_moves) == self.ranges[-1][1]
      assert len(self.scoring_strategies) == len(self.ranges)
      local_meta_scores = [
          strategy.compute_meta_scores(
            proposed_moves[rng[0]:rng[1]], his_move)
          for rng, strategy in zip(
            self.ranges, self.scoring_strategies)]
      local_chosen_move_idxs = []
      for rng, local_meta_score in zip(self.ranges, local_meta_scores):
        assert len(local_meta_score) == len(proposed_moves[rng[0]:rng[1]])
        best_meta_action_idx = np.argmax(local_meta_score)
        local_chosen_move_idxs.append(best_meta_action_idx)

      # After computing local (group) meta scores, compute global one
      for sf in range(len(self.meta_scores)):
        self.meta_scores[sf] = self.meta_scoring_func(
            self.meta_scores[sf],
            proposed_moves[sf], his_move)

      # One-hot encoding for the winning local strategy. This can be
      # also replaced with softmax with temperature, but no need here
      # as only the max one will be chosen anyways.
      def one_hot(a, num_classes):
        return np.squeeze(np.eye(num_classes)[a])

      # Correct the scores
      for rng, local_chosen_move_idx in zip(self.ranges, local_chosen_move_idxs):
        self.meta_scores[rng[0]:rng[1]] *= one_hot(
            local_chosen_move_idx, rng[1] - rng[0])
      return self.meta_scores

  def get_initial_scores(self):
    combined_initial_scores = np.concatenate(
        self.combined_scores, axis=0)
    assert len(combined_initial_scores.shape) == 2
    assert combined_initial_scores.shape[1] == self.num_strategies
    return combined_initial_scores

  def get_initial_meta_scores(self):
    """Initial meta-scores at step 0"""
    return self.meta_scores

  def get_score_names(self):
    return self.score_names


def combined_scoring_factory(scoring_strategies,
                             meta_scoring_config,
                             local_meta_scores):
  return partial(CombinedScoring,
                 scoring_strategies=scoring_strategies,
                 meta_scoring_config=meta_scoring_config,
                 local_meta_scores=local_meta_scores)


SCORINGS = {
  # DLLU-based scorings:
  'std_dllu_v1': standard_dllu_factory(
      scoring_configs=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
          [ 0.80,  3.00,    0.00,     -3.00,    0.00,      False,     False    ],
          [ 0.87,  3.30,    -0.90,    -3.00,    0.00,      False,     False    ],
          [ 1.00,  3.00,    0.00,     -3.00,    1.00,      False,     False    ],
          [ 1.00,  3.00,    0.00,     -3.00,    1.00,      True,      False    ],
      ],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.87,      False,     True,
      ]),

  # DLLU-based scorings:
  'std_dllu_v1_old': standard_dllu_factory(
      scoring_configs=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
          [ 0.80,  3.00,    0.00,     -3.00,    0.00,      False,     False    ],
          [ 0.87,  3.30,    -0.90,    -3.00,    0.00,      False,     False    ],
          [ 1.00,  3.00,    0.00,     -3.00,    0.00,      False,     False    ],
          [ 1.00,  3.00,    0.00,     -3.00,    0.00,      True,      False    ],
      ],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.0,      False,     True,
      ]),

  # Static window scoring:
  'static_wnd_v1': static_window_factory(
      window_sizes=[10, 20, 50],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.87,      False,     True,
      ]),

  # Static window scoring:
  'static_wnd_v2': static_window_factory(
      window_sizes=[10, 20, 50],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.87,      False,     True,
      ],
      safeguard=0.25),

  # Static window scoring:
  'static_wnd_v2_old': static_window_factory(
      window_sizes=[10, 20, 50],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.00,      False,     True,
      ],
      safeguard=0.25),

  # Static window scoring:
  'static_wnd_v4': static_window_factory(
      window_sizes=[5, 10, 20, 50, 75],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.87,      False,     True,
      ],
      safeguard=0.20),

  # Risk management scoring:
  'risk_mng_v1': risk_management_factory(
      window_sizes=[10, 20, 50],
      score_decays=[0.975, 0.975, 0.975],
      loss_penalty_alphas=[0.1, 0.1, 0.1],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.50,      False,     True,
      ],
      safeguard=0.20),

  # Risk management scoring:
  'risk_mng_v2': risk_management_factory(
      window_sizes=[5, 10, 20, 50, 75],
      score_decays=[0.90, 0.94, 0.96, 0.97, 0.99],
      loss_penalty_alphas=[0.1, 0.1, 0.1, 0.1, 0.1],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.87,      False,     True,
      ],
      safeguard=0.20),

  'combined_v1': combined_scoring_factory(
      scoring_strategies=[
        'std_dllu_v1', 'static_wnd_v2', 'risk_mng_v1'],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.99,  3.00,    0.00,     -3.00,    0.00,      False,     False,
      ],
      local_meta_scores=False),

  # DLLU-based scorings: for furiously fast rotations
  'std_dllu_v2': standard_dllu_factory(
      scoring_configs=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
          [ 0.80,  3.00,    0.00,     -3.00,    0.00,      False,     False    ],
          [ 0.87,  3.30,    -0.90,    -3.00,    0.00,      False,     False    ],
          [ 1.00,  3.00,    0.00,     -3.00,    1.00,      False,     False    ],
          [ 1.00,  3.00,    0.00,     -3.00,    1.00,      True,      False    ],
      ],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.87,      False,     True,
      ]),

  # Static window scoring: more conservative, long-term planning
  'static_wnd_v5': static_window_factory(
      window_sizes=[10, 20, 50],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.96,  3.00,    0.00,     -3.00,    0.00,      False,     True,
      ],
      safeguard=0.25),

  # Risk management scoring:
  'risk_mng_v3': risk_management_factory(
      window_sizes=[10, 20, 50, 75],
      score_decays=[0.94, 0.96, 0.97, 0.99],
      loss_penalty_alphas=[0.1, 0.1, 0.1, 0.1, 0.1],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.97,  3.00,    0.00,     -3.00,    0.00,      False,     True,
      ],
      safeguard=0.20),

  # Combined scoring with grouped local meta-scoring
  'combined_v1_loc': combined_scoring_factory(
      scoring_strategies=[
        'std_dllu_v2', 'static_wnd_v5', 'risk_mng_v1'],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.99,  3.00,    0.00,     -3.00,    0.00,      False,     False,
      ],
      local_meta_scores=True),

  'combined_v2': combined_scoring_factory(
      scoring_strategies=[
        'std_dllu_v1', 'static_wnd_v2', 'risk_mng_v1'],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.96,  3.00,    0.00,     -3.00,    0.00,      False,     False,
      ],
      local_meta_scores=False),
}
