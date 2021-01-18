import random
from kumoko.kumoko_base import *
from kumoko.kumoko import Kumoko
from kumoko.scoring import get_dllu_scoring


class RFindStrategy(BaseAtomicStrategy):
  def __init__(self, limit=None, src='his', shenanigans=True):
    self.limit = limit
    self.src = src
    self.shenanigans = shenanigans

  def __call__(self, history):
    if len(history) == 0:
      return NUM_TO_MOVE[random.randint(0, 2)]

    # Type of lookback sequence
    if self.src == 'his':
      sequence = history.his_moves
    elif self.src == 'our':
      sequence = history.our_moves
    elif self.src == 'dna':
      sequence = history.dna_moves
    else:
      raise ValueError(f'Invalid `src` value (got {self.src}')

    # Define lookback window
    length = len(history)
    if self.limit == None:
      lb = length
    else:
      lb = min(length, self.limit)

    # RFind choose action
    while lb >= 1 and \
        not sequence[length - lb:length] in sequence[0:length - 1]:
      lb -= 1
    if lb >= 1:
      if self.shenanigans:
        if random.random() < 0.6:
          idx = sequence.rfind(
              sequence[length - lb:length], 0, length - 1)
        elif random.random() < 0.5:
          idx = sequence.rfind(
              sequence[length - lb:length], 0, length - 1)
          idx2 = sequence.rfind(
              sequence[length - lb:length], 0, idx)
          if idx2 != -1:
            idx = idx2
        else:
          idx = sequence.find(
              sequence[length - lb:length], 0, length - 1)
      else:
        idx = sequence.rfind(
            sequence[length - lb:length], 0, length - 1)
      return BEAT[history.his_moves[idx + lb]]
    else:
      return random.choice('RPS')


class WrappedRFindStrategy(BaseAtomicStrategy):
  """A strategy that contains a Kumoko inside!
  """
  class _RFindInnerEnsemble:
    """Only Rfind, nothing else!
    """
    def __init__(self, limits, sources, shenanigans=True):
      self.limits = limits
      self.sources = sources
      self.shenanigans = shenanigans

    def generate(self):
      """List of strategies (including mirror strategies)
      """
      strategies = []

      # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
      limits=[50, 20, 10]
      sources = ['his', 'our', 'dna']
      for limit in limits:
        for source in sources:
          strategies.extend(
              generate_meta_strategy_pair(
                RFindStrategy,
                limit=limit,
                src=source,
                shenanigans=False,
              ))

      return strategies

  class _RFindInnerScoring:
    def generate_normal(self):
      """List of scoring functions
      """
      # Add DLLU's scoring methods from his blog
      # https://daniel.lawrence.lu/programming/rps/
      dllu_scoring_configs = [
          # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
          [ 0.80,  3.00,    0.00,     -3.00,    0.00,      False,     False    ],
          [ 0.87,  3.30,    -0.90,    -3.00,    0.00,      False,     False    ],
          [ 1.00,  3.00,    0.00,     -3.00,    1.00,      False,     False    ],
          [ 1.00,  3.00,    0.00,     -3.00,    1.00,      True,      False    ],
      ]
      scoring_funcs = [
          get_dllu_scoring(*cfg)
          for cfg in dllu_scoring_configs]
      return scoring_funcs

    def get_meta_scoring(self):
      """Generates a meta scoring function
      """
      meta_scoring_func = get_dllu_scoring(
          decay=0.94,
          win_value=3.0,
          draw_value=0.0,
          lose_value=-3.0,
          drop_prob=0.87,
          drop_draw=False,
          clip_zero=True)
      return meta_scoring_func

  def __init__(self, limits, sources, shenanigans=True):
    ensemble = self._RFindInnerEnsemble(limits, sources, shenanigans)
    scoring = self._RFindInnerScoring()
    self.kumoko = Kumoko(ensemble=ensemble, scoring=scoring)

  def __call__(self, history):
    if len(history) > 0:
      our_last_move = history.our_moves[-1]
      his_last_move = history.his_moves[-1]
    else:
      our_last_move = None
      his_last_move = None
    return self.kumoko.next_action(our_last_move, his_last_move)
