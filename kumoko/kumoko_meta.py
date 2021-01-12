import numpy as np
from kumoko.kumoko_base import *


#----------------------------------------------------------
#  GOING META WITH KUMOKO
#----------------------------------------------------------

class MetaKumoko:
  def __init__(self,
               kumoko_cls,
               kumoko_args=[],
               kumoko_kwargs={}):
    self.kumoko_1 = kumoko_cls(
        *kumoko_args, **kumoko_kwargs)
    self.kumoko_2 = kumoko_cls(
        *kumoko_args, **kumoko_kwargs)
    self.proposed_actions = []
    self.scores = 3. * np.ones(shape=(6,))
    self.scoring_func = get_dllu_scoring(
        decay=0.94,
        win_value=1.0,
        draw_value=0.0,
        lose_value=-1.0,
        drop_prob=0.87,
        drop_draw=False,
        clip_zero=True)
    self.our_last_move = None

  def next_action(self, our_last_move, his_last_move):
    """Generate next move based on opponent's last move"""

    # Force last move, so that we can use Kumoko as part of
    # a larger meta-agent
    self.our_last_move = our_last_move

    # Score the last actions
    if his_last_move is not None and \
        len(self.proposed_actions) > 0:
      for i in range(6):
        self.scores[i] = self.scoring_func(
            self.scores[i],
            self.proposed_actions[i],
            his_last_move)

    # Generate actions for Kumoko in our shoes and in the
    # shoes of opponents (i.e. 6 meta-strategies)
    a1 = self.kumoko_1.next_action(our_last_move, his_last_move)
    a2 = self.kumoko_2.next_action(his_last_move, our_last_move)
    a2 = BEAT[a2]
    self.proposed_actions = [
        a1, a2, BEAT[a1], BEAT[a2], CEDE[a1], CEDE[a2]]

    # Selecting the best action
    best_idx = np.argmax(self.scores)
    self.our_last_move = self.proposed_actions[best_idx]
    return self.our_last_move


