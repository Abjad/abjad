# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_all_are_contiguous_components_01():
    r'''True for strictly contiguous leaves in voice.
        False for other time orderings of leaves in voice.'''

    voice = Voice("c'8 d'8 e'8 f'8")

    assert componenttools.all_are_contiguous_components(voice.select_leaves())

    components = list(reversed(voice.select_leaves()))
    assert not componenttools.all_are_contiguous_components(components)

    components = []
    components.extend(voice.select_leaves()[2:])
    components.extend(voice.select_leaves()[:2])
    assert not componenttools.all_are_contiguous_components(components)

    components = []
    components.extend(voice.select_leaves()[3:4])
    components.extend(voice.select_leaves()[0:1])
    assert not componenttools.all_are_contiguous_components(components)

    components = [voice]
    components.extend(voice.select_leaves())
    assert not componenttools.all_are_contiguous_components(components)


def test_componenttools_all_are_contiguous_components_02():
    r'''True for strictly contiguous components.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

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

    assert componenttools.all_are_contiguous_components([voice])
    assert componenttools.all_are_contiguous_components(voice[:])
    assert componenttools.all_are_contiguous_components(voice[0][:])
    assert componenttools.all_are_contiguous_components(voice[1][:])
    assert componenttools.all_are_contiguous_components(voice[0:1] + voice[1][:])
    assert componenttools.all_are_contiguous_components(voice[0][:] + voice[1:2])
    assert componenttools.all_are_contiguous_components(voice.select_leaves())


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
