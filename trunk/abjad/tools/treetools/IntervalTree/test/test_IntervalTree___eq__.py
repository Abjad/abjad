from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_IntervalTree___eq___01( ):
   a = IntervalTree(_make_test_blocks( ))
   b = IntervalTree(_make_test_blocks( ))
   assert a == b


def test_IntervalTree___eq___02( ):
   a = IntervalTree(_make_test_blocks( ))
   b = IntervalTree(_make_test_blocks( )[:-1])
   assert a != b


def test_IntervalTree___eq___03( ):
   a = IntervalTree([ ])
   b = IntervalTree([ ])
   assert a == b

