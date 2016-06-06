# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools.topleveltools import override


def make_colored_text_spanner_with_nibs():
    r'''Makes colored text spanner with nibs.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.make_colored_text_spanner_with_nibs()
            >>> attach(spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \override TextSpanner.bound-details.left-broken.text = ##f
                \override TextSpanner.bound-details.left.text = \markup {
                    \draw-line
                        #'(0 . -1)
                    }
                \override TextSpanner.bound-details.right-broken.text = ##f
                \override TextSpanner.bound-details.right.text = \markup {
                    \draw-line
                        #'(0 . -1)
                    }
                \override TextSpanner.color = #red
                \override TextSpanner.dash-fraction = #1
                \override TextSpanner.staff-padding = #2
                \override TextSpanner.thickness = #1.5
                c'8 \startTextSpan
                d'8
                e'8
                f'8 \stopTextSpan
                \revert TextSpanner.bound-details
                \revert TextSpanner.color
                \revert TextSpanner.dash-fraction
                \revert TextSpanner.staff-padding
                \revert TextSpanner.thickness
            }

    Renders 1.5-unit thick solid red spanner.

    Draws nibs at beginning and end of spanner.

    Does not draw nibs at line breaks.

    Returns bracket spanner.
    '''
    from abjad.tools import spannertools

    spanner = spannertools.TextSpanner()
    pair = schemetools.SchemePair(0, -1)
    markup_command = markuptools.MarkupCommand('draw-line', pair)
    markup = markuptools.Markup(markup_command)
    override(spanner).text_spanner.bound_details__left__text = markup
    override(spanner).text_spanner.bound_details__left_broken__text = False
    markup = markuptools.Markup(markup)
    override(spanner).text_spanner.bound_details__right__text = markup
    override(spanner).text_spanner.bound_details__right_broken__text = False
    override(spanner).text_spanner.color = 'red'
    override(spanner).text_spanner.dash_fraction = 1
    override(spanner).text_spanner.staff_padding = 2
    override(spanner).text_spanner.thickness = 1.5

    return spanner
