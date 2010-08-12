from abjad.spanners.Spanner._PositionalGrobHandlerSpanner import _PositionalGrobHandlerSpanner
from abjad.spanners.Slur._SlurSpannerFormatInterface import _SlurSpannerFormatInterface


class SlurSpanner(_PositionalGrobHandlerSpanner):

   def __init__(self, music = None):
      _PositionalGrobHandlerSpanner.__init__(self, 'Slur', music)
      self._format = _SlurSpannerFormatInterface(self)
      self.position = None
      self.style = None

   ## PRIVATE ATTRIBUTES ##

   _positions = {'neutral':r'\slurNeutral', 'up':r'\slurUp', 
                 'down':r'\slurDown', None:None}

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
