from sklearn.tree import DecisionTreeClassifier
import numpy as np
from kumoko.kumoko_base import *


class DecisionTreeStrategy(BaseAtomicStrategy):
  def __init__(self):
    self.step = 0

  def construct_local_features(self, rollouts):
      features = np.array([[step % k for step in rollouts['steps']] for k in (2, 3, 5)])
      features = np.append(features, rollouts['steps'])
      features = np.append(features, rollouts['actions'])
      features = np.append(features, rollouts['opp-actions'])
      return features

  def construct_global_features(self, rollouts):
      features = []
      for key in ['actions', 'opp-actions']:
          for i in range(3):
              actions_count = np.mean([r == i for r in rollouts[key]])
              features.append(actions_count)
      return np.array(features)

  def construct_features(self, short_stat_rollouts, long_stat_rollouts):
      lf = self.construct_local_features(short_stat_rollouts)
      gf = self.construct_global_features(long_stat_rollouts)
      features = np.concatenate([lf, gf])
      return features

  def predict_opponent_move(self, train_data, test_sample):
      classifier = DecisionTreeClassifier(random_state=42)
      classifier.fit(train_data['x'], train_data['y'])
      return classifier.predict(test_sample)

  def update_rollouts_hist(self, rollouts_hist, last_move, opp_last_action):
      rollouts_hist['steps'].append(last_move['step'])
      rollouts_hist['actions'].append(last_move['action'])
      rollouts_hist['opp-actions'].append(opp_last_action)
      return rollouts_hist

  def warmup_strategy(self, his_last_move):
      action = int(np.random.randint(3))
      if self.step == 0:
          self.last_move = {'step': 0, 'action': action}
          self.rollouts_hist = {'steps': [], 'actions': [], 'opp-actions': []}
      else:
          self.rollouts_hist = self.update_rollouts_hist(self.rollouts_hist, self.last_move, his_last_move)
          self.last_move = {'step': self.step, 'action': action}
      return int(action)

  def init_training_data(self, rollouts_hist, k):
      for i in range(len(rollouts_hist['steps']) - k + 1):
          short_stat_rollouts = {key: rollouts_hist[key][i:i+k] for key in rollouts_hist}
          long_stat_rollouts = {key: rollouts_hist[key][:i+k] for key in rollouts_hist}
          features = self.construct_features(short_stat_rollouts, long_stat_rollouts)
          self.data['x'].append(features)
      test_sample = self.data['x'][-1].reshape(1, -1)
      self.data['x'] = self.data['x'][:-1]
      self.data['y'] = rollouts_hist['opp-actions'][k:]
      return self.data, test_sample

  def __call__(self, history):
      if len(history) != 0:
        his_last_move = MOVE_TO_NUM[history.his_moves[-1]]
        self.last_move = {'step': self.step, 'action': MOVE_TO_NUM[history.our_moves[-1]]}
      else:
        his_last_move = random.randint(0,2)

      # hyperparameters
      k = 5
      min_samples = 25
      if self.step == 0:
          self.data = {'x': [], 'y': []}
      # if not enough self.data -> randomize

      if self.step <= min_samples + k:
          action = self.warmup_strategy(his_last_move)
          self.step += 1
          return NUM_TO_MOVE[action]

      # update statistics
      self.rollouts_hist = self.update_rollouts_hist(self.rollouts_hist, self.last_move, his_last_move)
      # update training self.data
      if len(self.data['x']) == 0:
          self.data, self.test_sample = self.init_training_data(self.rollouts_hist, k)
      else:
          short_stat_rollouts = {key: self.rollouts_hist[key][-k:] for key in self.rollouts_hist}
          features = self.construct_features(short_stat_rollouts, self.rollouts_hist)
          self.data['x'].append(self.test_sample[0])
          self.data['y'] = self.rollouts_hist['opp-actions'][k:]
          self.test_sample = features.reshape(1, -1)

      # predict opponents move and choose an action
      next_opp_action_pred = self.predict_opponent_move(self.data, self.test_sample)
      action = int((next_opp_action_pred + 1) % 3)
      self.last_move = {'step': self.step, 'action': action}
      self.step += 1

      return NUM_TO_MOVE[action]
