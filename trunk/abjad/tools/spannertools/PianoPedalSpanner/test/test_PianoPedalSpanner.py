# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_PianoPedalSpanner_01():
    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.PianoPedalSpanner(t[:])

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
    }
    '''

    assert select(t).is_well_formed()
    assert p.kind == 'sustain'
    assert p.style == 'mixed'
    assert testtools.compare(
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.PianoPedalSpanner(t[:])
    p.kind = 'sostenuto'

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \sostenutoOn
        c'8
        c'8
        c'8 \sostenutoOff
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.PianoPedalSpanner(t[:])
    p.kind = 'corda'

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \unaCorda
        c'8
        c'8
        c'8 \treCorde
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.PianoPedalSpanner(t[:])
    assert p.kind == 'sustain'
    p.style = 'text'

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'text
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.PianoPedalSpanner(t[:])
    assert p.kind == 'sustain'
    p.style = 'bracket'

    r'''
    \new Staff {
        \set Staff.pedalSustainStyle = #'bracket
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(8))
    spannertools.PianoPedalSpanner(t[:4])
    spannertools.PianoPedalSpanner(t[3:])

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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.PianoPedalSpanner(t)

    assert py.test.raises(ValueError, 'p.kind = "abc"')
    assert py.test.raises(ValueError, 'p.style = "abc"')
