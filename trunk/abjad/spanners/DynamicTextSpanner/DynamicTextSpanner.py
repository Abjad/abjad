from abjad.spanners.DynamicTextSpanner._DynamicTextSpannerFormatInterface import \
   _DynamicTextSpannerFormatInterface
from abjad.spanners.Spanner._GrobHandlerSpanner import _GrobHandlerSpanner


class DynamicTextSpanner(_GrobHandlerSpanner):

   def __init__(self, music, mark):
      _GrobHandlerSpanner.__init__(self, 'DynamicText', music)
      self._format = _DynamicTextSpannerFormatInterface(self)
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
