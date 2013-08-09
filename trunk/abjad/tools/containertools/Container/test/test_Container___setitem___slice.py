# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Container___setitem___slice_01():
    r'''Containers set single leaves correctly in an unspanned structure.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[2:2] = [Note(7, (1, 8))]

    r'''
    \new Staff {
        c'8
        d'8
        g'8
        e'8
        f'8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            g'8
            e'8
            f'8
        }
        '''
        )


def test_Container___setitem___slice_02():
    r'''Set single leaf between spanned components.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    p = spannertools.BeamSpanner(staff[:])
    note = Note(7, (1, 8))
    staff[2:2] = [note]

    r'''
    \new Staff {
        c'8 [
        d'8
        g'8
        e'8
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            g'8
            e'8
            f'8 ]
        }
        '''
        )


def test_Container___setitem___slice_03():
    r'''Containers set sequence of leaves
        between spanned components.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"), Note("a'8")]

    beginning = notes[:2]
    middle = notes[2:4]
    end = notes[4:]

    staff = Staff(beginning + end)
    p = spannertools.BeamSpanner(staff[:])

    r'''
    \new Staff {
        c'8 [
        d'8
        g'8
        a'8 ]
    }
    '''

    staff[2:2] = middle

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8
        g'8
        a'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8
            g'8
            a'8 ]
        }
        '''
        )


def test_Container___setitem___slice_04():
    r'''Replace sequence of spanned components with a single leaf.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    p = spannertools.BeamSpanner(staff[:])
    note = Note(12, (1, 8))
    staff[1:3] = [note]

    r'''
    \new Staff {
        c'8 [
        c''8
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            c''8
            f'8 ]
        }
        '''
        )


def test_Container___setitem___slice_05():
    r'''Replace a sequence of multiple components with
        a different sequence of multiple components.'''

    staff = Staff("c'8 d'8 e'8 f'8")
    p = spannertools.BeamSpanner(staff[:])
    notes = [Note(11, (1, 8)), Note(9, (1, 8)), Note(7, (1, 8))]
    staff[1:3] = notes

    r'''
    \new Staff {
        c'8 [
        b'8
        a'8
        g'8
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            b'8
            a'8
            g'8
            f'8 ]
        }
        '''
        )


def test_Container___setitem___slice_06():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    sequential = staff[0]
    staff[0:1] = sequential.select_leaves()

    r'''
    \new Staff {
        c'8 [
        d'8
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(sequential) == 0
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            {
                e'8
                f'8 ]
            }
        }
        '''
        )


def test_Container___setitem___slice_07():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {

        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    staff[0:0] = staff[0][:1]

    r'''
    \new Staff {
        c'8
        {
            d'8 [
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            {
                d'8 [
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )


def test_Container___setitem___slice_08():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    staff[0:0] = staff[0][:]

    r'''
    \new Staff {
        c'8
        d'8
        {
        }
        {
            e'8 [
            f'8 ]
        }
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            {
            }
            {
                e'8 [
                f'8 ]
            }
        }
        '''
        )


def test_Container___setitem___slice_09():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    sequential = staff[0]
    staff[0:0] = sequential[:]
    sequential[0:0] = staff[-1][:1]

    r'''
    \new Staff {
        c'8
        d'8
        {
            e'8
        }
        {
            f'8 [ ]
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            {
                e'8
            }
            {
                f'8 [ ]
            }
        }
        '''
        )


def test_Container___setitem___slice_10():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    staff[0:0] = staff[0][:1]
    staff[len(staff):len(staff)] = staff[-1][-1:]

    r'''
    \new Staff {
        c'8
        {
            d'8 [
        }
        {
            e'8 ]
        }
        f'8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            {
                d'8 [
            }
            {
                e'8 ]
            }
            f'8
        }
        '''
        )


def test_Container___setitem___slice_11():
    r'''Extremely small coequal indices act as zero.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    voice[-1000:-1000] = [Rest((1, 8))]

    r'''
    \new Voice {
        r8
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            r8
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )


def test_Container___setitem___slice_12():
    r'''Extremely large, coequal indices work correctly.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    voice[1000:1000] = [Rest((1, 8))]

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
        r'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
            r8
        }
        '''
        )


def test_Container___setitem___slice_13():
    r'''You can use the slice for of setitem to empty the contents
    of a container. When you do this, emptied components withdraw
    from absolutely all spanners.

    On the other hand, if you want to empty a container and
    allow the emptied components to remain embedded within spanners,
    use del(container) instead.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    inner = Container(staff[1:3])
    outer = Container([inner])
    beam = spannertools.BeamSpanner(inner[:])

    r'''
    \new Staff {
        c'8
        {
            {
                d'8 [
                e'8 ]
            }
        }
        f'8
    }
    '''

    # set outer container contents to empty
    outer[:] = []

    r'''
    \new Staff {
        c'8
        {
        }
        f'8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            {
            }
            f'8
        }
        '''
        )

    r'''
    {
        d'8
        e'8
    }
    '''

    # inner container leaves DO withdraw from all spanners
    assert testtools.compare(
        inner,
        r'''
        {
            d'8
            e'8
        }
        '''
        )

    # ALTERNATIVE: use del(container)

    staff = Staff("c'8 d'8 e'8 f'8")
    inner = Container(staff[1:3])
    outer = Container([inner])
    beam = spannertools.BeamSpanner(inner[:])

    del(outer[:])

    r'''
    \new Staff {
        c'8
        {
        }
        f'8
    }
    '''

    r'''
    {
        d'8 [
        e'8 ]
    }
    '''

    # inner container leaves DO NOT withdraw from spanners
    assert testtools.compare(
        inner,
        r'''
        {
            d'8 [
            e'8 ]
        }
        '''
        )
