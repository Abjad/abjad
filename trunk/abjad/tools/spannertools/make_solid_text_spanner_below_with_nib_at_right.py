from abjad.markup import Markup
from abjad.spanners.Text import TextSpanner


def make_solid_text_spanner_below_with_nib_at_right(left_text, components = None):
   r'''.. versionadded:: 1.1.2

   Span `components` with text spanner.
   Position spanner below staff and configure with `left_text`,
   solid line and upward-pointing nib at right. ::
   
      abjad> t = Staff(macros.scale(4))
      abjad> spannertools.make_solid_text_spanner_below_with_nib_at_right('foo', t[:])
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
              \revert TextSpanner #'direction
              \revert TextSpanner #'bound-details #'left #'text
              \revert TextSpanner #'dash-fraction
              \revert TextSpanner #'bound-details #'right #'text
              \revert TextSpanner #'bound-details #'right-broken #'text
      }

   .. versionchanged:: 1.1.2
      renamed ``spanners.solid_text_spanner_below_with_nib_at_right( )`` to
      ``spannertools.make_solid_text_spanner_below_with_nib_at_right( )``.
   '''

   text_spanner = TextSpanner(components) 
   left_text = Markup(left_text)
   text_spanner.bound_details__left__text = left_text
   right_text = Markup("(markup #:draw-line '(0 . 1))")
   right_text.style = 'scheme'
   text_spanner.bound_details__right__text = right_text
   text_spanner.bound_details__right_broken__text = False
   text_spanner.dash_fraction = 1
   text_spanner.direction = 'down'

   return text_spanner
