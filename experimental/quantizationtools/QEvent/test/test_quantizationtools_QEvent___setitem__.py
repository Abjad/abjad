import py.test
from experimental.quantizationtools import QEvent


def test_quantizationtools_QEvent___setitem___01():
    '''QEvents are immutable.'''

    q = QEvent(0, 0)
    py.test.raises(AttributeError, 'q.ding = "dong"')
