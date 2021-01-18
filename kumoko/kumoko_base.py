from abc import ABC, abstractmethod
import random
import functools
import numpy as np

import collections


#----------------------------------------------------------
#  CONSTANTS
#----------------------------------------------------------

DEBUG_MODE = True
NUM_TO_MOVE = ['R', 'P', 'S']
MOVE_TO_NUM = {'R': 0, 'P': 1, 'S': 2}

BEAT = {'R': 'P', 'P': 'S', 'S': 'R', None: None}
CEDE = {'R': 'S', 'P': 'R', 'S': 'P', None: None}
DNA_ENCODE = {
    'RP': 'a', 'PS': 'b', 'SR': 'c',
    'PR': 'd', 'SP': 'e', 'RS': 'f',
    'RR': 'g', 'PP': 'h', 'SS': 'i'}


#----------------------------------------------------------
#  MAIN CLASSES AND METHODS
#----------------------------------------------------------

class HistoryHolder:
  """Holds the sequence of moves since the start of the game"""
  def __init__(self):
    self.our_moves = ''
    self.his_moves = ''
    self.dna_moves = ''

  def add_moves(self, our_move, his_move):
    self.our_moves += our_move
    self.his_moves += his_move
    self.dna_moves += DNA_ENCODE[our_move + his_move]

  def __len__(self):
    if DEBUG_MODE:
      assert len(self.our_moves) == len(self.his_moves)
      assert len(self.our_moves) == len(self.dna_moves)
    return len(self.our_moves)


class HolisticHistoryHolder:
  """Holds actual history and the history in opponent's shoes"""
  def __init__(self):
    self.actual_history = HistoryHolder()
    self.mirror_history = HistoryHolder()

  def add_moves(self, our_move, his_move):
    self.actual_history.add_moves(our_move, his_move)
    self.mirror_history.add_moves(his_move, our_move)

  def __len__(self):
    if DEBUG_MODE:
      assert len(self.actual_history) == len(self.mirror_history)
    return len(self.actual_history)


class BaseAtomicStrategy(ABC):
  """Interface for all atomic strategies"""

  @abstractmethod
  def __call__(self, history):
    """Returns an action to take, given the game history"""
    pass


def shift_action(action, shift):
  shift = shift % 3
  if shift == 0: return action
  elif shift == 1: return BEAT[action]
  elif shift == 2: return CEDE[action]


def generate_meta_strategy_pair(atomic_strategy_cls,
                                mirroring=True,
                                *args, **kwargs):
  """Generate pair of strategy and anti-strategies"""
  actual_atomic = atomic_strategy_cls(*args, **kwargs)
  def _actual_strategy(holistic_history):
    return actual_atomic(holistic_history.actual_history)

  if mirroring:
    mirror_atomic = atomic_strategy_cls(*args, **kwargs)
    def _mirror_strategy(holistic_history):
      move = mirror_atomic(holistic_history.mirror_history)
      return BEAT[move]
    return _actual_strategy, _mirror_strategy

  else:
    return _actual_strategy
