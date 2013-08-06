# -*- encoding: utf-8 -*-
from abjad import *
from py.test import raises


def test_TextSpanner_position_01():

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(t[:])

    r'''
    \new Staff {
        c'8 \startTextSpan
        c'8
        c'8
        c'8 \stopTextSpan
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(t[:])
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
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(t[:])
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
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(t[:])
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
        t.lilypond_format,
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

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(t)

    r'''
    \new Staff {
        c'8 \startTextSpan
        c'8
        c'8
        c'8 \stopTextSpan
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )
