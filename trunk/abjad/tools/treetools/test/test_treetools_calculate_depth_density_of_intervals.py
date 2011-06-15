from abjad import Fraction
from abjad.tools.treetools import *
import py.test


def test_treetools_calculate_depth_density_of_intervals_01( ):
   a = BoundedInterval(0, 10)
   assert calculate_depth_density_of_intervals(a) == 1


def test_treetools_calculate_depth_density_of_intervals_02( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(20, 30)
   assert calculate_depth_density_of_intervals([a, b]) == Fraction(2, 3)


def test_treetools_calculate_depth_density_of_intervals_03( ):
   assert calculate_depth_density_of_intervals([ ]) == 0
