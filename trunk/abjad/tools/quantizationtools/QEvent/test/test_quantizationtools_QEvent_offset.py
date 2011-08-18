import py.test
from abjad.tools.quantizationtools import QEvent


def test_quantizationtools_QEvent_offset_01():

    q = QEvent(0, 0)
    assert q.offset == 0
