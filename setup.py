from setuptools import setup
from setuptools import find_packages


setup(name='kumoko',
      version='0.1.0',
      description='Going Meta with Kumoko in Rock-Paper-Scissors',
      author='Chan Kha Vu',
      install_requires=[
        'kaggle-environments',
        'pydash',
        'pyyaml',
      ],
      packages=find_packages())
