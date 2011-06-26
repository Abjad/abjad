from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_intervals import _make_test_intervals


def test_treetools_all_are_intervals_or_trees_or_empty_01( ):
   tree = IntervalTree([ ])
   assert all_are_intervals_or_trees_or_empty(tree)


def test_treetools_all_are_intervals_or_trees_or_empty_02( ):
   interval = BoundedInterval(0, 10)
   assert all_are_intervals_or_trees_or_empty(interval)


def test_treetools_all_are_intervals_or_trees_or_empty_03( ):
   tree = IntervalTree([ ])
   other_tree = IntervalTree([BoundedInterval(2001, 2010)])
   interval = BoundedInterval(0, 10)
   assert all_are_intervals_or_trees_or_empty([tree, other_tree, interval])


def test_treetools_all_are_intervals_or_trees_or_empty_04( ):
   tree = IntervalTree([ ])
   other_tree = IntervalTree([BoundedInterval(2001, 2010)])
   interval = BoundedInterval(0, 10)
   assert all_are_intervals_or_trees_or_empty([tree, [[other_tree], interval], [ ]])


def test_treetools_all_are_intervals_or_trees_or_empty_05( ):
   tree = IntervalTree([ ])
   other_tree = IntervalTree([BoundedInterval(2001, 2010)])
   interval = BoundedInterval(0, 10)
   assert all_are_intervals_or_trees_or_empty([tree, [[other_tree], interval], [ ], [[interval]]])


def test_treetools_all_are_intervals_or_trees_or_empty_06( ):
   tree = IntervalTree([ ])
   other_tree = IntervalTree([BoundedInterval(2001, 2010)])
   interval = BoundedInterval(0, 10)
   assert not all_are_intervals_or_trees_or_empty([tree, [[other_tree], interval], [ ], [2]])


def test_treetools_all_are_intervals_or_trees_or_empty_07( ):
   assert all_are_intervals_or_trees_or_empty([ ])



