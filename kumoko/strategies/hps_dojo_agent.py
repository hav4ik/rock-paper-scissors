# This agent is taken from High-Performance RPS Dojo notebook:
# https://www.kaggle.com/elvenmonk/high-performance-rps-dojo/output

import secrets
import random
import math
import numpy as np
from kumoko.kumoko_base import *


def get_score(S, A1, A2):
    return (S + A1 - A2 + 1) % S - 1

class _Submission:
    K = 10
    def __init__(self, verbose=False):
        self.B = 0
        # Jitter - steps before next non-random move
        self.Jmax = 2
        self.J2 = (self.Jmax+1)**2
        self.J = int(math.sqrt(secrets.randbelow(self.J2)))
        # Depth - number of previous steps taken into consideration
        self.Dmin = 2
        self.Dmax = 6
        self.DL = self.Dmax-self.Dmin+1
        self.HL = 2
        self.HText = ['Opp',  'Me', 'Score']
        self.Depth = np.arange(self.DL)
        self.Hash = np.zeros((self.HL, self.DL), dtype=int)
        self.G = 2
        self.R = 0.4
        self.RG = (1-self.R) * self.G
        self.Threshold = 0.2
        self.verbose = verbose
        
    def split_idx(self, idx):
        d = idx % self.DL
        idx //= self.DL
        h2 = idx % self.HL
        idx //= self.HL
        h1 = idx % self.HL
        idx //= self.HL
        return d, h1, h2, idx
    
    def next_action(self, T, A, S, B):
        self.B = B
        B, HL, DL, Dmin, Dmax = self.B, self.HL, self.DL, self.Dmin, self.Dmax
        SD = S**self.DL
        PR = None
        if T == 0:
            self.Map = np.zeros((S, SD**2, HL, HL, DL))
            self.SList = np.arange(S)[:,None,None,None]
            self.Predicts = np.full((HL, HL, DL), S, dtype=int)
            self.Attempts = np.zeros((HL, HL, DL), dtype=int)
            self.Scores = np.zeros((S, HL, HL, DL))
            self.OrgID = np.ogrid[:S, :HL, :HL, :DL]
            self.Hash2 = self.Hash[None,:] + SD*self.Hash[:,None]
        else:
            C = get_score(S, A, B) + 1
            if self.verbose: print(T, f'{B}-{A} {1-C}')
            ABC = np.array([A, B, C])[:,None]
            Depth, Hash, Hash2, Map, SList, OrgID, Predicts, Attempts, Scores = self.Depth, self.Hash, self.Hash2, self.Map, self.SList, self.OrgID, self.Predicts, self.Attempts, self.Scores
            # Update Moves Map by previous move and previous Hash
            Map *= 0.995
            Map[OrgID[0], Hash2, OrgID[1], OrgID[2], OrgID[3]] += (T > Depth + Dmin) * (SList == A)
            # Update Hash by previous move
            Hash[:] //= S
            Hash[:] += ABC[:HL] * S**Depth
            Hash2[:] = Hash[None,:] + SD*Hash[:,None]
            
            # Update prediction scores by previous move
            PB = Predicts < S
            Attempts[:] = Attempts + PB
            Scores[:] += PB * get_score(S, Predicts + SList, A)
            #print(T, Scores.T[0])
            # Update prediction scores by previous move
            PR = Map[OrgID[0], Hash2, OrgID[1], OrgID[2], OrgID[3]]
            Sum = np.sum(PR, axis=0)
            Predicts[:] = (np.max((Sum >= self.G) * (PR >= Sum * self.R + self.RG) * (SList + 1), axis=0) - 1) % (S + 1)

        self.B = np.random.choice(S)
        if self.J > 0:
            self.J -= 1
        else:
            sc = np.where(self.Predicts < S, self.Scores / (self.Attempts + 5), 0).ravel()
            idx = np.argmax(sc)
            if sc[idx] > self.Threshold:
                self.Scores.ravel()[idx] -= 1/3
                Raw = self.Predicts.ravel()
                L = len(Raw)
                p = None
                s = 0
                if PR is not None:
                    p = PR.ravel().reshape((3,-1))[:, idx % L]
                    s = np.sum(p)
                if s > 0 and np.random.choice(3) > 3:
                    p /= s
                    self.B = (np.random.choice(S, p=p) + idx // L) % S
                    parts = self.split_idx(idx)
                    if self.verbose: print(T, f'Weighted {parts[0]+self.Dmin}: {self.HText[parts[1]]}-{self.HText[parts[2]]}+{parts[3]}', p, self.B)
                else:
                    self.B = (Raw[idx % L] + idx // L) % S
                    parts = self.split_idx(idx)
                    if self.verbose: print(T, f'Direct {parts[0]+self.Dmin}: {self.HText[parts[1]]}-{self.HText[parts[2]]}+{parts[3]}', self.Scores.ravel()[idx], self.B)
                self.J = int(math.sqrt(secrets.randbelow(self.J2)))
        return self.B


class _SubmissionV12:
    K = 20
    def __init__(self, verbose=False):
        self.B = 0
        # Jitter - steps before next non-random move
        self.Jmax = 2
        self.J2 = (self.Jmax+1)**2
        self.J = self.Jmax - int(math.sqrt(secrets.randbelow(self.J2)))
        # Depth - number of previous steps taken into consideration
        self.Dmin = 1
        self.Dmax = 3
        self.DL = self.Dmax-self.Dmin+1
        self.HL = 3
        self.HText = ['Opp',  'Me', 'Score']
        self.Depth = np.arange(self.DL)
        self.Hash = np.zeros((self.HL, self.DL), dtype=int)
        self.G = 2
        self.R = 0.4
        self.RG = (1-self.R) * self.G
        self.Threshold = 0.4
        
    def split_idx(self, idx):
        d = idx % self.DL
        idx //= self.DL
        h2 = idx % self.HL
        idx //= self.HL
        h1 = idx % self.HL
        idx //= self.HL
        return d, h1, h2, idx
    
    def next_action(self, T, A, S, B):
        self.B = B
        B, HL, DL, Dmin, Dmax = self.B, self.HL, self.DL, self.Dmin, self.Dmax
        SD = S**self.DL
        PR = None
        if T == 0:
            self.Map = np.zeros((S, SD**2, HL, HL, DL))
            self.SList = np.arange(S)[:,None,None,None]
            self.Predicts = np.full((HL, HL, DL), S, dtype=int)
            self.Attempts = np.zeros((HL, HL, DL), dtype=int)
            self.Scores = np.zeros((S, HL, HL, DL))
            self.OrgID = np.ogrid[:S, :HL, :HL, :DL]
            self.Hash2 = self.Hash[None,:] + SD*self.Hash[:,None]
        else:
            C = get_score(S, A, B) + 1
            ABC = np.array([A, B, C])[:,None]
            Depth, Hash, Hash2, Map, SList, OrgID, Predicts, Attempts, Scores = self.Depth, self.Hash, self.Hash2, self.Map, self.SList, self.OrgID, self.Predicts, self.Attempts, self.Scores
            # Update Moves Map by previous move and previous Hash
            Map *= 0.992
            Map[OrgID[0], Hash2, OrgID[1], OrgID[2], OrgID[3]] += (T > Depth + Dmin) * (SList == A)
            # Update Hash by previous move
            Hash[:] //= S
            Hash[:] += ABC[:HL] * S**Depth
            Hash2[:] = Hash[None,:] + SD*Hash[:,None]
            
            # Update prediction scores by previous move
            PB = Predicts < S
            Attempts[:] = Attempts + PB
            Scores[:] += PB * get_score(S, Predicts + SList, A)
            #print(T, Scores.T[0])
            # Update prediction scores by previous move
            PR = Map[OrgID[0], Hash2, OrgID[1], OrgID[2], OrgID[3]]
            Sum = np.sum(PR, axis=0)
            Predicts[:] = (np.max((Sum >= self.G) * (PR >= Sum * self.R + self.RG) * (SList + 1), axis=0) - 1) % (S + 1)

        self.B = secrets.randbelow(S)
        if self.J > 0:
            self.J -= 1
        else:
            sc = np.where(self.Predicts < S, self.Scores / (self.Attempts + 3), 0).ravel()
            idx = np.argmax(sc)
            if sc[idx] > self.Threshold:
                Raw = self.Predicts.ravel()
                L = len(Raw)
                #parts = self.split_idx(idx)
                p = None
                s = 0
                if PR is not None:
                    p = PR.ravel().reshape((3,-1))[:, idx % L]
                    s = np.sum(p)
                if s > 0:
                    p /= s
                    self.B = (np.random.choice(S, p=p) + idx // L) % S
                    #print(T, f'Weighted {parts[0]+self.Dmin}: {self.HText[parts[1]]}-{self.HText[parts[2]]}', p, self.B)
                else:
                    self.B = (Raw[idx % L] + idx // L) % S
                    #print(T, f'Direct {parts[0]+self.Dmin}: {self.HText[parts[1]]}-{self.HText[parts[2]]}+{parts[3]}', self.Scores.ravel()[idx], self.B)
                self.J = self.Jmax - int(math.sqrt(secrets.randbelow(self.J2)))
        return self.B


class HPSDojoStrategy(BaseAtomicStrategy):
  def __init__(self, version=0):
    if version == 0:
      self.submission = _Submission(verbose=False)
    elif version == 12:
      self.submission = _SubmissionV12(verbose=False)

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
