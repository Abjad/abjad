# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import override


def make_dynamic_spanner_below_with_nib_at_right(dynamic_text):
    r'''Makes dynamic spanner below with nib at right.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.make_dynamic_spanner_below_with_nib_at_right('mp')
            >>> attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \override TextSpanner.bound-details.left.text = \markup { \dynamic { mp } }
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

    text_spanner = spannertools.TextSpanner()

    string = r'\dynamic {{ {} }}'.format(dynamic_text)
    left_markup = markuptools.Markup(string)

    pair = schemetools.SchemePair(0, 1)
    markup_command = markuptools.MarkupCommand('draw-line', pair)
    right_markup = markuptools.Markup(markup_command)

    grob = override(text_spanner).text_spanner
    grob.bound_details__left__text = left_markup
    grob.bound_details__right__text = right_markup
    grob.bound_details__right_broken__text = False
    grob.dash_fraction = 1
    grob.direction = Down

    return text_spanner
