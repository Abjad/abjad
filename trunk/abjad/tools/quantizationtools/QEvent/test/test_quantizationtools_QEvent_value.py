import py.test
from abjad.tools.quantizationtools import QEvent


def test_quantizationtools_QEvent_value_01( ):

   q = QEvent(0, 1, 0)
   assert q.value == 0
