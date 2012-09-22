from abjad import *


def test_iterationtools_iterate_thread_in_expr_01():
    '''Yield nothing when class not present.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = componenttools.component_to_containment_signature(t[-1])
    iter = iterationtools.iterate_thread_in_expr(t, Rest, thread_signature, reverse=True)
    assert len(list(iter)) == 0


def test_iterationtools_iterate_thread_in_expr_02():
    '''Yield internal nodes only.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = componenttools.component_to_containment_signature(t[-1])
    iter = iterationtools.iterate_thread_in_expr(t, Tuplet, thread_signature, reverse=True)
    assert len(list(iter)) == 3


def test_iterationtools_iterate_thread_in_expr_03():
    '''Yield exact leaves.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = componenttools.component_to_containment_signature(t[-1])
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature, reverse=True)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_thread_in_expr_04():
    '''Yield leaves based on names higher in inheritence hierarchy.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    from abjad.tools.leaftools.Leaf import Leaf
    thread_signature = componenttools.component_to_containment_signature(t[-1][-1])
    iter = iterationtools.iterate_thread_in_expr(t, Leaf, thread_signature, reverse=True)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_thread_in_expr_05():
    '''Yield Notes in two contiguous Voices with the same name.'''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = v2.name = 'piccolo'
    t = Staff([v1, v2])
    thread_signature = componenttools.component_to_containment_signature(t[-1])
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 4
    for e in iter:
        assert isinstance(e, Note)


def test_iterationtools_iterate_thread_in_expr_06():
    '''Yield only Notes matching the given thread signature.'''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    t = Staff([v1, v2])
    thread_signature = componenttools.component_to_containment_signature(t[-1])
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_chromatic_pitch == 2


def test_iterationtools_iterate_thread_in_expr_07():
    '''Yield only Notes matching the given thread signature.'''

    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = 'flute'
    v2.name = 'piccolo'
    t = Staff([v1, v2])
    thread_signature = componenttools.component_to_containment_signature(t[-1])
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature, reverse=True)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_chromatic_pitch == 2


def test_iterationtools_iterate_thread_in_expr_08():
    '''Yield nothing when class not present.'''
    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = componenttools.component_to_containment_signature(t[0])
    iter = iterationtools.iterate_thread_in_expr(t, Rest, thread_signature)
    assert len(list(iter)) == 0


def test_iterationtools_iterate_thread_in_expr_09():
    '''Yield internal nodes only.'''
    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = componenttools.component_to_containment_signature(t[0])
    iter = iterationtools.iterate_thread_in_expr(t, Tuplet, thread_signature)
    assert len(list(iter)) == 3


def test_iterationtools_iterate_thread_in_expr_10():
    '''Yield exact leaves.'''
    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    thread_signature = componenttools.component_to_containment_signature(t[0])
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_thread_in_expr_11():
    '''Yield leaves based on names higher in inheritence hierarchy.'''
    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3) * 3)
    from abjad.tools.leaftools.Leaf import Leaf
    thread_signature = componenttools.component_to_containment_signature(t[0][0])
    iter = iterationtools.iterate_thread_in_expr(t, Leaf, thread_signature)
    assert len(list(iter)) == 9


def test_iterationtools_iterate_thread_in_expr_12():
    '''Yield Notes in two contiguous Voices with the same name.'''
    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = v2.name = 'piccolo'
    t = Staff([v1, v2])
    thread_signature = componenttools.component_to_containment_signature(t[0])
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature)
    iter = list(iter)

    assert len(iter) == 4
    for e in iter:
        assert isinstance(e, Note)


def test_iterationtools_iterate_thread_in_expr_13():
    '''Yield only Notes matching the given thread signature.'''
    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    t = Staff([v1, v2])
    thread_signature = componenttools.component_to_containment_signature(t[0])
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_chromatic_pitch == 0


def test_iterationtools_iterate_thread_in_expr_14():
    '''Yield only Notes matching the given thread signature.'''
    v1 = Voice(Note("c'4") * 2)
    v2 = Voice(Note(2, (1, 4)) * 2)
    v1.name = 'flute'
    v2.name = 'piccolo'
    t = Staff([v1, v2])
    thread_signature = componenttools.component_to_containment_signature(t[0])
    iter = iterationtools.iterate_thread_in_expr(t, Note, thread_signature)
    iter = list(iter)

    assert len(iter) == 2
    for e in iter:
        assert isinstance(e, Note)
        assert e.written_pitch.numbered_chromatic_pitch == 0
