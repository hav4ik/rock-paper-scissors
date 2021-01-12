from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *
from kumoko.strategies.rfind import RFindStrategy
from kumoko.strategies.decision_tree import DecisionTreeStrategy
from kumoko.strategies.hps_dojo_agent import HPSDojoStrategy
from kumoko.strategies.testing_pls_ignore import TestingPlsIgnoreStrategy


class RFindOnlyV1:
  """Only Rfind, nothing else!
  """
  @staticmethod
  def strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 35, 20, 10]
    sources = ['his', 'our', 'dna']
    for limit in limits:
      for source in sources:
        strategies.extend(
            generate_meta_strategy_pair(RFindStrategy,
                                       *(limit, source)))
    return strategies

  @staticmethod
  def scoring_funcs():
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


class FourStratsV1:
  """
  Contains 4 type of strategies:
  - RFind (with 4 windows and 3 sources)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 35, 20, 10]
    sources = ['his', 'our', 'dna']
    for limit in limits:
      for source in sources:
        strategies.extend(
            generate_meta_strategy_pair(RFindStrategy,
                                       *(limit, source)))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

    # # Add HPS Dojo strategies
    # strategies.extend(
    #     generate_meta_strategy_pair(HPSDojoStrategy))

    # # Add testing please ignore strategies
    # strategies.extend(
    #     generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    return strategies

  @staticmethod
  def scoring_funcs():
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


ENSEMBLES = {
  'rfind_v1': RFindOnlyV1,
  '4_strats_v1': FourStratsV1,
}
