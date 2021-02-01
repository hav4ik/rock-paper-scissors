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


opp_hist = []
my_opp_hist = []
offset = 0
last_feat = None
output = None
probs = None


def agent(obs, conf):
    global output, opp_hist, my_opp_hist, offset, last_feat, probs

    if obs.step == 0:
        output = np.random.choice(3)
    else:
        my_opp_hist.append((obs.lastOpponentAction, output))
        opp_hist.append(output)

        if last_feat is not None:
            this_offset = (basis[(opp_hist[-1] + 1) % 3]) * last_feat.conjugate()
            offset = (1 - .01) * offset + .01 * this_offset

        hist_match = find_all_longest(my_opp_hist, 20)
        if not hist_match:
            pred = 0
        else:
            feat = basis[opp_hist[hist_match[0].idx]]
            last_feat = complex_to_probs(feat / abs(feat)) @ basis
            pred = last_feat * offset * cmath.exp(2j * cmath.pi * 1/9)

        probs = complex_to_probs(pred)
        output = (int(np.argmax(probs)) + 1) % 3

    return output
