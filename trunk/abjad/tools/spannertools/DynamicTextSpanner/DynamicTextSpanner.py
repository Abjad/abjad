from abjad.tools.spannertools.DynamicTextSpanner._DynamicTextSpannerFormatInterface import \
   _DynamicTextSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class DynamicTextSpanner(Spanner):
   '''Abjad dynamic text spanner.

   Return dynamic text spanner.
   '''

   def __init__(self, components, mark):
      Spanner.__init__(self, components)
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
