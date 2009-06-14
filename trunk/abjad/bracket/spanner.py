from abjad.bracket.format import _BracketSpannerFormatInterface
from abjad.markup import Markup
from abjad.text import Text


class Bracket(Text):
   '''Structural bracket to group any Abjad components
      at composition-time. Defaults to red.'''

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
