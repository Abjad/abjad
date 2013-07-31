# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_all_are_contiguous_components_01():
    r'''True for strictly contiguous leaves in voice.
        False for other time orderings of leaves in voice.'''

    t = Voice("c'8 d'8 e'8 f'8")

    assert componenttools.all_are_contiguous_components(t.select_leaves())

    components = list(reversed(t.select_leaves()))
    assert not componenttools.all_are_contiguous_components(components)

    components = []
    components.extend(t.select_leaves()[2:])
    components.extend(t.select_leaves()[:2])
    assert not componenttools.all_are_contiguous_components(components)

    components = []
    components.extend(t.select_leaves()[3:4])
    components.extend(t.select_leaves()[0:1])
    assert not componenttools.all_are_contiguous_components(components)

    components = [t]
    components.extend(t.select_leaves())
    assert not componenttools.all_are_contiguous_components(components)


def test_componenttools_all_are_contiguous_components_02():
    r'''True for strictly contiguous components.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

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

    assert componenttools.all_are_contiguous_components([t])
    assert componenttools.all_are_contiguous_components(t[:])
    assert componenttools.all_are_contiguous_components(t[0][:])
    assert componenttools.all_are_contiguous_components(t[1][:])
    assert componenttools.all_are_contiguous_components(t[0:1] + t[1][:])
    assert componenttools.all_are_contiguous_components(t[0][:] + t[1:2])
    assert componenttools.all_are_contiguous_components(t.select_leaves())


def test_componenttools_all_are_contiguous_components_03():
    r'''Unicorporated leaves can not be evaluated for contiguity.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    assert componenttools.all_are_contiguous_components(notes)
    assert not componenttools.all_are_contiguous_components(notes, allow_orphans=False)


def test_componenttools_all_are_contiguous_components_04():
    r'''Empty list returns True.
    '''

    t = []

    assert componenttools.all_are_contiguous_components(t)
