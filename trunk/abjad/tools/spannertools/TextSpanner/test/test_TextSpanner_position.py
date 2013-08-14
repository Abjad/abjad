# -*- encoding: utf-8 -*-
from abjad import *
from py.test import raises


def test_TextSpanner_position_01():

    staff = Staff(notetools.make_repeated_notes(4))
    text_spanner = spannertools.TextSpanner(staff[:])

    assert testtools.compare(
        staff,
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
    text_spanner = spannertools.TextSpanner(staff[:])
    marktools.LilyPondCommandMark('textSpannerNeutral')(text_spanner[0])

    assert testtools.compare(
        staff,
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
    text_spanner = spannertools.TextSpanner(staff[:])
    marktools.LilyPondCommandMark('textSpannerUp')(text_spanner[0])

    assert testtools.compare(
        staff,
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
    text_spanner = spannertools.TextSpanner(staff[:])
    marktools.LilyPondCommandMark('textSpannerDown')(text_spanner[0])

    assert testtools.compare(
        staff,
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

    container = Container(notetools.make_repeated_notes(4))
    text_spanner = spannertools.TextSpanner(container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )
