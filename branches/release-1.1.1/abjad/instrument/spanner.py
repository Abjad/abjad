from abjad.instrument.format import _InstrumentSpannerFormatInterface
from abjad.spanner.spanner import Spanner


class Instrument(Spanner):

   def __init__(self, music = None, long = None, short = None):
      Spanner.__init__(self, music)
      self._format = _InstrumentSpannerFormatInterface(self)
      self.long = long
      self.short = short

   ## PUBLIC ATTRIBUTES ##

   @apply
   def long( ):
      def fget(self):
         return self._long
      def fset(self, arg):
         assert isinstance(arg, str) or arg is None
         self._long = arg
      return property(**locals( ))

   @apply
   def short( ):
      def fget(self):
         return self._short
      def fset(self, arg):
         assert isinstance(arg, str) or arg is None
         self._short = arg
      return property(**locals( ))
