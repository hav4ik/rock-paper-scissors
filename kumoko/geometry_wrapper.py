import operator
import numpy as np
import cmath
from typing import List
from collections import namedtuple
import traceback
import sys


basis = np.array(
    [1, cmath.exp(2j * cmath.pi * 1 / 3), cmath.exp(2j * cmath.pi * 2 / 3)]
)
HistMatchResult = namedtuple("HistMatchResult", "idx length")


def probs_to_complex(p):
    return p @ basis


def _fix_probs(probs):
    """
    Put probs back into triangle. Sometimes this happens due to rounding errors or if you
    use complex numbers which are outside the triangle.
    """
    if min(probs) < 0:
        probs -= min(probs)
    probs /= sum(probs)
    return probs


def complex_to_probs(z):
    probs = (2 * (z * basis.conjugate()).real + 1) / 3
    probs = _fix_probs(probs)
    return probs


def z_from_action(action):
    return basis[action]


def sample_from_z(z):
    probs = complex_to_probs(z)
    return np.random.choice(3, p=probs)


def bound(z):
    return probs_to_complex(complex_to_probs(z))


def norm(z):
    return bound(z / abs(z))


class Pred:
    def __init__(self, *, alpha):
        self.offset = 0
        self.alpha = alpha
        self.last_feat = None

    def train(self, target):
        if self.last_feat is not None:
            offset = target * self.last_feat.conjugate()   # fixed
            self.offset = (1 - self.alpha) * self.offset + self.alpha * offset

    def predict(self, feat):
        """
        feat is an arbitrary feature with a probability on 0,1,2
        anything which could be useful anchor to start with some kind of sensible direction
        """
        feat = norm(feat)

        # offset = mean(target - feat)
        # so here we see something like: result = feat + mean(target - feat)
        # which seem natural and accounts for the correlation between target and feat
        # all RPSContest bots do no more than that, just in a hidden way
        result = feat * self.offset
        self.last_feat = feat
        return result


class BaseWrapper:
    def __init__(self):
        self.my_hist = []
        self.opp_hist = []
        self.my_opp_hist = []
        self.outcome_hist = []

    def __call__(self,
                 our_last_move,
                 his_last_move,
                 proposed_action,
                 factor=1.0):
        try:
            opp = his_last_move
            my = our_last_move

            self.my_opp_hist.append((my, opp))
            self.opp_hist.append(opp)

            outcome = {0: 0, 1: 1, 2: -1}[(my - opp) % 3]
            self.outcome_hist.append(outcome)
            action = self.action(proposed_action, factor)
            self.my_hist.append(action)

            return action
        except Exception:
            traceback.print_exc(file=sys.stderr)
            raise

    def action(self, proposed_action, factor):
        pass


class GeometryWrapper(BaseWrapper):
    def __init__(self, alpha=0.01):
        super().__init__()
        self.predictor = Pred(alpha=alpha)

    def action(self, proposed_action, factor):
        self.train()
        pred = self.predictor.predict(
            z_from_action((proposed_action + 2) % 3))
        return_action = sample_from_z(factor * pred)
        return return_action

    def train(self):
        last_beat_opp = z_from_action((self.opp_hist[-1] + 1) % 3)
        self.predictor.train(last_beat_opp)
