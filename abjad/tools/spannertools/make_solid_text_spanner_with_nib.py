# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import override


def make_solid_text_spanner_with_nib(
    left_text,
    direction=Up,
    ):
    r'''Makes solid text spanner with nib at right.

    ..  container:: example

        Solid text spanner forced above staff:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.make_solid_text_spanner_with_nib(
            ...     'foo',
            ...     direction=Up,
            ...     )
            >>> attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \override TextSpanner.bound-details.left.text = \markup { foo }
                \override TextSpanner.bound-details.right-broken.text = ##f
                \override TextSpanner.bound-details.right.text = \markup {
                    \draw-line
                        #'(0 . -1)
                    }
                \override TextSpanner.dash-fraction = #1
                \override TextSpanner.direction = #up
                c'8 \startTextSpan
                d'8
                e'8
                f'8 \stopTextSpan
                \revert TextSpanner.bound-details
                \revert TextSpanner.dash-fraction
                \revert TextSpanner.direction
            }

    ..  container:: example

        Solid text spanner forced below staff:

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.make_solid_text_spanner_with_nib(
            ...     'foo',
            ...     direction=Down,
            ...     )
            >>> attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \override TextSpanner.bound-details.left.text = \markup { foo }
                \override TextSpanner.bound-details.right-broken.text = ##f
                \override TextSpanner.bound-details.right.text = \markup {
                    \draw-line
                        #'(0 . 1)
                    }
                \override TextSpanner.dash-fraction = #1
                \override TextSpanner.direction = #down
                c'8 \startTextSpan
                d'8
                e'8
                f'8 \stopTextSpan
                \revert TextSpanner.bound-details
                \revert TextSpanner.dash-fraction
                \revert TextSpanner.direction
            }

    Returns text spanner.
    '''
    from abjad.tools import spannertools
    assert direction in (Up, Down)

    text_spanner = spannertools.TextSpanner()
    left_text = markuptools.Markup(left_text)
    override(text_spanner).text_spanner.bound_details__left__text = left_text
    if direction == Up:
        pair = schemetools.SchemePair(0, -1)
    else:
        pair = schemetools.SchemePair(0, 1)
    right_text = markuptools.Markup(
        markuptools.MarkupCommand('draw-line', pair))
    override(text_spanner).text_spanner.bound_details__right__text = right_text
    override(text_spanner).text_spanner.bound_details__right_broken__text = \
        False
    override(text_spanner).text_spanner.dash_fraction = 1
    override(text_spanner).text_spanner.direction = direction

    return text_spanner
