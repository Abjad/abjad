from abjad.tools.quantizationtools import QEvent


def test_quantizationtools_QEvent___repr___01():
    q = QEvent(0, (3, 2, 1))
    assert repr(q) == 'QEvent(0, (1, 2, 3))'
