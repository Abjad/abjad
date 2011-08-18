import py.test
from abjad.tools.quantizationtools import QEvent


def test_quantizationtools_QEvent___eq___01():

    assert QEvent(0, None) == QEvent(0, None)
    assert QEvent(0, None) != QEvent(0, 0)
    assert QEvent(0, None) != QEvent(1, None)
    assert QEvent(0, None) != QEvent(1, 0)
