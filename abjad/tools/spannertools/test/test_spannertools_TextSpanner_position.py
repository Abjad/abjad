# -*- coding: utf-8 -*-
import abjad


def test_spannertools_TextSpanner_position_01():

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
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

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, staff[:])
    command = abjad.LilyPondCommand('textSpannerNeutral')
    abjad.attach(command, text_spanner[0])

    assert format(staff) == abjad.String.normalize(
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

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, staff[:])
    command = abjad.LilyPondCommand('textSpannerUp')
    abjad.attach(command, text_spanner[0])

    assert format(staff) == abjad.String.normalize(
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

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, staff[:])
    command = abjad.LilyPondCommand('textSpannerDown')
    abjad.attach(command, text_spanner[0])

    assert format(staff) == abjad.String.normalize(
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
    r'''TextSpanner abjad.attaching to container formats correctly.
    '''

    container = abjad.Container("c'8 c'8 c'8 c'8")
    text_spanner = abjad.TextSpanner()
    abjad.attach(text_spanner, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8 \startTextSpan
            c'8
            c'8
            c'8 \stopTextSpan
        }
        '''
        )
