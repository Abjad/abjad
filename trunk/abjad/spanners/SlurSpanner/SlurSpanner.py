from abjad.spanners.Spanner import Spanner
from abjad.spanners.SlurSpanner._SlurSpannerFormatInterface import _SlurSpannerFormatInterface


class SlurSpanner(Spanner):

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _SlurSpannerFormatInterface(self)
      self.style = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def style( ):
      def fget(self):
         return self._style
      def fset(self, expr):
         if expr is None:
            self._style = expr
         elif expr in ('solid', 'dotted', 'dashed'):
            self._style = expr
         else:
            raise ValueError("must be 'solid', 'dotted', 'dashed', or None.")
      return property(**locals( ))
