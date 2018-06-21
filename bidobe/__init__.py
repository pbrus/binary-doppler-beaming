"""
Bidobe
======

Bidobe is an acronym of BInary DOppler BEaming

This package provides tools to:
  1. solve a two body problem
  2. calculate photometric doppler beaming
  3. represent graphically determined parameters

"""
from . import astunit
from . import dobe
from . import orbit
from . import plotorb

__all__ = ["orbit", "astunit", "plotorb", "dobe"]
__version__ = '0.1.0'
