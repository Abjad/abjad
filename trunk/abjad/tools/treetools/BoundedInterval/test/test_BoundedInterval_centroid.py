from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks
from fractions import Fraction


def test_BoundedInterval_centroid_01( ):
   intervals = _make_test_blocks( )
   for interval in intervals:
      assert interval.centroid == Fraction(interval.low + interval.high, 2)
