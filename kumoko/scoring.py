from kumoko.kumoko_base import *


#----------------------------------------------------------
#  DLLU SCORING FUNCTION FACTORY
#----------------------------------------------------------

def get_dllu_scoring(decay=1.,
                     win_value=1.,
                     draw_value=0.,
                     lose_value=-1.,
                     drop_prob=0.,
                     drop_draw=False,
                     clip_zero=False):
  """Returns a DLLU score (daniel.lawrence.lu/programming/rps/)

  Adds 1 to previous score if we won, subtract if we lose the
  round. Previous score is multiplied by a decay parameter >0.
  Thus, if the opponent occasionally switches strategies, this
  should be able to cope.

  If a predictor loses even once, its score is reset to zero
  with some probability. This allows for much faster response
  to opponents with switching strategies.
  """
  def _scoring_func(score, our_move, his_move):
    if our_move == his_move:
      retval = decay * score + draw_value
    elif our_move == BEAT[his_move]:
      retval = decay * score + win_value
    elif our_move == CEDE[his_move]:
      retval = decay * score + lose_value

    if drop_prob > 0. and random.random() < drop_prob:
      if our_move == CEDE[his_move]:
        score = 0.
      elif drop_draw and our_move == his_move:
        score = 0.

    if clip_zero: retval = max(0., retval)
    return retval

  return _scoring_func


class StandardDlluV1:
  @staticmethod
  def generate_normal():
    """List of scoring functions
    """
    # Add DLLU's scoring methods from his blog
    # https://daniel.lawrence.lu/programming/rps/
    dllu_scoring_configs = [
        # decay, win_val, draw_val, lose_val, drop_prob, drop_draw, clip_zero
        [ 0.80,  3.00,    0.00,     -3.00,    0.00,      False,     False    ],
        [ 0.87,  3.30,    -0.90,    -3.00,    0.00,      False,     False    ],
        [ 1.00,  3.00,    0.00,     -3.00,    1.00,      False,     False    ],
        [ 1.00,  3.00,    0.00,     -3.00,    1.00,      True,      False    ],
    ]
    scoring_funcs = [
        get_dllu_scoring(*cfg)
        for cfg in dllu_scoring_configs]
    return scoring_funcs

  @staticmethod
  def get_meta_scoring():
    """Generates a meta scoring function
    """
    meta_scoring_func = get_dllu_scoring(
        decay=0.94,
        win_value=3.0,
        draw_value=0.0,
        lose_value=-3.0,
        drop_prob=0.87,
        drop_draw=False,
        clip_zero=True)
    return meta_scoring_func

  @staticmethod
  def get_metameta_scoring():
    """Generates a metameta scoring function
    """
    metameta_scoring_func = get_dllu_scoring(
        decay=0.94,
        win_value=3.0,
        draw_value=0.0,
        lose_value=-3.0,
        drop_prob=0.87,
        drop_draw=False,
        clip_zero=True)
    return metameta_scoring_func


SCORINGS = {
  'std_dllu_v1': StandardDlluV1,
}
