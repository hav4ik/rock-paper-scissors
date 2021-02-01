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
from kumoko.strategies.centrifugal_bumblepuppy import CentrifugalBumblepuppy4
from kumoko.strategies.anti_trivial import AntiTrivialStrategy
from kumoko.strategies.testimono import TestimonoStrategy
from kumoko.strategies.statistical_prediction import StatisticalPredictionStrategy
from kumoko.strategies.geometry import GeometryV4Strategy
from kumoko.strategies.iocane_powder import IocanePowderStrategy
from kumoko.strategies.are_you_a_lucker import AreYouALuckerStrategy
from kumoko.strategies.geobot_beater import GeobotBeaterStrategy
from kumoko.strategies.greenberg import GreenbergStrategy
from kumoko.strategies.rps_meta_fix import RPSMetaFixStrategy


class Testing:
  @staticmethod
  def generate():
    strategies = []
    limits = [10, 20]
    # for limit in limits:
    #   strategies.extend(
    #       generate_meta_strategy_pair(
    #         RFindStrategy,
    #         limit=limit,
    #         src='his',
    #         shenanigans=True,
    #       ))

    # sources = ['his', 'our', 'dna']
    # strategies.extend(
    #     generate_meta_strategy_pair(
    #       WrappedRFindStrategy,
    #       limits=limits,
    #       sources=sources,
    #       shenanigans=False))

    strategies.extend(
        generate_meta_strategy_pair(
          IocanePowderStrategy))

    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

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


class StatisticalPrediction:
  """Only Stat Prediction, nothing else!
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []
    strategies.extend(
        generate_meta_strategy_pair(
          StatisticalPredictionStrategy))
    do_rotations = [True for _ in strategies]
    return strategies, do_rotations


class GeometryV4:
  """Only Geometry, nothing else!
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []
    strategies.extend(
        generate_meta_strategy_pair(
          GeometryV4Strategy, mirroring=False,
          alpha=0.5))
    do_rotations = [False for _ in strategies]
    assert len(strategies) == 1
    return strategies, do_rotations


class GeometryV4Augmented:
  """Only Geometry, nothing else!
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []
    strategies.extend(
        generate_meta_strategy_pair(
          GeometryV4Strategy,
          alpha=0.1))
    do_rotations = [True for _ in strategies]
    return strategies, do_rotations


class VanillaGeoBeater:
  """Only geobeater, nothing else!
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []
    strategies.extend(
        generate_meta_strategy_pair(GeobotBeaterStrategy))
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


