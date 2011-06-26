from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_intervals import _make_test_intervals
from abjad import Fraction


def test_BoundedInterval_centroid_01( ):
   intervals = _make_test_intervals( )
   for interval in intervals:
      assert interval.centroid == Fraction(interval.low + interval.high, 2)
