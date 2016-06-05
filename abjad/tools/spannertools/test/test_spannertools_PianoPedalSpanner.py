# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_spannertools_PianoPedalSpanner_01():

    staff = Staff(scoretools.make_repeated_notes(4))
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[:])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()
    assert piano_pedal_spanner.kind == 'sustain'
    assert piano_pedal_spanner.style == 'mixed'


def test_spannertools_PianoPedalSpanner_02():
    r'''Piano pedal spanner supports sostenuto pedal.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    piano_pedal_spanner = spannertools.PianoPedalSpanner(kind='sostenuto')
    attach(piano_pedal_spanner, staff[:])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_03():
    r'''Piano pedal spanner supports una corda pedal.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    piano_pedal_spanner = spannertools.PianoPedalSpanner(kind='corda')
    attach(piano_pedal_spanner, staff[:])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_04():
    r'''PianoPedal spanner supports text style.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    piano_pedal_spanner = spannertools.PianoPedalSpanner(
        kind='sustain',
        style='text',
        )
    attach(piano_pedal_spanner, staff[:])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_05():
    r'''PianoPedal spanner supports bracket style.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    piano_pedal_spanner = spannertools.PianoPedalSpanner(
        kind='sustain',
        style='bracket',
        )
    attach(piano_pedal_spanner, staff[:])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_PianoPedalSpanner_06():
    r'''Consecutive dovetailing PianoPedal spanners format correctly.
    '''

    staff = Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[:4])
    piano_pedal_spanner = spannertools.PianoPedalSpanner()
    attach(piano_pedal_spanner, staff[3:])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()
