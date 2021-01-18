from kumoko.kumoko_base import *
from kumoko.kumoko_meta import *

from kumoko.strategies.rfind import RFindStrategy
from kumoko.strategies.rfind import WrappedRFindStrategy
from kumoko.strategies.decision_tree import DecisionTreeStrategy
from kumoko.strategies.decision_tree_v10 import DecisionTreeV10Strategy
from kumoko.strategies.hps_dojo_agent import HPSDojoStrategy
from kumoko.strategies.testing_pls_ignore import TestingPlsIgnoreStrategy
from kumoko.strategies.memory_patterns_v7 import MemoryPatternsV7Strategy
from kumoko.strategies.centrifugal_bumblepuppy import CentrifugalBumblepuppy16h


class Testing:
  @staticmethod
  def generate():
    strategies = []
    # limits = [10, 20]
    # for limit in limits:
    #   strategies.extend(
    #       generate_meta_strategy_pair(
    #         RFindStrategy,
    #         limit=limit,
    #         src='his',
    #         shenanigans=True,
    #       ))
    strategies.extend(
        generate_meta_strategy_pair(
          CentrifugalBumblepuppy16h))

    return strategies


class RFindOnlyV1:
  """Only Rfind, nothing else!
  """
  @staticmethod
  def generate():
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


class FourStratsV1a:
  """
  Contains 4 type of strategies:
  - RFind (with 4 windows and 3 sources)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate():
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


class FourStratsV1:
  """
  Contains 4 type of strategies:
  - RFind (with 4 windows and 3 sources)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate():
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


class FourStratsV2a:
  """
  Contains 4 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate():
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


class FourStratsV2b:
  """
  Contains 4 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate():
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


class FourStratsV2c:
  """
  Contains 4 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate():
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
  def generate():
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


class FourStratsV3a:
  """
  Contains 4 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate():
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
  '4_strats_v3a': FourStratsV3a,

  # Ensembles with 5 strategies
  '5_strats_v1a': FiveStratsV1a
}
