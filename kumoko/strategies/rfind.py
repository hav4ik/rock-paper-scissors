import random
from kumoko.kumoko_base import *
from kumoko.kumoko import Kumoko
from kumoko.scoring import SCORINGS
from functools import partial


class RFindStrategy(BaseAtomicStrategy):
  def __init__(self, limit=None, src='his', shenanigans=True):
    self.limit = limit
    self.src = src
    self.shenanigans = shenanigans

  def name(self):
    name = f'RFind_{self.limit}_{self.src}'
    if self.shenanigans:
      name += '_with_shen'
    return name

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

      do_rotations = [True for _ in strategies]
      return strategies, do_rotations

  def __init__(self, limits, sources, shenanigans=True):
    ensemble_cls = partial(self._RFindInnerEnsemble,
                           limits=limits,
                           sources=sources,
                           shenanigans=shenanigans)
    scoring_cls = SCORINGS['std_dllu_v1']
    self.kumoko = Kumoko(ensemble_cls=ensemble_cls, scoring_cls=scoring_cls)

  def __call__(self, history):
    if len(history) > 0:
      our_last_move = history.our_moves[-1]
      his_last_move = history.his_moves[-1]
    else:
      our_last_move = None
      his_last_move = None
    return self.kumoko.next_action(our_last_move, his_last_move)
