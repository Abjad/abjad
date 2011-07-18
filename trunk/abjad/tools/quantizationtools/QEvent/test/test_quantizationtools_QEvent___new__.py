import py.test
from abjad.tools.quantizationtools import QEvent


def test_quantizationtools_QEvent___new___01( ):
   '''Basic instantiation.'''

   q = QEvent(0, 1, None)
   q = QEvent(0, 1, 0)
   q = QEvent(0, 1, [0, 1, 2, 3])


def test_quantizationtools_QEvent___new___02( ):
   '''Duration must be greater than zero.'''

   py.test.raises(AssertionError, 'q = QEvent(0, 0, 0)')
