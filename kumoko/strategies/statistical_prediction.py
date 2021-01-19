import random
import pydash
from collections import Counter

from kumoko.kumoko_base import *
from kumoko.kumoko import Kumoko


class StatisticalPredictionStrategy(BaseAtomicStrategy):
  def __init__(self):
    super().__init__()
    # Create a small amount of starting history
    self.history = {
        "guess":      [0,1,2],
        "prediction": [0,1,2],
        "expected":   [0,1,2],
        "action":     [1,2,0],
        "opponent":   [0,1],
        "rotn":       [0,1],
    }

  # observation   =  {'step': 1, 'lastOpponentAction': 1}
  # configuration =  {'episodeSteps': 1000, 'agentTimeout': 60, 'actTimeout': 1, 'runTimeout': 1200, 'isProduction': False, 'signs': 3}
  def __call__(self, external_history):    
    if len(external_history) > 0:
      self.history['action'].append(MOVE_TO_NUM[external_history.our_moves[-1]])

    actions          = list(range(3))  # [0,1,2]
    last_action      = self.history['action'][-1]
    prev_opp_action  = self.history['opponent'][-1]
    if len(external_history) > 0:
      opponent_action  = MOVE_TO_NUM[external_history.his_moves[-1]]
    else:
      opponent_action = 2
    rotn             = (opponent_action - prev_opp_action) % 3
  
    self.history['opponent'].append(opponent_action)
    self.history['rotn'].append(rotn)
    
    # Make weighted random guess based on the complete move history, weighted towards relative moves based on our last action 
    move_frequency   = Counter(self.history['rotn'])
    action_frequency = Counter(zip(self.history['action'], self.history['rotn'])) 
    move_weights     = [   move_frequency.get(n, 1) 
                         + action_frequency.get((last_action,n), 1) 
                         for n in range(3) ] 
    guess            = random.choices( population=actions, weights=move_weights, k=1 )[0]
    
    # Compare our guess to how our opponent actually played
    guess_frequency  = Counter(zip(self.history['guess'], self.history['rotn']))
    guess_weights    = [ guess_frequency.get((guess,n), 1) 
                         for n in range(3) ]
    prediction       = random.choices( population=actions, weights=guess_weights, k=1 )[0]
  
    # Repeat, but based on how many times our prediction was correct
    pred_frequency   = Counter(zip(self.history['prediction'], self.history['rotn']))
    pred_weights     = [ pred_frequency.get((prediction,n), 1) 
                         for n in range(3) ]
    expected         = random.choices( population=actions, weights=pred_weights, k=1 )[0]
  
    
    # Slowly decay to 50% pure randomness as the match progresses
    pure_random_chance = len(external_history) / (1000 * 2)
    if random.random() < pure_random_chance:
        action = random.randint(0, 3-1)
        is_pure_random_chance = True
    else:
        # Play the +1 counter move
        # action = (expected + 1) % configuration.signs                  # without rotn
        action = (opponent_action + expected + 1) % 3  # using   rotn
        is_pure_random_chance = False
    
    # Persist state
    self.history['guess'].append(guess)
    self.history['prediction'].append(prediction)
    self.history['expected'].append(expected)
  
    # Print debug information
    # print('step                      = ', len(external_history))
    # print('opponent_action           = ', opponent_action)
    # print('guess,      move_weights  = ', guess,      move_weights)
    # print('prediction, guess_weights = ', prediction, guess_weights)
    # print('expected,   pred_weights  = ', expected,   pred_weights)
    # print('action                    = ', action)
    # print('pure_random_chance        = ', f'{100*pure_random_chance:.2f}%', is_pure_random_chance)
    # print()
    
    return NUM_TO_MOVE[action]
