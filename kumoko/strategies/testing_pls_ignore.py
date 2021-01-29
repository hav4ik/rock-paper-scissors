import random
from operator import itemgetter
from kumoko.kumoko_base import *


class TestingPleaseIgnore:
    K = 20
    def counter_prob(self, probs):
        weighted_list = []
        for h in self.rps:
            weighted = 0
            for p in probs.keys():
                points = self.score[h + p]
                prob = probs[p]
                weighted += points * prob
            weighted_list.append((h, weighted))
        return max(weighted_list, key=itemgetter(1))[0]

    def __init__(self):
        self.score  = {'RR': 0, 'PP': 0, 'SS': 0, \
                  'PR': 1, 'RS': 1, 'SP': 1, \
                  'RP': -1, 'SR': -1, 'PS': -1,}
        self.cscore = {'RR': 'r', 'PP': 'r', 'SS': 'r', \
                  'PR': 'b', 'RS': 'b', 'SP': 'b', \
                  'RP': 'c', 'SR': 'c', 'PS': 'c',}
        self.beat = {'P': 'S', 'S': 'R', 'R': 'P'}
        self.cede = {'P': 'R', 'S': 'P', 'R': 'S'}
        self.rps = ['R', 'P', 'S']
        self.wlt = {1: 0, -1: 1, 0: 2}

        self.played_probs = collections.defaultdict(lambda: 1)
        self.dna_probs = [
            collections.defaultdict(lambda: collections.defaultdict(lambda: 1)) for i in range(18)
        ]
        self.wlt_probs = [collections.defaultdict(lambda: 1) for i in range(9)]
        self.answers = [{'c': 1, 'b': 1, 'r': 1} for i in range(12)]
        self.patterndict = [collections.defaultdict(str) for i in range(6)]
        self.consec_strat_usage = [[0] * 6, [0] * 6,
                                   [0] * 6]  #consecutive strategy usage
        self.consec_strat_candy = [[], [], []]  #consecutive strategy candidates
        self.histories = ["", "", ""]
        self.dna = ["" for i in range(12)]
        self.sc = 0
        self.strats = [[] for i in range(3)]
        
    def next_action(self, T, A, S, B):
        if T == 0:
            self.B = random.choice(self.rps)
            return {'R': 0, 'P': 1, 'S': 2}[self.B]
        prev_sc = self.sc

        self.sc = self.score[self.B + 'RPS'[A]]
        for j in range(3):
            prev_strats = self.strats[j][:]
            for i, c in enumerate(self.consec_strat_candy[j]):
                if c == 'RPS'[A]:
                    self.consec_strat_usage[j][i] += 1
                else:
                    self.consec_strat_usage[j][i] = 0
            m = max(self.consec_strat_usage[j])
            self.strats[j] = [
                i for i, c in enumerate(self.consec_strat_candy[j])
                if self.consec_strat_usage[j][i] == m
            ]

            for s1 in prev_strats:
                for s2 in self.strats[j]:
                    self.wlt_probs[j * 3 + self.wlt[prev_sc]][chr(s1) + chr(s2)] += 1

            if self.dna[2 * j + 0] and self.dna[2 * j + 1]:
                self.answers[2 * j + 0][self.cscore['RPS'[A] + self.dna[2 * j + 0]]] += 1
                self.answers[2 * j + 1][self.cscore['RPS'[A] + self.dna[2 * j + 1]]] += 1
            if self.dna[2 * j + 6] and self.dna[2 * j + 7]:
                self.answers[2 * j + 6][self.cscore['RPS'[A] + self.dna[2 * j + 6]]] += 1
                self.answers[2 * j + 7][self.cscore['RPS'[A] + self.dna[2 * j + 7]]] += 1

            for length in range(min(10, len(self.histories[j])), 0, -2):
                pattern = self.patterndict[2 * j][self.histories[j][-length:]]
                if pattern:
                    for length2 in range(min(10, len(pattern)), 0, -2):
                        self.patterndict[2 * j + 1][pattern[-length2:]] += self.B + 'RPS'[A]
                self.patterndict[2 * j][self.histories[j][-length:]] += self.B + 'RPS'[A]
        self.played_probs['RPS'[A]] += 1
        self.dna_probs[0][self.dna[0]]['RPS'[A]] += 1
        self.dna_probs[1][self.dna[1]]['RPS'[A]] += 1
        self.dna_probs[2][self.dna[1] + self.dna[0]]['RPS'[A]] += 1
        self.dna_probs[9][self.dna[6]]['RPS'[A]] += 1
        self.dna_probs[10][self.dna[6]]['RPS'[A]] += 1
        self.dna_probs[11][self.dna[7] + self.dna[6]]['RPS'[A]] += 1

        self.histories[0] += self.B + 'RPS'[A]
        self.histories[1] += 'RPS'[A]
        self.histories[2] += self.B

        self.dna = ["" for i in range(12)]
        for j in range(3):
            for length in range(min(10, len(self.histories[j])), 0, -2):
                pattern = self.patterndict[2 * j][self.histories[j][-length:]]
                if pattern != "":
                    self.dna[2 * j + 1] = pattern[-2]
                    self.dna[2 * j + 0] = pattern[-1]
                    for length2 in range(min(10, len(pattern)), 0, -2):
                        pattern2 = self.patterndict[2 * j + 1][pattern[-length2:]]
                        if pattern2 != "":
                            self.dna[2 * j + 7] = pattern2[-2]
                            self.dna[2 * j + 6] = pattern2[-1]
                            break
                    break

        probs = {}
        for hand in self.rps:
            probs[hand] = self.played_probs[hand]

        for j in range(3):
            if self.dna[j * 2] and self.dna[j * 2 + 1]:
                for hand in self.rps:
                    probs[hand] *= self.dna_probs[j*3+0][self.dna[j*2+0]][hand] * \
                                   self.dna_probs[j*3+1][self.dna[j*2+1]][hand] * \
                          self.dna_probs[j*3+2][self.dna[j*2+1]+self.dna[j*2+0]][hand]
                    probs[hand] *= self.answers[j*2+0][self.cscore[hand+self.dna[j*2+0]]] * \
                                   self.answers[j*2+1][self.cscore[hand+self.dna[j*2+1]]]
                self.consec_strat_candy[j] = [self.dna[j*2+0], self.beat[self.dna[j*2+0]], self.cede[self.dna[j*2+0]],\
                                         self.dna[j*2+1], self.beat[self.dna[j*2+1]], self.cede[self.dna[j*2+1]]]
                strats_for_hand = {'R': [], 'P': [], 'S': []}
                for i, c in enumerate(self.consec_strat_candy[j]):
                    strats_for_hand[c].append(i)
                pr = self.wlt_probs[self.wlt[self.sc] + 3 * j]
                for hand in self.rps:
                    for s1 in self.strats[j]:
                        for s2 in strats_for_hand[hand]:
                            probs[hand] *= pr[chr(s1) + chr(s2)]
            else:
                self.consec_strat_candy[j] = []
        for j in range(3):
            if self.dna[j * 2 + 6] and self.dna[j * 2 + 7]:
                for hand in self.rps:
                    probs[hand] *= self.dna_probs[j*3+9][self.dna[j*2+6]][hand] * \
                                   self.dna_probs[j*3+10][self.dna[j*2+7]][hand] * \
                          self.dna_probs[j*3+11][self.dna[j*2+7]+self.dna[j*2+6]][hand]
                    probs[hand] *= self.answers[j*2+6][self.cscore[hand+self.dna[j*2+6]]] * \
                                   self.answers[j*2+7][self.cscore[hand+self.dna[j*2+7]]]

        self.B = self.counter_prob(probs)
        return {'R': 0, 'P': 1, 'S': 2}[self.B]


class TestingPlsIgnoreStrategy(BaseAtomicStrategy):
  def __init__(self):
    self.submission = TestingPleaseIgnore()

  def __call__(self, history):
    T = len(history)
    if T > 0:
      A = MOVE_TO_NUM[history.his_moves[-1]]
      B = MOVE_TO_NUM[history.our_moves[-1]]
    else:
      A = None
      B = random.randint(0, 2)
    S = 3
    return NUM_TO_MOVE[int(self.submission.next_action(T, A, S, B))]

# def agent(observation, configuration):
#     T = observation.step
#     A = observation.lastOpponentAction if T > 0 else None
#     S = configuration.signs
# 
#     try:
#         return NUM_TO_MOVE[int(self.submission.next_action(T, A, S))]
#     except Exception as e:
#         print(T, f'Failed', e)
#         return random.choice('RPS')
