# -*- coding: utf-8 -*-
import abjad
import pytest


def test_spannertools_TextSpanner_format_01():

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    markup_one = abjad.Markup('one')
    markup_two = abjad.Markup('two')
    markup_three = abjad.Markup('three')
    line_segment = abjad.LineSegment()
    arrow = abjad.Arrow()
    text_spanner = abjad.TextSpanner()
    abjad.attach(markup_one, staff[0], is_annotation=True)
    abjad.attach(line_segment, staff[0])
    abjad.attach(markup_two, staff[1], is_annotation=True)
    abjad.attach(arrow, staff[1])
    abjad.attach(markup_three, staff[-1], is_annotation=True)
    abjad.attach(text_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \once \override TextSpanner.bound-details.left.text = \markup { one }
            c'4 \startTextSpan
            \once \override TextSpanner.arrow-width = 0.25
            \once \override TextSpanner.bound-details.left-broken.text = ##f
            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
            \once \override TextSpanner.bound-details.left.text = \markup {
                \concat
                    {
                        two
                        \hspace
                            #0.25
                    }
                }
            \once \override TextSpanner.bound-details.right-broken.padding = 0
            \once \override TextSpanner.bound-details.right.arrow = ##t
            \once \override TextSpanner.bound-details.right.padding = 1.5
            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
            \once \override TextSpanner.dash-fraction = 1
            d'4 \stopTextSpan \startTextSpan
            e'4
            f'4 \stopTextSpan ^ \markup { three }
        }
        ''')


def test_spannertools_TextSpanner_format_02():
    r'''Regression test: makes sure text spanner ignores nonannotated markup;
    also makes sure nonannotated markup formats and appears in LilyPond
    output.
    '''

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    nonannotated_markup = abjad.Markup('leggieriss.')
    abjad.attach(nonannotated_markup, staff[0])

    arrow_start = abjad.Markup('ord.').upright()
    arrow_stop = abjad.Markup('pont.').upright()
    markup_three = abjad.Markup('three')
    arrow = abjad.Arrow()
    text_spanner = abjad.TextSpanner()
    abjad.attach(arrow_start, staff[0], is_annotation=True)
    abjad.attach(arrow, staff[0])
    abjad.attach(arrow_stop, staff[-1], is_annotation=True)
    abjad.attach(text_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \once \override TextSpanner.arrow-width = 0.25
            \once \override TextSpanner.bound-details.left-broken.text = ##f
            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
            \once \override TextSpanner.bound-details.left.text = \markup {
                \concat
                    {
                        \upright
                            ord.
                        \hspace
                            #0.25
                    }
                }
            \once \override TextSpanner.bound-details.right-broken.padding = 0
            \once \override TextSpanner.bound-details.right.arrow = ##t
            \once \override TextSpanner.bound-details.right.padding = 1.5
            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
            \once \override TextSpanner.dash-fraction = 1
            c'4 \startTextSpan - \markup { leggieriss. }
            d'4
            e'4
            f'4 \stopTextSpan ^ \markup {
                \upright
                    pont.
                }
        }
        ''')


def test_spannertools_TextSpanner_format_03():

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    markup_one = abjad.Markup('one')
    markup_two = abjad.Markup('two')
    markup_three = abjad.Markup('three')
    text_spanner = abjad.TextSpanner()
    abjad.attach(markup_one, staff[0], is_annotation=True)
    abjad.attach(markup_two, staff[1], is_annotation=True)
    abjad.attach(markup_three, staff[-1], is_annotation=True)
    abjad.attach(text_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4 ^ \markup { one }
            d'4 ^ \markup { two }
            e'4
            f'4 ^ \markup { three }
        }
        ''')
