from abjad import *
import py.test


def test_componenttools_all_are_thread_contiguous_components_01():
    '''True for thread contiguous components even when
        components are not strictly contiguous.'''

    t = Voice(notetools.make_repeated_notes(4))
    t.insert(2, Voice(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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
    assert componenttools.all_are_thread_contiguous_components([t.leaves[i] for i in outer])


def test_componenttools_all_are_thread_contiguous_components_02():
    '''Temporal gaps between components are OK.
        So long as gaps are filled with foreign components
        that do not belong to thread.'''

    t = Voice(notetools.make_repeated_notes(4))
    t.insert(2, Voice(notetools.make_repeated_notes(2)))
    Container(t[:2])
    Container(t[-2:])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.all_are_thread_contiguous_components(t[0:1] + t[-1:])
    assert componenttools.all_are_thread_contiguous_components(t[0][:] + t[-1:])
    assert componenttools.all_are_thread_contiguous_components(t[0:1] + t[-1][:])
    assert componenttools.all_are_thread_contiguous_components(t[0][:] + t[-1][:])


def test_componenttools_all_are_thread_contiguous_components_03():
    '''Components that start at the same moment are bad.
        Even if components are all part of the same thread.'''

    t = Voice(notetools.make_repeated_notes(4))
    t.insert(2, Voice(notetools.make_repeated_notes(2)))
    Container(t[:2])
    Container(t[-2:])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert not componenttools.all_are_thread_contiguous_components([t, t[0]])
    assert not componenttools.all_are_thread_contiguous_components(t[0:1] + t[0][:])
    assert not componenttools.all_are_thread_contiguous_components(t[-1:] + t[-1][:])


def test_componenttools_all_are_thread_contiguous_components_04():
    '''True for strictly contiguous leaves in same staff.'''

    t = Staff("c'8 d'8 e'8 f'8")
    assert componenttools.all_are_thread_contiguous_components(t[:])


def test_componenttools_all_are_thread_contiguous_components_05():
    '''True for orphan components when allow_orphans is True.
        False for orphan components when allow_orphans is False.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert componenttools.all_are_thread_contiguous_components(notes)
    assert not componenttools.all_are_thread_contiguous_components(notes, allow_orphans = False)


def test_componenttools_all_are_thread_contiguous_components_06():
    '''False for time reordered leaves in staff.'''

    t = Staff("c'8 d'8 e'8 f'8")
    assert not componenttools.all_are_thread_contiguous_components(t[2:] + t[:2])


def test_componenttools_all_are_thread_contiguous_components_07():
    '''True for unincorporated component.'''

    assert componenttools.all_are_thread_contiguous_components([Staff("c'8 d'8 e'8 f'8")])


def test_componenttools_all_are_thread_contiguous_components_08():
    '''True for empty list.'''

    assert componenttools.all_are_thread_contiguous_components([])


def test_componenttools_all_are_thread_contiguous_components_09():
    '''False when components belonging to same thread are ommitted.'''

    t = Voice("c'8 d'8 e'8 f'8 g'8 a'8")
    spannertools.BeamSpanner(t[:])

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

    assert not componenttools.all_are_thread_contiguous_components(t[:2] + t[-2:])


def test_componenttools_all_are_thread_contiguous_components_10():
    '''False when components belonging to same thread are ommitted.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)

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