class FiveStratsV3a:
  """
  Contains 5 type of strategies:
  - RFind (with 4 windows and 3 sources)
  - DecisionTree
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - RPS Geometry V4
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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(
          GeometryV4Strategy))

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


class SevenStratsV1a:
  """
  Contains 6 type of strategies:
  - Centrifugal Bumblepuppy 16+H
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

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class SevenStratsV1b:
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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class EightStratsV1a:
  """
  Contains 8 type of strategies:
  - Centrifugal Bumblepuppy 16+H
  - DecisionTree
  - DecisionTreeV10
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
  - RPS Geometry
  - Iocane Powder (IOU Fight uuu)
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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # Add Iocaine Powder strategy
    strategies.extend(
        generate_meta_strategy_pair(IocanePowderStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class EightStratsV1b:
  """
  Contains 8 type of strategies:
  - RFind family (with 3 limits and 3 sources)
  - DecisionTree
  - DecisionTreeV10
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
  - RPS Geometry
  - Iocane Powder (IOU Fight uuu)
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

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # Add Iocaine Powder strategy
    strategies.extend(
        generate_meta_strategy_pair(IocanePowderStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class NineStratsV1a:
  """
  Contains 9 type of strategies:
  - Centrifugal Bumblepuppy 16+H
  - RFind family (with 3 limits and 3 sources)
  - DecisionTree
  - DecisionTreeV10
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
  - RPS Geometry
  - Iocane Powder (IOU Fight uuu)
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

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # Add Iocaine Powder strategy
    strategies.extend(
        generate_meta_strategy_pair(IocanePowderStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class NineStratsV2a:
  """
  Contains 9 type of strategies:
  - Centrifugal Bumblepuppy 16+H
  - Centrifugal Bumblepuppy 4
  - DecisionTree
  - DecisionTreeV10
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
  - RPS Geometry
  - Iocane Powder (IOU Fight uuu)
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy4))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # Add Iocaine Powder strategy
    strategies.extend(
        generate_meta_strategy_pair(IocanePowderStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class TenStratsV1a:
  """
  Contains 10 type of strategies:
  - Centrifugal Bumblepuppy 16+H
  - Centrifugal Bumblepuppy 4
  - DecisionTree
  - DecisionTreeV10
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
  - RPS Geometry
  - Iocane Powder (IOU Fight uuu)
  - Are you a lucker?
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy4))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # Add Iocaine Powder strategy
    strategies.extend(
        generate_meta_strategy_pair(IocanePowderStrategy))

    # Add are you a lucker strategies
    strategies.extend(
        generate_meta_strategy_pair(AreYouALuckerStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class ElevenStratsV1a:
  """
  Contains 11 type of strategies:
  - Centrifugal Bumblepuppy 16+H
  - Centrifugal Bumblepuppy 4
  - DecisionTree
  - DecisionTreeV10
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
  - RPS Geometry
  - Iocane Powder (IOU Fight uuu)
  - Are you a lucker?
  - RPS Meta Fix
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy4))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # Add Iocaine Powder strategy
    strategies.extend(
        generate_meta_strategy_pair(IocanePowderStrategy))

    # Add are you a lucker strategies
    strategies.extend(
        generate_meta_strategy_pair(AreYouALuckerStrategy))

    # Add RPS Meta Fix strategies
    strategies.extend(
        generate_meta_strategy_pair(RPSMetaFixStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


class TwelveStratsV1a:
  """
  Contains 12 type of strategies:
  - Centrifugal Bumblepuppy 16+H
  - Centrifugal Bumblepuppy 4
  - DecisionTree
  - DecisionTreeV10
  - HPSDojo (from high performance notebook)
  - TestingPleaseIgnore
  - Testimono
  - RPS Geometry
  - Iocane Powder (IOU Fight uuu)
  - Are you a lucker?
  - Greenberg
  - RPS Meta Fix
  """
  @staticmethod
  def generate():
    """List of strategies (including mirror strategies)
    """
    strategies = []

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy16h))

    # Add Centrifugal Bumblepuppy 16+H (RFind based)
    strategies.extend(
        generate_meta_strategy_pair(CentrifugalBumblepuppy4))

    # Add decision tree strategies
    strategies.extend(
        generate_meta_strategy_pair(DecisionTreeStrategy))

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

    # Add RPS Geometry
    strategies.extend(
        generate_meta_strategy_pair(GeometryV4Strategy))

    # Add Iocaine Powder strategy
    strategies.extend(
        generate_meta_strategy_pair(IocanePowderStrategy))

    # Add are you a lucker strategies
    strategies.extend(
        generate_meta_strategy_pair(AreYouALuckerStrategy))

    # Add Greenberg strategies
    strategies.extend(
        generate_meta_strategy_pair(GreenbergStrategy))

    # Add RPS Meta Fix strategies
    strategies.extend(
        generate_meta_strategy_pair(RPSMetaFixStrategy))

    # By default, rotate everything
    do_rotations = [True for _ in strategies]

    # Anti Trivial
    strategies.extend(
        generate_meta_strategy_pair(
          AntiTrivialStrategy, mirroring=False))
    do_rotations.extend([False])

    return strategies, do_rotations


ENSEMBLES = {
  # Basic ensembles and single agents
  'test': Testing,
  'rfind_v1': RFindOnlyV1,
  'stat_pred': StatisticalPrediction,
  'geom_v4': GeometryV4,
  'geom_v4_aug': GeometryV4Augmented,
  'geobeater': VanillaGeoBeater,

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
  '5_strats_v3a': FiveStratsV3a,

  # Ensembles with 6 strategies
  '6_strats_v1a': SixStratsV1a,

  # Ensembles with 7 strategies
  '7_strats_v1a': SevenStratsV1a,
  '7_strats_v1b': SevenStratsV1b,

  # Ensembles with 8 strategies
  '8_strats_v1a': EightStratsV1a,
  '8_strats_v1b': EightStratsV1b,

  # Ensembles with 9 strategies
  '9_strats_v1a': NineStratsV1a,
  '9_strats_v2a': NineStratsV2a,

  # Ensembles with 10 strategies
  '10_strats_v1a': TenStratsV1a,

  # Ensembles with 11 strategies
  '11_strats_v1a': ElevenStratsV1a,

  # Ensembles with 12 strategies
  '12_strats_v1a': TwelveStratsV1a,
}
