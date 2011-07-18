import py.test
from abjad.tools.quantizationtools import QEvent


def test_quantizationtools_QEvent___eq___01( ):

   assert QEvent(0, 10, None) == QEvent(0, 10, None)
   assert QEvent(0, 10, None) != QEvent(0, 10, 0)
   assert QEvent(0, 10, None) != QEvent(0, 11, None)
   assert QEvent(0, 10, None) != QEvent(1, 10, None)
