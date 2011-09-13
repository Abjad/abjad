from abjad.tools.markuptools import Markup
from abjad.tools.spannertools.TextSpanner import TextSpanner


def make_solid_text_spanner_below_with_nib_at_right(left_text, components = None):
    r'''.. versionadded:: 2.0

    Span `components` with text spanner.
    Position spanner below staff and configure with `left_text`,
    solid line and upward-pointing nib at right. ::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.make_solid_text_spanner_below_with_nib_at_right('foo', t[:])
        TextSpanner(c'8, d'8, e'8, f'8)
        abjad> f(t)
        \new Staff {
            \override TextSpanner #'bound-details #'left #'text = \markup { foo }
            \override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . 1))
            \override TextSpanner #'bound-details #'right-broken #'text = ##f
            \override TextSpanner #'dash-fraction = #1
            \override TextSpanner #'direction = #down
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
        renamed ``spanners.solid_text_spanner_below_with_nib_at_right()`` to
        ``spannertools.make_solid_text_spanner_below_with_nib_at_right()``.
    '''

    text_spanner = TextSpanner(components)
    left_text = Markup(left_text)
    text_spanner.override.text_spanner.bound_details__left__text = left_text
    right_text = Markup("(markup #:draw-line '(0 . 1))", style_string = 'scheme')
    text_spanner.override.text_spanner.bound_details__right__text = right_text
    text_spanner.override.text_spanner.bound_details__right_broken__text = False
    text_spanner.override.text_spanner.dash_fraction = 1
    text_spanner.override.text_spanner.direction = 'down'

    return text_spanner
