from abjad import *
from abjad.tools.componenttools._Component import _Component
import py.test


def test_componenttools_all_are_components_in_same_parent_01():

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
    }
    '''


    assert componenttools.all_are_components_in_same_parent(t[:])
    assert componenttools.all_are_components_in_same_parent(t.leaves[:2])
    assert componenttools.all_are_components_in_same_parent(t.leaves[2:])

    assert componenttools.all_are_components_in_same_parent([t])
    assert not componenttools.all_are_components_in_same_parent([t], allow_orphans = False)

    assert not componenttools.all_are_components_in_same_parent(t.leaves)
    assert not componenttools.all_are_components_in_same_parent(
        list(componenttools.iterate_components_forward_in_expr(t, _Component)))


def test_componenttools_all_are_components_in_same_parent_02():

    t1 = Voice("c'8 d'8 e'8 f'8")
    t2 = Voice("c'8 d'8 e'8 f'8")

    assert componenttools.all_are_components_in_same_parent(t1.leaves)
    assert componenttools.all_are_components_in_same_parent(t2.leaves)

    assert componenttools.all_are_components_in_same_parent([t1])
    assert not componenttools.all_are_components_in_same_parent([t1], allow_orphans = False)

    assert componenttools.all_are_components_in_same_parent([t2])
    assert not componenttools.all_are_components_in_same_parent([t2], allow_orphans = False)

    assert componenttools.all_are_components_in_same_parent([t1, t2])
    assert not componenttools.all_are_components_in_same_parent([t1, t2],
        allow_orphans = False)

    assert not componenttools.all_are_components_in_same_parent(t1.leaves + t2.leaves)


def test_componenttools_all_are_components_in_same_parent_03():
    #'''Nonlist input raises TypeError.'''
    '''Noniterable input returns false.
    '''

    #assert py.test.raises(TypeError,
    #    'componenttools.all_are_components_in_same_parent(Note(0, (1, 8)))')

    assert not componenttools.all_are_components_in_same_parent(Note(0, (1, 8)))


def test_componenttools_all_are_components_in_same_parent_04():
    '''Empty list returns True.'''

    assert componenttools.all_are_components_in_same_parent([])
