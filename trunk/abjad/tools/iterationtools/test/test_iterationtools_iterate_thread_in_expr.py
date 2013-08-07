# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_thread_in_expr_01():
    r'''Yield nothing when class not present.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = staff[-1].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Rest, thread_signature, reverse=True)
    assert len(list(iter)) == 0


def test_iterationtools_iterate_thread_in_expr_02():
    r'''Yield internal nodes only.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = staff[-1].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Tuplet, thread_signature, reverse=True)
    assert len(list(iter)) == 3


def test_iterationtools_iterate_thread_in_expr_03():
    r'''Yield exact leaves.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = staff[-1].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Note, thread_signature, reverse=True)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_thread_in_expr_04():
    r'''Yield leaves based on names higher in inheritence hierarchy.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    from abjad.tools.leaftools.Leaf import Leaf
    thread_signature = staff[-1][-1].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Leaf, thread_signature, reverse=True)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_thread_in_expr_05():
    r'''Yield Notes in two contiguous Voices with the same name.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = v2.name = 'piccolo'
    staff = Staff([v1, v2])
    thread_signature = staff[-1].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Note, thread_signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 4
    for e in iter:
        assert isinstance(e, Note)


def test_iterationtools_iterate_thread_in_expr_06():
    r'''Yield only Notes matching the given thread signature.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    staff = Staff([v1, v2])
    thread_signature = staff[-1].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Note, thread_signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_chromatic_pitch == 2


def test_iterationtools_iterate_thread_in_expr_07():
    r'''Yield only Notes matching the given thread signature.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = 'flute'
    v2.name = 'piccolo'
    staff = Staff([v1, v2])
    thread_signature = staff[-1].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Note, thread_signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_chromatic_pitch == 2


def test_iterationtools_iterate_thread_in_expr_08():
    r'''Yield nothing when class not present.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = staff[0].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Rest, thread_signature)
    assert len(list(iter)) == 0


def test_iterationtools_iterate_thread_in_expr_09():
    r'''Yield internal nodes only.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = staff[0].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Tuplet, thread_signature)
    assert len(list(iter)) == 3


def test_iterationtools_iterate_thread_in_expr_10():
    r'''Yield exact leaves.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = staff[0].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Note, thread_signature)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_thread_in_expr_11():
    r'''Yield leaves based on names higher in inheritence hierarchy.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    from abjad.tools.leaftools.Leaf import Leaf
    thread_signature = staff[0][0].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Leaf, thread_signature)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_thread_in_expr_12():
    r'''Yield Notes in two contiguous Voices with the same name.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = v2.name = 'piccolo'
    staff = Staff([v1, v2])
    thread_signature = staff[0].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Note, thread_signature)
    iter = list(iter)

    assert len(iter) == 4
    for e in iter:
        assert isinstance(e, Note)


def test_iterationtools_iterate_thread_in_expr_13():
    r'''Yield only Notes matching the given thread signature.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    staff = Staff([v1, v2])
    thread_signature = staff[0].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(staff, Note, thread_signature)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_chromatic_pitch == 0


def test_iterationtools_iterate_thread_in_expr_14():
    r'''Yield only Notes matching the given thread signature.
    '''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = 'flute'
    v2.name = 'piccolo'
    t = Staff([v1, v2])
    thread_signature = t[0].select_parentage().containment_signature
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_chromatic_pitch == 0
