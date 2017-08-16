import abjad
import pytest


def test_spannertools_PianoPedalSpanner_01():

    staff = abjad.Staff([abjad.Note("c'8"), abjad.Note("c'8"), abjad.Note("c'8"), abjad.Note("c'8")])
    piano_pedal_spanner = abjad.PianoPedalSpanner()
    abjad.attach(piano_pedal_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set Staff.pedalSustainStyle = #'mixed
            c'8 \sustainOn
            c'8
            c'8
            c'8 \sustainOff
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
    assert piano_pedal_spanner.kind == 'sustain'
    assert piano_pedal_spanner.style == 'mixed'


def test_spannertools_PianoPedalSpanner_02():
    r'''Piano pedal spanner supports sostenuto pedal.
    '''

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    piano_pedal_spanner = abjad.PianoPedalSpanner(kind='sostenuto')
    abjad.attach(piano_pedal_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set Staff.pedalSustainStyle = #'mixed
            c'8 \sostenutoOn
            c'8
            c'8
            c'8 \sostenutoOff
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_03():
    r'''Piano pedal spanner supports una corda pedal.
    '''

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    piano_pedal_spanner = abjad.PianoPedalSpanner(kind='corda')
    abjad.attach(piano_pedal_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set Staff.pedalSustainStyle = #'mixed
            c'8 \unaCorda
            c'8
            c'8
            c'8 \treCorde
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_04():
    r'''PianoPedal spanner supports text style.
    '''

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    piano_pedal_spanner = abjad.PianoPedalSpanner(
        kind='sustain',
        style='text',
        )
    abjad.attach(piano_pedal_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set Staff.pedalSustainStyle = #'text
            c'8 \sustainOn
            c'8
            c'8
            c'8 \sustainOff
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_05():
    r'''PianoPedal spanner supports bracket style.
    '''

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    piano_pedal_spanner = abjad.PianoPedalSpanner(
        kind='sustain',
        style='bracket',
        )
    abjad.attach(piano_pedal_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set Staff.pedalSustainStyle = #'bracket
            c'8 \sustainOn
            c'8
            c'8
            c'8 \sustainOff
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_06():
    r'''Consecutive dovetailing PianoPedal spanners format correctly.
    '''

    staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    piano_pedal_spanner = abjad.PianoPedalSpanner()
    abjad.attach(piano_pedal_spanner, staff[:4])
    piano_pedal_spanner = abjad.PianoPedalSpanner()
    abjad.attach(piano_pedal_spanner, staff[3:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set Staff.pedalSustainStyle = #'mixed
            c'8 \sustainOn
            c'8
            c'8
            \set Staff.pedalSustainStyle = #'mixed
            c'8 \sustainOff \sustainOn
            c'8
            c'8
            c'8
            c'8 \sustainOff
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
