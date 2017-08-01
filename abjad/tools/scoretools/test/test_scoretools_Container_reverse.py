# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Container_reverse_01():
    r'''Retrograde works on a depth-0 container with no spanners and no parent.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    reversed_leaves = reversed(staff[:])
    staff.reverse()

    assert list(reversed_leaves) == list(staff[:])
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container_reverse_02():
    r'''Retrograde works on a depth-0 container with one spanner
    abjad.attached and no parent.
    '''

    container = abjad.Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    leaves = abjad.select(container).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    reversed_leaves = reversed(leaves)
    container.reverse()

    assert list(reversed_leaves) == list(container[:])
    assert abjad.inspect(container).is_well_formed()


def test_scoretools_Container_reverse_03():
    r'''Retrograde works on a depth-0 container with one spanner abjad.attached
    to its leaves and with no parent.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    reversed_leaves = reversed(staff[:])
    staff.reverse()

    assert list(reversed_leaves) == list(staff[:])
    assert beam.components == tuple(staff[:])
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container_reverse_04():
    r'''Retrograde works on a depth-0 container with one spanner
    abjad.attached to itself and with a parent.
    '''

    staff = abjad.Staff([
        abjad.Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8"),
        abjad.Note("c'8"),
        abjad.Note("c'8"),
        ])
    measure = staff[0]
    beam = abjad.Beam()
    abjad.attach(beam, measure[:])
    reversed_leaves = reversed(measure[:])
    staff[0].reverse()
    assert list(reversed_leaves) == list(measure[:])
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container_reverse_05():
    r'''Retrograde works on a depth-0 container with one spanner
    abjad.attached to its leaves and with a parent.
    '''

    staff = abjad.Staff([
        abjad.Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8"),
        abjad.Note("c'8"),
        abjad.Note("c'8"),
        ])
    measure = staff[0]
    beam = abjad.Beam()
    abjad.attach(beam, measure[:])
    reversed_leaves = reversed(measure[:])
    staff[0].reverse()
    assert list(reversed_leaves) == list(measure[:])
    assert beam.components == tuple(measure[:])
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container_reverse_06():
    r'''Retrograde works on a depth-0 container with one spanner
    abjad.attached to its parent.
    '''

    notes = [abjad.Note("c'8"), abjad.Note("d'8")]
    container = abjad.Container(
        [abjad.Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")] + notes)
    measure = container[0]
    beam = abjad.Beam()
    abjad.attach(beam, measure[:])
    reversed_leaves = reversed(measure[:])
    container[0].reverse()
    assert list(reversed_leaves) == list(measure[:])
    assert abjad.inspect(container).is_well_formed()


def test_scoretools_Container_reverse_07():
    r'''Retrograde works on a depth-0 container with one spanner
    abjad.attached to its parent's contents.
    '''

    notes = [abjad.Note("c'8"), abjad.Note("d'8")]
    measure = abjad.Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    staff = abjad.Staff([measure] + notes)
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    reversed_leaves = reversed(measure[:])
    staff[0].reverse()
    assert list(reversed_leaves) == list(measure[:])
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container_reverse_08():

    notes = [abjad.Note("c'8"), abjad.Note("d'8")]
    measure = abjad.Measure((4, 4), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    staff = abjad.Staff([measure] + notes)
    leaves = abjad.select(staff).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            {
                \time 4/4
                c'8 [
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }
            c'8
            d'8 ]
        }
        '''
        )

    staff.reverse()

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            d'8 [
            c'8
            {
                \time 4/4
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ]
            }
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container_reverse_09():
    r'''Retrograde works on a depth-2 container with no parent
    and with spanners at all levels.
    '''

    measure_1 = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
    measure_2 = abjad.Measure((3, 8), "c'8 d'8 e'8")
    container = abjad.Container([measure_1, measure_2])
    leaves = abjad.select(container).by_leaf()
    pedal = abjad.PianoPedalSpanner()
    abjad.attach(pedal, leaves)
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)
    beam_1 = abjad.Beam()
    abjad.attach(beam_1, measure_1[:])
    beam_2 = abjad.Beam()
    abjad.attach(beam_2, measure_2[:])
    gliss = abjad.Glissando()
    abjad.attach(gliss, leaves)

    assert format(container) == abjad.String.normalize(
        r'''
        {
            {
                \time 4/8
                \set Staff.pedalSustainStyle = #'mixed
                c'8 [ \glissando \sustainOn \startTrillSpan
                d'8 \glissando
                e'8 \glissando
                f'8 ] \glissando
            }
            {
                \time 3/8
                c'8 [ \glissando
                d'8 \glissando
                e'8 ] \sustainOff \stopTrillSpan
            }
        }
        '''
        )

    container.reverse()

    assert format(container) == abjad.String.normalize(
        r'''
        {
            {
                \time 3/8
                \set Staff.pedalSustainStyle = #'mixed
                c'8 [ \glissando \sustainOn \startTrillSpan
                d'8 \glissando
                e'8 ] \glissando
            }
            {
                \time 4/8
                c'8 [ \glissando
                d'8 \glissando
                e'8 \glissando
                f'8 ] \sustainOff \stopTrillSpan
            }
        }
        '''
        )

    assert container[0] is measure_2
    assert container[1] is measure_1
    assert len(measure_2) == 3
    assert len(measure_1) == 4
    leaves = tuple(abjad.iterate(container).by_leaf())
    assert pedal.components == leaves
    assert gliss.components == leaves
    assert abjad.inspect(container).is_well_formed()
