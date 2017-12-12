import abjad
import pytest


def test_scoretools_Mutation_swap_01():
    r'''Moves parentage, children and spanners from multiple containers
    to empty tuplet.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
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
        )

    tuplet = abjad.Tuplet((3, 4), [])
    abjad.mutate(voice[:2]).swap(tuplet)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'8 [
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_swap_02():
    r'''Moves parentage, children and spanners from container to empty voice.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).leaves()
    voice.name = 'foo'
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves)
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r'''
        \context Voice = "foo" {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    new_voice = abjad.Voice()
    new_voice.name = 'foo'
    abjad.mutate(voice[1:2]).swap(new_voice)

    assert format(voice) == abjad.String.normalize(
        r'''
        \context Voice = "foo" {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            \context Voice = "foo" {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_swap_03():
    r'''Moves parentage, children and spanners from container to empty tuplet.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).leaves()
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves)
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    tuplet = abjad.Tuplet((3, 4), [])
    abjad.mutate(voice[1:2]).swap(tuplet)


    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4 {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_swap_04():
    r'''Trying to move parentage, children and spanners to noncontainer
    raises exception.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    note = abjad.Note("c'4")
    assert pytest.raises(Exception, 'abjad.mutate(voice[1:2]).swap(note)')


def test_scoretools_Mutation_swap_05():
    r'''Trying to move parentage, children and spanners from
    nonempty container to nonempty container raises exception.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    assert pytest.raises(Exception, 'abjad.mutate(voice[1:2]).swap(tuplet)')


def test_scoretools_Mutation_swap_06():
    r'''Trying to move parentage, children and spanners from components
    that are not parent-contiguous raises exception.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
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
        )

    tuplet = abjad.Tuplet((2, 3), [])
    statement = 'abjad.mutate([voice[0], voice[2]]).swap(tuplet)'
    assert pytest.raises(Exception, statement)


def test_scoretools_Mutation_swap_07():
    r'''Moves parentage, children and spanners from one measure to another.
    '''

    measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")

    assert format(measure) == abjad.String.normalize(
        r'''
        { % measure
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        } % measure
        '''
        )

    new_measure = abjad.Measure((4, 8), [])
    abjad.mutate(measure).swap(new_measure)

    assert format(new_measure) == abjad.String.normalize(
        r'''
        { % measure
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        } % measure
        '''
        )

    assert abjad.inspect(new_measure).is_well_formed()
