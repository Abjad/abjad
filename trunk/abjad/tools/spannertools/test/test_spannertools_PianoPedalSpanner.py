# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_spannertools_PianoPedalSpanner_01():

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[:])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()
    assert piano_pedal_spanner.kind == 'sustain'
    assert piano_pedal_spanner.style == 'mixed'


def test_spannertools_PianoPedalSpanner_02():
    r'''Piano pedal spanner supports sostenuto pedal.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    piano_pedal_spanner.kind = 'sostenuto'
    attach(piano_pedal_spanner, staff[:])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_03():
    r'''Piano pedal spanner supports una corda pedal.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    piano_pedal_spanner.kind = 'corda'
    attach(piano_pedal_spanner, staff[:])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_04():
    r'''PianoPedal spanner supports text style.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[:])
    assert piano_pedal_spanner.kind == 'sustain'
    piano_pedal_spanner.style = 'text'

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_05():
    r'''PianoPedal spanner supports bracket style.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[:])
    assert piano_pedal_spanner.kind == 'sustain'
    piano_pedal_spanner.style = 'bracket'

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_06():
    r'''Consecutive dovetailing PianoPedal spanners format correctly.
    '''

    staff = Staff(notetools.make_repeated_notes(8))
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[:4])
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[3:])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_07():
    r'''The 'kind' and 'style' attributes raise ValueError as needed.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[:])

    assert py.test.raises(ValueError, 'piano_pedal_spanner.kind = "abc"')
    assert py.test.raises(ValueError, 'piano_pedal_spanner.style = "abc"')
