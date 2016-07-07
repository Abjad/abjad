# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Container___setitem___01():
    r'''Replaces in-score leaf with out-of-score leaf.
    '''

    voice = Voice("c'8 [ d'8 ] e'8 f'8")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    attach(Glissando(), list(leaves))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    voice[1] = Note("c''8")

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            c''8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___02():
    r'''Replaces in-score leaf with out-of-score container.
    '''

    voice = Voice("c'8 [ d'8 ] e'8 f'8")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    glissando = Glissando(allow_repeated_pitches=True)
    attach(glissando, list(leaves))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 ] \glissando
            e'8 \glissando
            f'8
        }
        '''
        )

    voice[1] = Container("c'16 c'16 c'16")

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            {
                c'16 \glissando
                c'16 \glissando
                c'16 ] \glissando
            }
            e'8 \glissando
            f'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___03():
    r'''Replaces in-score container with out-of-score leaf.
    '''

    voice = Voice("{ c'8 [ d'8 } { e'8 f'8 ] }")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    attach(Glissando(), list(leaves))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 ]
            }
        }
        '''
        )

    voice[1] = Note("c''8")

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            c''8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___04():
    r'''Replaces in-score container with out-of-score tuplet.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = select(voice).by_leaf()
    attach(Beam(), leaves)
    attach(Glissando(), leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 ]
            }
        }
        '''
        )

    voice[1] = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            \times 2/3 {
                c'8 \glissando
                d'8 \glissando
                e'8 ]
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___05():
    r'''Replaces in-score container with out-of-score leaf.
    '''

    voice = Voice("{ c'8 [ d'8 } { e'8 f'8 ] }")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    attach(Glissando(), list(leaves))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 ]
            }
        }
        '''
        )

    voice[1] = Note("c''8")

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            c''8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___06():
    r'''Replaces in-score container with out-of-score leaf.
    '''

    voice = Voice(2 * Container("c'8 c'8 c'8 c'8"))
    voice = Voice("{ c'8 d'8 e'8 f'8 } { g'8 a'8 b'8 c''8 }")
    leaves = iterate(voice).by_class(scoretools.Leaf)
    attach(Beam(), list(leaves)[0:6])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
                b'8
                c''8
            }
        }
        '''
        )

    voice[1] = Rest('r2')

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                d'8
                e'8
                f'8 ]
            }
            r2
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___setitem___07():
    r'''Replaces note in one score with note from another score.
    '''

    notes = [
        Note("c'8"), Note("d'8"), Note("e'8"), 
        Note("f'8"), Note("g'8"), Note("a'8"),
        ]

    voice_1 = Voice(notes[:3])
    attach(Beam(), voice_1[:])

    assert format(voice_1) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    voice_2 = Voice(notes[3:])
    attach(Beam(), voice_2[:])

    assert format(voice_2) == stringtools.normalize(
        r'''
        \new Voice {
            f'8 [
            g'8
            a'8 ]
        }
        '''
        )

    voice_1[1] = voice_2[1]

    assert format(voice_1) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            g'8
            e'8 ]
        }
        '''
        )

    assert inspect_(voice_1).is_well_formed()

    assert format(voice_2) == stringtools.normalize(
        r'''
        \new Voice {
            f'8 [
            a'8 ]
        }
        '''
        )

    assert inspect_(voice_2).is_well_formed()


def test_scoretools_Container___setitem___08():
    r'''Replaces note in one score with container from another score.
    '''

    notes = [
        Note("c'8"), Note("d'8"), Note("e'8"),
        Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8"),
        ]
    voice_1 = Voice(notes[:3])
    attach(Beam(), voice_1[:])

    assert format(voice_1) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    voice_2 = Voice(notes[3:])
    Container(voice_2[1:3])
    leaves = iterate(voice_2).by_class(scoretools.Leaf)
    attach(Glissando(), list(leaves))
    leaves = iterate(voice_2[1]).by_class(scoretools.Leaf)
    attach(Slur(), list(leaves))

    assert format(voice_2) == stringtools.normalize(
        r'''
        \new Voice {
            f'8 \glissando
            {
                g'8 \glissando (
                a'8 ) \glissando
            }
            b'8
        }
        '''
        )

    voice_1[1] = voice_2[1]

    assert format(voice_1) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            {
                g'8 (
                a'8 )
            }
            e'8 ]
        }
        '''
        )

    assert inspect_(voice_1).is_well_formed()

    assert format(voice_2) == stringtools.normalize(
        r'''
        \new Voice {
            f'8 \glissando
            b'8
        }
        '''
        )

    assert inspect_(voice_2).is_well_formed()


