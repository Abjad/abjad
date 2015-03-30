# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Container___setitem___slice_01():
    r'''Containers set single leaves correctly in an unspanned structure.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[2:2] = [Note(7, (1, 8))]

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___slice_02():
    r'''Set single leaf between spanned components.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, staff[:])
    note = Note(7, (1, 8))
    staff[2:2] = [note]

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___slice_03():
    r'''Containers set sequence of leaves between spanned components.
    '''

    notes = [
        Note("c'8"), Note("d'8"), Note("e'8"),
        Note("f'8"), Note("g'8"), Note("a'8"),
        ]

    beginning = notes[:2]
    middle = notes[2:4]
    end = notes[4:]

    staff = Staff(beginning + end)
    beam = Beam()
    attach(beam, staff[:])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            g'8
            a'8 ]
        }
        '''
        )

    staff[2:2] = middle

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___slice_04():
    r'''Replace sequence of spanned components with a single leaf.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, staff[:])
    note = Note(12, (1, 8))
    staff[1:3] = [note]

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            c''8
            f'8 ]
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___slice_05():
    r'''Replace a sequence of multiple components with
    a different sequence of multiple components.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, staff[:])
    notes = [Note(11, (1, 8)), Note(9, (1, 8)), Note(7, (1, 8))]
    staff[1:3] = notes

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___slice_06():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, staff.select_leaves())

    assert systemtools.TestManager.compare(
        staff,
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
        )

    sequential = staff[0]
    staff[0:1] = sequential.select_leaves()

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()
    assert len(sequential) == 0


def test_scoretools_Container___setitem___slice_07():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, staff.select_leaves())

    assert systemtools.TestManager.compare(
        staff,
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
        )

    staff[0:0] = staff[0][:1]

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___slice_08():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, staff.select_leaves())

    assert systemtools.TestManager.compare(
        staff,
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
        )

    staff[0:0] = staff[0][:]

    assert systemtools.TestManager.compare(
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


def test_scoretools_Container___setitem___slice_09():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, staff.select_leaves())

    assert systemtools.TestManager.compare(
        staff,
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
        )

    sequential = staff[0]
    staff[0:0] = sequential[:]
    sequential[0:0] = staff[-1][:1]

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___slice_10():
    r'''Donor and recipient container are the same.
    '''

    staff = Staff("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, staff.select_leaves())

    assert systemtools.TestManager.compare(
        staff,
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
        )

    staff[0:0] = staff[0][:1]
    staff[len(staff):len(staff)] = staff[-1][-1:]

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
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

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___slice_11():
    r'''Extremely small coequal indices act as zero.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    voice[-1000:-1000] = [Rest((1, 8))]

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
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

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___slice_12():
    r'''Extremely large, coequal indices work correctly.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    voice[1000:1000] = [Rest((1, 8))]

    assert systemtools.TestManager.compare(
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

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___slice_13():
    r'''You can use setitem to empty the contents of a container.
    When you do this, emptied components withdraw
    from absolutely all spanners.

    On the other hand, if you want to empty a container and
    allow the emptied components to remain embedded within spanners,
    use del(container) instead.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    inner = Container(staff[1:3])
    outer = Container([inner])
    beam = Beam()
    attach(beam, inner[:])

    assert systemtools.TestManager.compare(
        staff,
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
        )

    # empty outer container
    outer[:] = []

    assert systemtools.TestManager.compare(
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

    # inner container leaves DO withdraw from all spanners
    assert systemtools.TestManager.compare(
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
    beam = Beam()
    attach(beam, inner[:])

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
    assert systemtools.TestManager.compare(
        inner,
        r'''
        {
            d'8 [
            e'8 ]
        }
        '''
        )


def test_scoretools_Container___setitem___slice_14():

    staff = Staff("c'8 { d'8 e'8 } f'8")
    beam = Beam()
    attach(beam, staff.select_leaves())
    assert beam.components == staff.select_leaves()

    staff[1].append("g'8")
    assert beam.components == staff.select_leaves()

    staff[1].insert(0, "b'8")
    assert beam.components == staff.select_leaves()

    staff.insert(1, "a'8")
    assert beam.components == staff.select_leaves()

    staff.insert(3, "fs'8")
    assert beam.components == staff.select_leaves()

    assert format(staff) == systemtools.TestManager.clean_string(
        r'''
        \new Staff {
            c'8 [
            a'8
            {
                b'8
                d'8
                e'8
                g'8
            }
            fs'8
            f'8 ]
        }
        ''',
        )