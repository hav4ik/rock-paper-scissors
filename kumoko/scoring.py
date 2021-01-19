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
  def compute_metameta_scores(self, proposed_metameta_moves, his_move):
    return NotImplemented

  @abstractmethod
  def get_initial_scores(self):
    return NotImplemented

  @abstractmethod
  def get_initial_meta_scores(self):
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


def standard_dllu_factory(scoring_configs,
                          meta_scoring_config):
  return partial(StandardDllu,
                 scoring_configs,
                 meta_scoring_config)



SCORINGS = {
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
}
