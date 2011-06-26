from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_intervals import _make_test_intervals   
from abjad import Fraction


def test_treetools_calculate_mean_attack_of_intervals_01( ):
   tree = IntervalTree(_make_test_intervals( ))
   attack = calculate_mean_attack_of_intervals(tree)
   assert attack == Fraction(sum([x.low for x in tree]), len(tree))


def test_treetools_calculate_mean_attack_of_intervals_02( ):
   tree = IntervalTree([ ])
   attack = calculate_mean_attack_of_intervals(tree)
   assert attack is None          
