from abjad.markup import Markup
from abjad.spanners.bracket.format import _BracketSpannerFormatInterface
from abjad.spanners.text import Text


class Bracket(Text):
   r'''Structural bracket to group any Abjad components at 
   composition-time. Defaults to red. ::
   
      abjad> t = Staff(construct.scale(4))
      abjad> Bracket(t[:])
      Bracket(c'8, d'8, e'8, f'8)

      abjad> print t.format
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

   .. note:: The Abjad :class:`~abjad.bracket.spanner.Bracket` formats as
      a LillyPond TextSpanner. The large number of \overrides and \reverts
      shown above are necessary to draw a 1.5-unit thick solid red spanner
      with nibs at the beginning and end but with no nibs at line breaks.
      These values may all be overriden after creating the bracket.
   '''

   def __init__(self, music = None):
      Text.__init__(self, music)
      self._format = _BracketSpannerFormatInterface(self)
      self.bound_details__left__text = \
         Markup("(markup #:draw-line '(0 . -1))")
      self.bound_details__left__text.style = 'scheme'
      self.bound_details__left_broken__text = False
      self.bound_details__right__text = \
         Markup("(markup #:draw-line '(0 . -1))")
      self.bound_details__right__text.style = 'scheme'
      self.bound_details__right_broken__text = False
      self.color = 'red'
      self.dash_fraction = 1
      self.staff_padding = 2
      self.thickness = 1.5
