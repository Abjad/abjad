# -*- encoding: utf-8 -*-
from abjad import *
from py.test import raises


def test_TextSpanner_position_01():

    staff = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(staff[:])

    r'''
    \new Staff {
        c'8 \startTextSpan
        c'8
        c'8
        c'8 \stopTextSpan
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )


def test_TextSpanner_position_02():

    staff = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(staff[:])
    marktools.LilyPondCommandMark('textSpannerNeutral')(p[0])

    r'''
    \new Staff {
        \textSpannerNeutral
        c'8 \startTextSpan
        c'8
        c'8
        c'8 \stopTextSpan
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            \textSpannerNeutral
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )


def test_TextSpanner_position_03():

    staff = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(staff[:])
    marktools.LilyPondCommandMark('textSpannerUp')(p[0])

    r'''
    \new Staff {
        \textSpannerUp
        c'8 \startTextSpan
        c'8
        c'8
        c'8 \stopTextSpan
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            \textSpannerUp
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )


def test_TextSpanner_position_04():

    staff = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(staff[:])
    marktools.LilyPondCommandMark('textSpannerDown')(p[0])

    r'''
    \new Staff {
        \textSpannerDown
        c'8 \startTextSpan
        c'8
        c'8
        c'8 \stopTextSpan
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            \textSpannerDown
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )


def test_TextSpanner_position_05():
    r'''TextSpanner attaching to container formats correctly.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(staff)

    r'''
    \new Staff {
        c'8 \startTextSpan
        c'8
        c'8
        c'8 \stopTextSpan
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )
