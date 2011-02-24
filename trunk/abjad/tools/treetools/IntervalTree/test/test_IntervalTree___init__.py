from abjad.tools.treetools import *


def test_IntervalTree___init___01( ):
   '''IntervalTree can be initialized without arguments.'''
   tree = IntervalTree([ ])

def tree_IntervalTree___init___02( ):
   '''IntervalTree can be instantiated from a single BoundedInterval.'''
   a = BoundedInterval(0, 10)
   tree = IntervalTree(a)
   assert a in tree

def tree_IntervalTree___init___03( ):
   '''IntervalTree can be instantiated from a single IntervalTree.'''
   a = BoundedInterval(0, 10)
   t = IntervalTree(a)
   tree = IntervalTree(t)
   assert a in tree

def test_IntervalTree___init___04( ):
   '''IntervalTree can be initialized from a list of BoundedIntervals.'''
   a = BoundedInterval(0, 10, 'a')
   b = BoundedInterval(5, 15, 'b')
   c = BoundedInterval(10, 25, 'c')
   tree = IntervalTree([a, b, c])
   assert all([block in tree for block in [a, b, c]])

def test_IntervalTree___init___05( ):
   '''IntervalTree can be initialized from a list of Blocks.'''
   a = Block(0, 10, 'a')
   b = Block(5, 15, 'b')
   c = Block(10, 5, 'c')
   tree = IntervalTree([a, b, c])

def test_IntervalTree___init___06( ):
   '''IntervalTree recursively flattens its input argument,
   allowing instantiation from any nested collection of
   BoundedIntervals and / or trees.'''
   a = BoundedInterval(0, 10)
   b = BoundedInterval(5, 15)
   t = IntervalTree([a, b])
   c = BoundedInterval(21, 23)
   d = Block(2001, 9)
   tree = IntervalTree([a, b, [c, d], [[t]]])
   assert [x.signature for x in tree] == \
      [(0, 10), (0, 10), (5, 15), (5, 15), (21, 23), (2001, 2010)]
