# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools


def make_solid_text_spanner_with_nib(
    left_text, 
    components=None,
    direction=Up,
    ):
    r'''Span `components` with solid line text spanner.
    Configure with `left_text` and nib at right.

    ..  container:: example

        **Example 1.** Spanner above with downward-pointing nib:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.make_solid_text_spanner_with_nib(
            ...     'foo', staff[:], direction=Up)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \override TextSpanner #'bound-details #'left #'text = \markup { foo }
                \override TextSpanner #'bound-details #'right #'text = \markup {
                    \draw-line #'(0 . -1) }
                \override TextSpanner #'bound-details #'right-broken #'text = ##f
                \override TextSpanner #'dash-fraction = #1
                \override TextSpanner #'direction = #up
                c'8 \startTextSpan
                d'8
                e'8
                f'8 \stopTextSpan
                \revert TextSpanner #'bound-details
                \revert TextSpanner #'dash-fraction
                \revert TextSpanner #'direction
            }

    ..  container:: example

        **Example 2.** Spanner below with upward-pointing nib:

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.make_solid_text_spanner_with_nib(
            ...     'foo', staff[:], direction=Down)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \override TextSpanner #'bound-details #'left #'text = \markup { foo }
                \override TextSpanner #'bound-details #'right #'text = \markup { \draw-line #'(0 . 1) }
                \override TextSpanner #'bound-details #'right-broken #'text = ##f
                \override TextSpanner #'dash-fraction = #1
                \override TextSpanner #'direction = #down
                c'8 \startTextSpan
                d'8
                e'8
                f'8 \stopTextSpan
                \revert TextSpanner #'bound-details
                \revert TextSpanner #'dash-fraction
                \revert TextSpanner #'direction
            }

    Returns spanner.
    '''
    from abjad.tools import spannertools
    from abjad.tools.scoretools import attach
    assert direction in (Up, Down)

    text_spanner = spannertools.TextSpanner()
    attach(text_spanner, components)
    left_text = markuptools.Markup(left_text)
    text_spanner.override.text_spanner.bound_details__left__text = left_text
    if direction is Up:
        pair = schemetools.SchemePair(0, -1)
    else:
        pair = schemetools.SchemePair(0, 1)
    right_text = markuptools.Markup(
        markuptools.MarkupCommand('draw-line', pair))
    text_spanner.override.text_spanner.bound_details__right__text = right_text
    text_spanner.override.text_spanner.bound_details__right_broken__text = \
        False
    text_spanner.override.text_spanner.dash_fraction = 1
    text_spanner.override.text_spanner.direction = direction

    return text_spanner
