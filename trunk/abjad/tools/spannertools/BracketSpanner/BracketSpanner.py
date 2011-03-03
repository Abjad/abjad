from abjad.tools.markuptools import Markup
from abjad.tools.spannertools.BracketSpanner._BracketSpannerFormatInterface import _BracketSpannerFormatInterface
from abjad.tools.spannertools.TextSpanner import TextSpanner


class BracketSpanner(TextSpanner):
   r'''Abjad bracket spanner::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> spannertools.BracketSpanner(staff[:])
      spannertools.BracketSpanner(c'8, d'8, e'8, f'8)

   ::

      abjad> f(staff)
      \new Staff {
              \override TextSpanner #'dash-fraction = #1
              \override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))
              \override TextSpanner #'staff-padding = #2
              \override TextSpanner #'color = #red
              \override TextSpanner #'thickness = #1.5
              \override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))
              \override TextSpanner #'bound-details #'right-broken #'text = ##f
              \override TextSpanner #'bound-details #'left-broken #'text = ##f
              c'8 \startTextSpan
              d'8
              e'8
              f'8 \stopTextSpan
              \revert TextSpanner #'dash-fraction
              \revert TextSpanner #'bound-details #'left #'text
              \revert TextSpanner #'staff-padding
              \revert TextSpanner #'color
              \revert TextSpanner #'thickness
              \revert TextSpanner #'bound-details #'right #'text
              \revert TextSpanner #'bound-details #'right-broken #'text
              \revert TextSpanner #'bound-details #'left-broken #'text
      }
   
   Render 1.5-unit thick solid red spanner.

   Draw nibs at beginning and end of spanner.

   Do not draw nibs at line breaks.

   Return bracket spanner.
   '''

   def __init__(self, components = None):
      TextSpanner.__init__(self, components)
      self._format = _BracketSpannerFormatInterface(self)
      self.override.text_spanner.bound_details__left__text = Markup(
            "(markup #:draw-line '(0 . -1))", style_string = 'scheme')
      self.override.text_spanner.bound_details__left_broken__text = False
      self.override.text_spanner.bound_details__right__text = Markup(
         "(markup #:draw-line '(0 . -1))", style_string = 'scheme')
      self.override.text_spanner.bound_details__right_broken__text = False
      self.override.text_spanner.color = 'red'
      self.override.text_spanner.dash_fraction = 1
      self.override.text_spanner.staff_padding = 2
      self.override.text_spanner.thickness = 1.5
