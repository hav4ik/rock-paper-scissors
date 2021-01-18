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
from kumoko.strategies.anti_trivial import AntiTrivialStrategy
from kumoko.strategies.testimono import TestimonoStrategy


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

    do_rotations = [True for _ in strategies]
    return strategies, do_rotations


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
    do_rotations = [True for _ in strategies]
    return strategies, do_rotations


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

    do_rotations = [True for _ in strategies]
    return strategies, do_rotations


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

    do_rotations = [True for _ in strategies]
    return strategies, do_rotations


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

    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


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

    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


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

    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class FourStratsV3a:
  """
  Contains 4 type of strategies:
  - Centrifugal Bumblepuppy 16+H
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class FourStratsV3b:
  """
  Contains 4 type of strategies:
  - Centrifugal Bumblepuppy 16+H
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies, do_rotations = [], []

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(
          CentrifugalBumblepuppy16h,
          mirroring=False))
    do_rotations.extend([False])

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))
    do_rotations.extend([True, True])

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))
    do_rotations.extend([True, True])

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))
    do_rotations.extend([True, True])

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class FourStratsV3c:
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

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeV10Strategy))

    # Add HPS Dojo strategies
    strategies.extend(
        generate_meta_strategy_pair(HPSDojoStrategy))

    # Add testing please ignore strategies
    strategies.extend(
        generate_meta_strategy_pair(TestingPlsIgnoreStrategy))

    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


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

    do_rotations = [True for _ in strategies]
    return strategies, do_rotations


class FiveStratsV2b:
  """
  Contains 5 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
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

    # Add testimono strategy
    strategies.extend(
        generate_meta_strategy_pair(TestimonoStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class FiveStratsV2c:
  """
  Contains 5 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
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

    # Add testimono strategy
    strategies.extend(
        generate_meta_strategy_pair(TestimonoStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class FiveStratsV2d:
  """
  Contains 5 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Memory Patterns V7
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

    # Add testimono strategy
    strategies.extend(
        generate_meta_strategy_pair(MemoryPatternsV7Strategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class SixStratsV1a:
  """
  Contains 6 type of strategies:
  - RFindWrapped (with 4 windows and 3 sources wrapped inside a Kumoko)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
  - Memory Patterns V7
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

    # Add testimono strategy
    strategies.extend(
        generate_meta_strategy_pair(TestimonoStrategy))

    # Add memory patterns v7
    strategies.extend(
        generate_meta_strategy_pair(MemoryPatternsV7Strategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


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
  '4_strats_v3b': FourStratsV3b,
  '4_strats_v3c': FourStratsV3c,

  # Ensembles with 5 strategies
  '5_strats_v1a': FiveStratsV1a,
  '5_strats_v2b': FiveStratsV2b,
  '5_strats_v2c': FiveStratsV2c,

  # Ensembles with 6 strategies
  '6_strats_v1a': SixStratsV1a,
}
