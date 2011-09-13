from abjad import *
from abjad.tools.marktools import Mark


def test_Mark___repr___01():
    '''Repr of unattached mark is evaluable.
    '''

    mark_1 = marktools.Mark()
    mark_2 = eval(repr(mark_1))

    assert isinstance(mark_1, marktools.Mark)
    assert isinstance(mark_2, marktools.Mark)
    assert mark_1 == mark_2
