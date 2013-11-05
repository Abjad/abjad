# -*- encoding: utf-8 -*-
from abjad import *
from pytest import raises


def test_spannertools_TextSpanner_position_01():

    staff = Staff(scoretools.make_repeated_notes(4))
    text_spanner = spannertools.TextSpanner()
    attach(text_spanner, staff[:])

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


def test_spannertools_TextSpanner_position_02():

    staff = Staff(scoretools.make_repeated_notes(4))
    text_spanner = spannertools.TextSpanner()
    attach(text_spanner, staff[:])
    command = marktools.LilyPondCommandMark('textSpannerNeutral')
    attach(command, text_spanner[0])

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


def test_spannertools_TextSpanner_position_03():

    staff = Staff(scoretools.make_repeated_notes(4))
    text_spanner = spannertools.TextSpanner()
    attach(text_spanner, staff[:])
    command = marktools.LilyPondCommandMark('textSpannerUp')
    attach(command, text_spanner[0])

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


def test_spannertools_TextSpanner_position_04():

    staff = Staff(scoretools.make_repeated_notes(4))
    text_spanner = spannertools.TextSpanner()
    attach(text_spanner, staff[:])
    command = marktools.LilyPondCommandMark('textSpannerDown')
    attach(command, text_spanner[0])

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


def test_spannertools_TextSpanner_position_05():
    r'''TextSpanner attaching to container formats correctly.
    '''

    container = Container(scoretools.make_repeated_notes(4))
    text_spanner = spannertools.TextSpanner()
    attach(text_spanner, container)

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
