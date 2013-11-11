# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import override


def make_dynamic_spanner_below_with_nib_at_right(
    dynamic_text, 
    components=None,
    ):
    r'''Span `components` with text spanner.
    Position spanner below staff and configure with `dynamic_text`,
    solid line and upward-pointing nib at right:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.make_dynamic_spanner_below_with_nib_at_right(
        ...     'mp', staff[:])
        TextSpanner(c'8, d'8, e'8, f'8)

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \override TextSpanner #'bound-details #'left #'text = \markup { \dynamic { mp } }
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

    ::

        >>> show(staff) # doctest: +SKIP

    Returns spanner.
    '''
    from abjad.tools import spannertools

    text_spanner = spannertools.TextSpanner()
    attach(text_spanner, components)
    text_spanner._dynamic_text = dynamic_text
    dynamic_text = markuptools.Markup(r'\dynamic { %s }' % dynamic_text)
    override(text_spanner).text_spanner.bound_details__left__text = dynamic_text
    right_text = markuptools.Markup(
        markuptools.MarkupCommand('draw-line', schemetools.SchemePair(0, 1)))
    override(text_spanner).text_spanner.bound_details__right__text = right_text
    override(text_spanner).text_spanner.bound_details__right_broken__text = False
    override(text_spanner).text_spanner.dash_fraction = 1
    override(text_spanner).text_spanner.direction = Down

    return text_spanner
