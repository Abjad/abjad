# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_logical_voice_in_expr_01():
    r'''Yield nothing when class not present.
    '''

    staff = Staff(scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    signature = inspect(staff[-1]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Rest, signature, reverse=True)
    assert len(list(iter)) == 0


def test_iterationtools_iterate_logical_voice_in_expr_02():
    r'''Yield internal nodes only.
    '''

    staff = Staff(scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    signature = inspect(staff[-1]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Tuplet, signature, reverse=True)
    assert len(list(iter)) == 3


def test_iterationtools_iterate_logical_voice_in_expr_03():
    r'''Yield exact leaves.
    '''

    staff = Staff(scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    signature = inspect(staff[-1]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Note, signature, reverse=True)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_logical_voice_in_expr_04():
    r'''Yield leaves based on names higher in inheritence hierarchy.
    '''

    staff = Staff(scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    from abjad.tools.leaftools.Leaf import Leaf
    signature = inspect(staff[-1][-1]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Leaf, signature, reverse=True)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_logical_voice_in_expr_05():
    r'''Yield Notes in two contiguous Voices with the same name.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = v2.name = 'piccolo'
    staff = Staff([v1, v2])
    signature = inspect(staff[-1]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Note, signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 4
    for e in iter:
        assert isinstance(e, Note)


def test_iterationtools_iterate_logical_voice_in_expr_06():
    r'''Yield only Notes matching the given logical voice signature.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    staff = Staff([v1, v2])
    signature = inspect(staff[-1]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Note, signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_pitch == 2


def test_iterationtools_iterate_logical_voice_in_expr_07():
    r'''Yield only Notes matching the given logical voice signature.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = 'flute'
    v2.name = 'piccolo'
    staff = Staff([v1, v2])
    signature = inspect(staff[-1]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Note, signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_pitch == 2


def test_iterationtools_iterate_logical_voice_in_expr_08():
    r'''Yield nothing when class not present.
    '''

    staff = Staff(scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    signature = inspect(staff[0]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Rest, signature)
    assert len(list(iter)) == 0


def test_iterationtools_iterate_logical_voice_in_expr_09():
    r'''Yield internal nodes only.
    '''

    staff = Staff(scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    signature = inspect(staff[0]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Tuplet, signature)
    assert len(list(iter)) == 3


def test_iterationtools_iterate_logical_voice_in_expr_10():
    r'''Yield exact leaves.
    '''

    staff = Staff(scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    signature = inspect(staff[0]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Note, signature)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_logical_voice_in_expr_11():
    r'''Yield leaves based on names higher in inheritence hierarchy.
    '''

    staff = Staff(scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    from abjad.tools.leaftools.Leaf import Leaf
    signature = inspect(staff[0][0]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Leaf, signature)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_logical_voice_in_expr_12():
    r'''Yield Notes in two contiguous Voices with the same name.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = v2.name = 'piccolo'
    staff = Staff([v1, v2])
    signature = inspect(staff[0]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Note, signature)
    iter = list(iter)

    assert len(iter) == 4
    for e in iter:
        assert isinstance(e, Note)


def test_iterationtools_iterate_logical_voice_in_expr_13():
    r'''Yield only Notes matching the given logical voice signature.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    staff = Staff([v1, v2])
    signature = inspect(staff[0]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Note, signature)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_pitch == 0


def test_iterationtools_iterate_logical_voice_in_expr_14():
    r'''Yield only Notes matching the given logical voice signature.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = 'flute'
    v2.name = 'piccolo'
    staff = Staff([v1, v2])
    signature = inspect(staff[0]).get_parentage().logical_voice_indicator
    iter = iterationtools.iterate_logical_voice_in_expr(staff, Note, signature)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_pitch == 0
