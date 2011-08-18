from abjad.tools.quantizationtools import QEvent


def test_quantizationtools_QEvent___new___01():
    '''Basic instantiation.'''

    q = QEvent(0, None)
    q = QEvent(0, 0)
    q = QEvent(0, [0, 1, 2, 3])
