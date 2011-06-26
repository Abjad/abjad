from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_intervals import _make_test_intervals


def test_IntervalTree___iter____01( ):
   blocks = _make_test_intervals( )
   tree = IntervalTree(blocks)
   for e in enumerate(tree):
      assert blocks[e[0]] == e[1]    
