import os
import random
import numpy as np
from typing import List, Dict
from sklearn.tree import DecisionTreeClassifier
from kumoko.kumoko_base import *


def get_winstats(history) -> Dict[str,int]:
    total = len(history['action'])
    assert len(history['action']) <= len(history['opponent'])
    wins = 0
    draw = 0
    loss = 0
    for n in range(total):
        if   history['action'][n] == history['opponent'][n] + 1: wins +=  1
        elif history['action'][n] == history['opponent'][n]:     draw +=  1
        elif history['action'][n] == history['opponent'][n] - 1: loss +=  1
    return { "wins": wins, "draw": draw, "loss": loss }

def get_winrate(history):
    winstats = get_winstats(history)
    winrate  = winstats['wins'] / (winstats['wins'] + winstats['loss']) if (winstats['wins'] + winstats['loss']) else 0
    return winrate

# NOTE: adding statistics causes the DecisionTree to make random moves
def get_statistics(values) -> List[float]:
    values = np.array(values)
    return [
        np.count_nonzero(values == n) / len(values)
        if len(values) else 0.0
        for n in [0,1,2]
    ]


class DecisionTreeV10Strategy(BaseAtomicStrategy):
  def __init__(self):
    # Initialize starting history
    self.history = {
        "step":        [],
        "prediction1": [],
        "prediction2": [],
        "expected":    [],
        "action":      [],
        "opponent":    [],
    }

  # observation   =  {'step': 1, 'lastOpponentAction': 1}
  # configuration =  {'episodeSteps': 10, 'agentTimeout': 60, 'actTimeout': 1, 'runTimeout': 1200, 'isProduction': False, 'signs': 3}
  def __call__(self, external_history, window=6, stages=3, random_freq=0.25, max_samples=1000, warmup_period=0):
      warmup_period   = warmup_period  # if os.environ.get('KAGGLE_KERNEL_RUN_TYPE','') != 'Interactive' else 0
      models          = [ None ] + [ DecisionTreeClassifier() ] * stages
      actions         = list(range(3))  # [0,1,2]
      step            = len(external_history)
      last_action     = MOVE_TO_NUM[external_history.our_moves[-1]] if len(external_history) else random.randint(0,2)
      opponent_action = MOVE_TO_NUM[external_history.his_moves[-1]] if step > 0   else random.randint(0,2)

      # if step == 0:
      #   self.history = {
      #       "step":        [],
      #       "prediction1": [],
      #       "prediction2": [],
      #       "expected":    [],
      #       "action":      [],
      #       "opponent":    [],
      #   }

      if step > 0:
          self.history['opponent'].append(opponent_action)
          self.history['action'].append(last_action)

      winrate  = get_winrate(self.history)
      winstats = get_winstats(self.history)

      # Set default values
      prediction1 = random.randint(0,2)
      prediction2 = random.randint(0,2)
      prediction3 = random.randint(0,2)
      expected    = random.randint(0,2)

      # We need at least some turns of self.history for DecisionTreeClassifier to work

      # print('step:', step)
      # print('len ext:', len(external_history))
      # print('  OA0', len(self.history['opponent']), len(self.history['action']))
      # print('  OP1', len(self.history['opponent']), len(self.history['prediction1']))
      # print('  OP2', len(self.history['opponent']), len(self.history['prediction2']))
      # print('  OA0', len(self.history['opponent']), len(self.history['expected']))

      if step >= window + stages:
          if stages >= 1:
            assert len(self.history['opponent']) <= len(self.history['action'])
          if stages >= 2:
            assert len(self.history['opponent']) <= len(self.history['prediction1'])
          if stages >= 3:
            assert len(self.history['opponent']) <= len(self.history['prediction2'])

          # First we try to predict the opponents next move based on move self.history
          # TODO: create windowed self.history
          try:
              n_start = max(1, len(self.history['opponent']) - window - max_samples)
              # print('stats: ', { key: get_statistics(self.history[key]) for key in self.history.keys() })
              if stages >= 1:
                  X = np.stack([
                      np.array([
                          # get_statistics(self.history['action'][:n+window]),
                          # get_statistics(self.history['opponent'][:n-1+window]),
                          self.history['action'][n:n+window],
                          self.history['opponent'][n:n+window]
                      ]).flatten()
                      for n in range(n_start,len(self.history['opponent'])-window)
                  ])
                  Y = np.array([
                      self.history['opponent'][n+window]
                      for n in range(n_start,len(self.history['opponent'])-window)
                  ])
                  Z = np.array([
                      # get_statistics(self.history['action']),
                      # get_statistics(self.history['opponent']),
                      self.history['action'][-window+1:] + [ last_action ],
                      self.history['opponent'][-window:]
                  ]).flatten().reshape(1, -1)

                  models[1].fit(X, Y)
                  expected = prediction1 = models[1].predict(Z)[0]

              if stages >= 2:
                  # Now retrain including prediction self.history
                  X = np.stack([
                      np.array([
                          # get_statistics(self.history['action'][:n+window]),
                          # get_statistics(self.history['prediction1'][:n+window]),
                          # get_statistics(self.history['opponent'][:n-1+window]),
                          self.history['action'][n:n+window],
                          self.history['prediction1'][n:n+window],
                          self.history['opponent'][n:n+window],
                      ]).flatten()
                      for n in range(n_start,len(self.history['opponent'])-window)
                  ])
                  Y = np.array([
                      self.history['opponent'][n+window]
                      for n in range(n_start,len(self.history['opponent'])-window)
                  ])
                  Z = np.array([
                      # get_statistics(self.history['action']),
                      # get_statistics(self.history['prediction1']),
                      # get_statistics(self.history['opponent']),
                      self.history['action'][-window+1:]      + [ last_action ],
                      self.history['prediction1'][-window+1:] + [ prediction1 ],
                      self.history['opponent'][-window:]
                  ]).flatten().reshape(1, -1)

                  models[2].fit(X, Y)
                  expected = prediction2 = models[2].predict(Z)[0]

              if stages >= 3:
                  # Now retrain including prediction self.history
                  X = np.stack([
                      np.array([
                          # get_statistics(self.history['action'][:n+window]),
                          # get_statistics(self.history['prediction1'][:n+window]),
                          # get_statistics(self.history['prediction2'][:n+window]),
                          # get_statistics(self.history['opponent'][:n-1+window]),
                          self.history['action'][n:n+window],
                          self.history['prediction1'][n:n+window],
                          self.history['prediction2'][n:n+window],
                          self.history['opponent'][n:n+window],
                      ]).flatten()
                      for n in range(n_start,len(self.history['opponent'])-window)
                  ])
                  Y = np.array([
                      self.history['opponent'][n+window]
                      for n in range(n_start,len(self.history['opponent'])-window)
                  ])
                  Z = np.array([
                      # get_statistics(self.history['action']),
                      # get_statistics(self.history['prediction1']),
                      # get_statistics(self.history['prediction2']),
                      # get_statistics(self.history['opponent']),
                      self.history['action'][-window+1:]      + [ last_action ],
                      self.history['prediction1'][-window+1:] + [ prediction1 ],
                      self.history['prediction2'][-window+1:] + [ prediction2 ],
                      self.history['opponent'][-window:]
                  ]).flatten().reshape(1, -1)

                  models[3].fit(X, Y)
                  expected = prediction3 = models[3].predict(Z)[0]

          except Exception as exception:
              print('Exception:', step, exception)

      # During the warmup period, play random to get a feel for the opponent
      if (step <= max(warmup_period,window)):
          actor  = 'warmup'
          action = random.randint(0, 2)

      # # Play a purely random move occasionally, which will hopefully distort any opponent statistics
      # elif (random.random() <= random_freq):
      #     actor  = 'random'
      #     action = random_agent(observation, configuration)

      # But mostly use DecisionTreeClassifier to predict the next move
      else:
          actor  = 'DecisionTree'
          action = (expected + 1) % 3

      # Persist state
      self.history['step'].append(step)
      self.history['prediction1'].append(prediction1)
      self.history['prediction2'].append(prediction2)
      self.history['expected'].append(expected)
      # if step == 0:  # keep arrays equal length
      #     self.history['opponent'].append(random.randint(0, 2))
      return NUM_TO_MOVE[int(action)]
