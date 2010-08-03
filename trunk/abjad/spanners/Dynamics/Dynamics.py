from abjad.spanners.dynamics.format import _DynamicSpannerFormatInterface
from abjad.spanners.Spanner.grobhandler import _GrobHandlerSpanner


class Dynamic(_GrobHandlerSpanner):

   def __init__(self, music, mark):
      _GrobHandlerSpanner.__init__(self, 'DynamicText', music)
      self._format = _DynamicSpannerFormatInterface(self)
      self.mark = mark

   ## PUBLIC ATTRIBUTES ##

   @apply
   def mark( ):
      def fget(self):
         return self._mark
      def fset(self, arg):
         assert isinstance(arg, str)
         self._mark = arg
      return property(**locals( ))
