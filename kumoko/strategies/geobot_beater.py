from kumoko.kumoko_base import *

import operator
import numpy as np
import cmath
from collections import namedtuple


basis = np.array([1, cmath.exp(2j * cmath.pi * 1 / 3), cmath.exp(2j * cmath.pi * 2 / 3)])
HistMatchResult = namedtuple("HistMatchResult", "idx length")


def find_all_longest(seq, max_len=None):
  result = []
  i_search_start = len(seq) - 2
  while i_search_start > 0:
    i_sub = -1
    i_search = i_search_start
    length = 0
    while i_search >= 0 and seq[i_sub] == seq[i_search]:
      length += 1
      i_sub -= 1
      i_search -= 1
      if max_len is not None and length > max_len: break
    if length > 0: result.append(HistMatchResult(i_search_start + 1, length))
    i_search_start -= 1
  return sorted(result, key=operator.attrgetter("length"), reverse=True)


def complex_to_probs(z):
    probs = (2 * (z * basis.conjugate()).real + 1) / 3
    if min(probs) < 0: probs -= min(probs)
    return probs / sum(probs)


class GeobotBeater:
  def __init__(self):
    self.opp_hist = []
    self.my_opp_hist = []
    self.offset = 0
    self.last_feat = None

  def __call__(self, step, our_last_action, opp_last_action):
    if step == 0:
      action = np.random.choice(3)
    else:
      self.my_opp_hist.append((opp_last_action, our_last_action))
      self.opp_hist.append(our_last_action)
      if self.last_feat is not None:
        this_offset = (basis[(self.opp_hist[-1] + 1) % 3]) * self.last_feat.conjugate()
        self.offset = (1 - .01) * self.offset + .01 * this_offset
      hist_match = find_all_longest(self.my_opp_hist, 20)
      if not hist_match:
        pred = 0
      else:
        feat = basis[self.opp_hist[hist_match[0].idx]]
        self.last_feat = complex_to_probs(feat / abs(feat)) @ basis
        pred = self.last_feat * self.offset * cmath.exp(2j * cmath.pi * 1/9)
      probs = complex_to_probs(pred)
      if probs[np.argmax(probs)] > .334:
        action = (int(np.argmax(probs))+1)%3
      else:
        action = (np.random.choice(3, p=probs)+1)%3
    return action


class GeobotBeaterStrategy(BaseAtomicStrategy):
  def __init__(self):
    super().__init__()
    self.beater = GeobotBeater()

  def __call__(self, history):
    step = len(history)
    if step > 0:
      our_last_move = MOVE_TO_NUM[history.our_moves[-1]]
      his_last_move = MOVE_TO_NUM[history.his_moves[-1]]
    else:
      our_last_move, his_last_move = None, None
    return NUM_TO_MOVE[self.beater(step, our_last_move, his_last_move)]
