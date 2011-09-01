from abjad import *


def test_Mark___init___01():
    '''Initialize mark from empty argument list.
    '''

    mark = marktools.Mark()
    assert isinstance(mark, marktools.Mark)


def test_Mark___init___02():
    '''Initialize mark from other mark.
    '''

    mark_1 = marktools.Mark()
    mark_2 = marktools.Mark(mark_1)

    assert isinstance(mark_1, marktools.Mark)
    assert isinstance(mark_2, marktools.Mark)
    assert mark_1 == mark_2
    assert mark_1 is not mark_2