def test_scoretools_Container___setitem___09():
    r'''Sets leaf between unspanned components.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[2:2] = [Note("g'8")]

    assert format(staff) == stringtools.normalize(
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


def test_scoretools_Container___setitem___10():
    r'''Sets leaf between spanned compoennts.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, staff[:])
    note = Note("g'8")
    staff[2:2] = [note]

    assert format(staff) == stringtools.normalize(
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


def test_scoretools_Container___setitem___11():
    r'''Sets multiple leaves between spanned components.
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

    assert format(staff) == stringtools.normalize(
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

    assert format(staff) == stringtools.normalize(
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


def test_scoretools_Container___setitem___12():
    r'''Replaces multiple spanned leaves with with single leaf.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, staff[:])
    note = Note("c''8")
    staff[1:3] = [note]

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            c''8
            f'8 ]
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Container___setitem___13():
    r'''Replaces three spanned leaves with three different leaves.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, staff[:])
    notes = [Note("b'8"), Note("a'8"), Note("g'8")]
    staff[1:3] = notes

    assert format(staff) == stringtools.normalize(
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


def test_scoretools_Container___setitem___14():
    r'''Replaces in-score container with contents of container.
    '''

    staff = Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert format(staff) == stringtools.normalize(
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

    container = staff[0]
    staff[0:1] = container[:]

    assert format(staff) == stringtools.normalize(
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
    assert len(container) == 0


def test_scoretools_Container___setitem___15():
    r'''Sets first slice of staff equal to first element of first container in
    staff.
    '''

    staff = Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert format(staff) == stringtools.normalize(
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

    assert format(staff) == stringtools.normalize(
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


def test_scoretools_Container___setitem___16():
    r'''Sets first slice of staff equal to contents of first container in
    staff.

    Empties first container in staff.

    Leaves empty container in staff.
    '''

    staff = Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert format(staff) == stringtools.normalize(
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

    assert format(staff) == stringtools.normalize(
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


def test_scoretools_Container___setitem___17():
    r'''Set first slice of staff equal to contents of first container in staff;
    empties first container in staff.

    Sets contents of empty first container in staff equal to first component in
    second container in staff.
    '''

    staff = Staff("{ c'8 [ d'8 } { e'8 f'8 ] }")

    assert format(staff) == stringtools.normalize(
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

    container = staff[0]
    staff[0:0] = container[:]
    container[0:0] = staff[-1][:1]

    assert format(staff) == stringtools.normalize(
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


def test_scoretools_Container___setitem___18():
    r'''Extremely small coequal indices indicate first slice in staff.
    '''

    voice = Voice("c'8 [ d'8 e'8 f'8 ]")
    voice[-1000:-1000] = [Rest('r8')]

    assert format(voice) == stringtools.normalize(
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

    assert format(voice) == stringtools.normalize(
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


def test_scoretools_Container___setitem___19():
    r'''Extremely large coequal indices indicate last slice in staff.
    '''

    voice = Voice("c'8 [ d'8 e'8 f'8 ]")
    voice[1000:1000] = [Rest('r8')]

    assert format(voice) == stringtools.normalize(
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


def test_scoretools_Container___setitem___20():
    r'''You can use setitem to empty the contents of a container.
    When you do this, emptied components withdraw
    from absolutely all spanners.

    On the other hand, if you want to empty a container and
    allow the emptied components to remain embedded within spanners,
    use del(container) instead.
    '''

    staff = Staff("c'8 d'8 [ e'8 ] f'8")
    inner_container = Container(staff[1:3])
    outer_container = Container([inner_container])

    assert format(staff) == stringtools.normalize(
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

    # sets contents of outer container to nothing
    outer_container[:] = []

    # outer container is empty and remains in score
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8
            {
            }
            f'8
        }
        '''
        )

    # inner container leaves are no longer spanned
    assert format(inner_container) == stringtools.normalize(
        r'''
        {
            d'8
            e'8
        }
        '''
        )

    # ALTERNATIVE: use del(container)
    staff = Staff("c'8 d'8 [ e'8 ] f'8")
    inner_container = Container(staff[1:3])
    outer_container = Container([inner_container])

    assert format(staff) == stringtools.normalize(
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

    # deletes outer container
    del(outer_container[:])

    # outer container is empty and remains in score (as before)
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8
            {
            }
            f'8
        }
        '''
        )

    # inner container leaves are still spanned
    assert format(inner_container) == stringtools.normalize(
        r'''
        {
            d'8 [
            e'8 ]
        }
        '''
        )


def test_scoretools_Container___setitem___21():
    r'''Extends beam as leaves append and insert into staff.
    '''

    staff = Staff("c'8 [ { d'8 e'8 } f'8 ]")
    beam = inspect_(staff[0]).get_spanner(prototype=Beam)

    leaves = iterate(staff).by_class(scoretools.Leaf)
    assert beam.components == list(leaves)

    staff[1].append("g'8")
    leaves = iterate(staff).by_class(scoretools.Leaf)
    assert beam.components == list(leaves)

    staff[1].insert(0, "b'8")
    leaves = iterate(staff).by_class(scoretools.Leaf)
    assert beam.components == list(leaves)

    staff.insert(1, "a'8")
    leaves = iterate(staff).by_class(scoretools.Leaf)
    assert beam.components == list(leaves)

    staff.insert(3, "fs'8")
    leaves = iterate(staff).by_class(scoretools.Leaf)
    assert beam.components == list(leaves)

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
