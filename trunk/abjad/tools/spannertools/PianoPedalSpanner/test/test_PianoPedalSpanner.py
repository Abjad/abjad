# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_PianoPedalSpanner_01():
    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal = spannertools.PianoPedalSpanner(staff[:])

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
    }
    '''

    assert select(staff).is_well_formed()
    assert piano_pedal.kind == 'sustain'
    assert piano_pedal.style == 'mixed'
    assert testtools.compare(
        staff.lilypond_format,
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


def test_PianoPedalSpanner_02():
    r'''PianoPedal spanner supports sostenuto pedal.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal = spannertools.PianoPedalSpanner(staff[:])
    piano_pedal.kind = 'sostenuto'

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \sostenutoOn
        c'8
        c'8
        c'8 \sostenutoOff
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
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


def test_PianoPedalSpanner_03():
    r'''PianoPedal spanner supports una corda pedal.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal = spannertools.PianoPedalSpanner(staff[:])
    piano_pedal.kind = 'corda'

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \unaCorda
        c'8
        c'8
        c'8 \treCorde
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
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


def test_PianoPedalSpanner_04():
    r'''PianoPedal spanner supports text style.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal = spannertools.PianoPedalSpanner(staff[:])
    assert piano_pedal.kind == 'sustain'
    piano_pedal.style = 'text'

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'text
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
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


def test_PianoPedalSpanner_05():
    r'''PianoPedal spanner supports bracket style.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal = spannertools.PianoPedalSpanner(staff[:])
    assert piano_pedal.kind == 'sustain'
    piano_pedal.style = 'bracket'

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'bracket
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
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


def test_PianoPedalSpanner_06():
    r'''Consecutive dovetailing PianoPedal spanners format correctly.
    '''

    staff = Staff(notetools.make_repeated_notes(8))
    spannertools.PianoPedalSpanner(staff[:4])
    spannertools.PianoPedalSpanner(staff[3:])

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

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
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


def test_PianoPedalSpanner_07():
    r'''The 'kind' and 'style' attributes raise ValueError as needed.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal = spannertools.PianoPedalSpanner(staff)

    assert py.test.raises(ValueError, 'piano_pedal.kind = "abc"')
    assert py.test.raises(ValueError, 'piano_pedal.style = "abc"')
