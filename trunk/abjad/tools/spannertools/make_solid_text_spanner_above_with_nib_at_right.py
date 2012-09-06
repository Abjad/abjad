from abjad.tools import markuptools
from abjad.tools import schemetools


def make_solid_text_spanner_above_with_nib_at_right(left_text, components=None):
    r'''.. versionadded:: 2.0

    Span `components` with text spanner.
    Position spanner above staff and configure with `left_text`,
    solid line and downward-pointing nib at right. ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> spannertools.make_solid_text_spanner_above_with_nib_at_right('foo', t[:])
        TextSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(t)
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
            \revert TextSpanner #'bound-details #'left #'text
            \revert TextSpanner #'bound-details #'right #'text
            \revert TextSpanner #'bound-details #'right-broken #'text
            \revert TextSpanner #'dash-fraction
            \revert TextSpanner #'direction
        }

    .. versionchanged:: 2.0
        renamed ``spanners.solid_text_spanner_above_with_nib_at_right()`` to
        ``spannertools.make_solid_text_spanner_above_with_nib_at_right()``.
    '''
    from abjad.tools import spannertools

    text_spanner = spannertools.TextSpanner(components)
    left_text = markuptools.Markup(left_text)
    text_spanner.override.text_spanner.bound_details__left__text = left_text
    right_text = markuptools.Markup(markuptools.MarkupCommand('draw-line', schemetools.SchemePair(0, -1)))
    text_spanner.override.text_spanner.bound_details__right__text = right_text
    text_spanner.override.text_spanner.bound_details__right_broken__text = False
    text_spanner.override.text_spanner.dash_fraction = 1
    text_spanner.override.text_spanner.direction = Up

    return text_spanner
