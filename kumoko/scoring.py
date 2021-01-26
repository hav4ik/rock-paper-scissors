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
    return [
        f'std_dllu_{i}'
        for i in range(len(self.scoring_funcs))]


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
    return [f'static_wnd_{ws}' for ws in self.window_sizes]


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
  'static_wnd_v3': static_window_factory(
      window_sizes=[10, 20, 50],
      meta_scoring_config=[
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
            0.94,  3.00,    0.00,     -3.00,    0.00,      False,     True,
      ],
      safeguard=0.25),

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
}
