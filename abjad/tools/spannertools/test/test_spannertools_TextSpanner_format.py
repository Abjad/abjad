# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_spannertools_TextSpanner_format_01():

    staff = scoretools.Staff("c'4 d'4 e'4 f'4")
    markup_one = markuptools.Markup('one')
    markup_two = markuptools.Markup('two')
    markup_three = markuptools.Markup('three')
    line_segment = indicatortools.LineSegment()
    arrow = indicatortools.Arrow()
    text_spanner = spannertools.TextSpanner()
    attach(markup_one, staff[0], is_annotation=True)
    attach(line_segment, staff[0])
    attach(markup_two, staff[1], is_annotation=True)
    attach(arrow, staff[1])
    attach(markup_three, staff[-1], is_annotation=True)
    attach(text_spanner, staff[:])

    assert format(staff) == stringtools.normalize(
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

    staff = scoretools.Staff("c'4 d'4 e'4 f'4")
    nonannotated_markup = Markup('leggieriss.')
    attach(nonannotated_markup, staff[0])

    arrow_start = markuptools.Markup('ord.').upright()
    arrow_stop = markuptools.Markup('pont.').upright()
    markup_three = markuptools.Markup('three')
    arrow = indicatortools.Arrow()
    text_spanner = spannertools.TextSpanner()
    attach(arrow_start, staff[0], is_annotation=True)
    attach(arrow, staff[0])
    attach(arrow_stop, staff[-1], is_annotation=True)
    attach(text_spanner, staff[:])

    assert format(staff) == systemtools.TestManager.clean_string(
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

    staff = scoretools.Staff("c'4 d'4 e'4 f'4")
    markup_one = markuptools.Markup('one')
    markup_two = markuptools.Markup('two')
    markup_three = markuptools.Markup('three')
    text_spanner = spannertools.TextSpanner()
    attach(markup_one, staff[0], is_annotation=True)
    attach(markup_two, staff[1], is_annotation=True)
    attach(markup_three, staff[-1], is_annotation=True)
    attach(text_spanner, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'4 ^ \markup { one }
            d'4 ^ \markup { two }
            e'4
            f'4 ^ \markup { three }
        }
        ''')
