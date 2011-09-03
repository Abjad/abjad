from abjad import *


def test_componenttools_all_are_contiguous_components_in_same_parent_01():
    '''True for strictly contiguous leaves in voice.
        False for other time orderings of leaves in voice.'''

    t = Voice("c'8 d'8 e'8 f'8")

    assert componenttools.all_are_contiguous_components_in_same_parent(t.leaves)

    assert not componenttools.all_are_contiguous_components_in_same_parent(list(reversed(t.leaves)))

    components = []
    components.extend(t.leaves[2:])
    components.extend(t.leaves[:2])
    assert not componenttools.all_are_contiguous_components_in_same_parent(components)

    components = []
    components.extend(t.leaves[3:4])
    components.extend(t.leaves[0:1])
    assert not componenttools.all_are_contiguous_components_in_same_parent(components)
    components = [t]
    components.extend(t.leaves)
    assert not componenttools.all_are_contiguous_components_in_same_parent(components)


def test_componenttools_all_are_contiguous_components_in_same_parent_02():
    '''True for unincorporated components when orphans allowed.
        False to unincorporated components when orphans not allowed.'''

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

    assert componenttools.all_are_contiguous_components_in_same_parent([t])
    assert not componenttools.all_are_contiguous_components_in_same_parent([t],
        allow_orphans = False)

    assert componenttools.all_are_contiguous_components_in_same_parent(t[:])

    assert componenttools.all_are_contiguous_components_in_same_parent(t[0][:])
    assert componenttools.all_are_contiguous_components_in_same_parent(t[1][:])

    assert not componenttools.all_are_contiguous_components_in_same_parent(t.leaves)


def test_componenttools_all_are_contiguous_components_in_same_parent_03():
    '''True for orphan leaves when allow_orphans is True.
        False for orphan leaves when allow_orphans is False.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    assert componenttools.all_are_contiguous_components_in_same_parent(notes)
    assert not componenttools.all_are_contiguous_components_in_same_parent(notes, allow_orphans = False)


def test_componenttools_all_are_contiguous_components_in_same_parent_04():
    '''Empty list returns True.'''

    t = []

    assert componenttools.all_are_contiguous_components_in_same_parent(t)
