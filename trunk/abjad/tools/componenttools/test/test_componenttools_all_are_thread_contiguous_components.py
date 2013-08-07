# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_componenttools_all_are_thread_contiguous_components_01():
    r'''True for thread contiguous components even when
        components are not strictly contiguous.'''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Voice(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

    r'''
    \new Voice {
        c'8
        d'8
        \new Voice {
            e'8
            f'8
        }
        g'8
        a'8
    }
    '''

    outer = (0, 1, 4, 5)
    assert componenttools.all_are_thread_contiguous_components([voice.select_leaves()[i] for i in outer])


def test_componenttools_all_are_thread_contiguous_components_02():
    r'''Temporal gaps between components are OK.
        So long as gaps are filled with foreign components
        that do not belong to thread.'''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Voice(notetools.make_repeated_notes(2)))
    Container(voice[:2])
    Container(voice[-2:])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        \new Voice {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
    }
    '''

    assert componenttools.all_are_thread_contiguous_components(voice[0:1] + voice[-1:])
    assert componenttools.all_are_thread_contiguous_components(voice[0][:] + voice[-1:])
    assert componenttools.all_are_thread_contiguous_components(voice[0:1] + voice[-1][:])
    assert componenttools.all_are_thread_contiguous_components(voice[0][:] + voice[-1][:])


def test_componenttools_all_are_thread_contiguous_components_03():
    r'''Components that start at the same moment are bad.
        Even if components are all part of the same thread.'''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Voice(notetools.make_repeated_notes(2)))
    Container(voice[:2])
    Container(voice[-2:])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        \new Voice {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
    }
    '''

    assert not componenttools.all_are_thread_contiguous_components([voice, voice[0]])
    assert not componenttools.all_are_thread_contiguous_components(voice[0:1] + voice[0][:])
    assert not componenttools.all_are_thread_contiguous_components(voice[-1:] + voice[-1][:])


def test_componenttools_all_are_thread_contiguous_components_04():
    r'''True for strictly contiguous leaves in same staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    assert componenttools.all_are_thread_contiguous_components(staff[:])


def test_componenttools_all_are_thread_contiguous_components_05():
    r'''True for orphan components when allow_orphans is True.
        False for orphan components when allow_orphans is False.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert componenttools.all_are_thread_contiguous_components(notes)
    assert not componenttools.all_are_thread_contiguous_components(notes, allow_orphans=False)


def test_componenttools_all_are_thread_contiguous_components_06():
    r'''False for time reordered leaves in staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    assert not componenttools.all_are_thread_contiguous_components(staff[2:] + staff[:2])


def test_componenttools_all_are_thread_contiguous_components_07():
    r'''True for unincorporated component.
    '''

    assert componenttools.all_are_thread_contiguous_components([Staff("c'8 d'8 e'8 f'8")])


def test_componenttools_all_are_thread_contiguous_components_08():
    r'''True for empty list.
    '''

    assert componenttools.all_are_thread_contiguous_components([])


def test_componenttools_all_are_thread_contiguous_components_09():
    r'''False when components belonging to same thread are ommitted.
    '''

    voice = Voice("c'8 d'8 e'8 f'8 g'8 a'8")
    spannertools.BeamSpanner(voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8
        g'8
        a'8 ]
    }
    '''

    assert not componenttools.all_are_thread_contiguous_components(voice[:2] + voice[-2:])


def test_componenttools_all_are_thread_contiguous_components_10():
    r'''False when components belonging to same thread are ommitted.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t.select_leaves())

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert not componenttools.all_are_thread_contiguous_components(t[:1] + t[-1:])
