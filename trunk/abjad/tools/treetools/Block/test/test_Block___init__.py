from abjad.tools.treetools import *
import py.test


def test_Block___init___01( ):
   '''Block duration must be at least zero.'''
   py.test.raises(AssertionError,
      "b = Block(0, -1, 'this should fail.')")
