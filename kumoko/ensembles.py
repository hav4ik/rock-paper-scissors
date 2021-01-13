from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *

from kumoko.strategies.rfind import RFindStrategy
from kumoko.strategies.rfind import WrappedRFindStrategy
from kumoko.strategies.decision_tree import DecisionTreeStrategy
from kumoko.strategies.decision_tree_v10 import DecisionTreeV10Strategy
from kumoko.strategies.hps_dojo_agent import HPSDojoStrategy
from kumoko.strategies.testing_pls_ignore import TestingPlsIgnoreStrategy
from kumoko.strategies.memory_patterns_v7 import MemoryPatternsV7Strategy


class Testing:
  @staticmethod
  def generate_strategies():
    strategies = []
    limits = [10, 20]
    for limit in limits:
      strategies.extend(
          generate_meta_strategy_pair(
            RFindStrategy,
            limit=limit,
            src='his',
            shenanigans=True,
          ))
    return strategies

  @staticmethod
  def generate_scoring_funcs():
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


class RFindOnlyV1:
  """Only Rfind, nothing else!
  """
  @staticmethod
  def generate_strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 20, 10]
    sources = ['his', 'our', 'dna']
    for limit in limits:
      for source in sources:
        strategies.extend(
            generate_meta_strategy_pair(
              RFindStrategy,
              limit=limit,
              src=source,
              shenanigans=True,
            ))
    return strategies

  @staticmethod
  def generate_scoring_funcs():
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


class FourStratsV1a:
  """
  Contains 4 type of strategies:
  - RFind (with 4 windows and 3 sources)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate_strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 20, 10]
    sources = ['his', 'our', 'dna']
    for limit in limits:
      for source in sources:
        strategies.extend(
            generate_meta_strategy_pair(
              RFindStrategy,
              limit=limit,
              src=source,
              shenanigans=False,
            ))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeV10Strategy))

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    return strategies

  @staticmethod
  def generate_scoring_funcs():
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
  def generate_strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 20, 10]
    sources = ['his', 'our', 'dna']
    for limit in limits:
      for source in sources:
        strategies.extend(
            generate_meta_strategy_pair(
              RFindStrategy,
              limit=limit,
              src=source,
              shenanigans=False,
            ))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    return strategies

  @staticmethod
  def generate_scoring_funcs():
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


class FourStratsV2a:
  """
  Contains 4 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate_strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 20, 10]
    sources = ['his', 'our', 'dna']

    strategies.extend([
        generate_meta_strategy_pair(
          WrappedRFindStrategy,
          limits=limits,
          sources=sources,
          shenanigans=False)[0]])

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    return strategies

  @staticmethod
  def generate_scoring_funcs():
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


class FourStratsV2b:
  """
  Contains 4 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate_strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 20, 10]
    sources = ['his', 'our', 'dna']

    strategies.extend(
        generate_meta_strategy_pair(
          WrappedRFindStrategy,
          limits=limits,
          sources=sources,
          shenanigans=False))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    return strategies

  @staticmethod
  def generate_scoring_funcs():
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


class FourStratsV2c:
  """
  Contains 4 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate_strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 20, 10]
    sources = ['his', 'our', 'dna']

    strategies.extend(
        generate_meta_strategy_pair(
          WrappedRFindStrategy,
          limits=limits,
          sources=sources,
          shenanigans=False))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeV10Strategy))

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    return strategies

  @staticmethod
  def generate_scoring_funcs():
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


class FiveStratsV1a:
  """
  Contains 5 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTreeV10
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - MemoryPatternsV7
  """
  @staticmethod
  def generate_strategies():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add RFind strategies (2 meta-strategies P0 and P'0 for each)
    limits=[50, 20, 10]
    sources = ['his', 'our', 'dna']
    strategies.extend(
        generate_meta_strategy_pair(
          WrappedRFindStrategy,
          limits=limits,
          sources=sources,
          shenanigans=False))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeV10Strategy))

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    # Add memory pattern strategies
    strategies.extend(
        generate_meta_strategy_pair(MemoryPatternsV7Strategy))

    return strategies

  @staticmethod
  def generate_scoring_funcs():
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
  # Basic ensembles
  'test': Testing,
  'rfind_v1': RFindOnlyV1,

  # Ensembles with 4 strategies
  '4_strats_v1': FourStratsV1,
  '4_strats_v1a': FourStratsV1a,
  '4_strats_v2a': FourStratsV2a,
  '4_strats_v2b': FourStratsV2b,
  '4_strats_v2c': FourStratsV2c,

  # Ensembles with 5 strategies
  '5_strats_v1a': FiveStratsV1a
}
