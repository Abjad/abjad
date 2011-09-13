from abjad import *


def test_leaftools_expr_has_leaf_with_dotted_written_duration_01():

    notes = notetools.make_notes([0], [(1, 16), (2, 16), (3, 16)])
    assert leaftools.expr_has_leaf_with_dotted_written_duration(notes)


def test_leaftools_expr_has_leaf_with_dotted_written_duration_02():

    notes = notetools.make_notes([0], [(1, 16), (2, 16), (4, 16)])
    assert not leaftools.expr_has_leaf_with_dotted_written_duration(notes)


def test_leaftools_expr_has_leaf_with_dotted_written_duration_03():
    '''Empty iterable boundary case.'''

    assert not leaftools.expr_has_leaf_with_dotted_written_duration([])
