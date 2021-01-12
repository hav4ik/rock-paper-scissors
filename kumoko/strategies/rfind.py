import random
from kumoko.kumoko_base import *


class RFindStrategy(BaseAtomicStrategy):
  def __init__(self, limit=None, src='his'):
    self.limit = limit
    self.src = src

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
      return BEAT[history.his_moves[idx + lb]]
    else:
      return random.choice('RPS')
