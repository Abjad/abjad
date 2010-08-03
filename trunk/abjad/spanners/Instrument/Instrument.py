from abjad.markup import Markup
from abjad.spanners.instrument.format import _InstrumentSpannerFormatInterface
from abjad.spanners.Spanner.spanner import Spanner
import types


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
         #assert isinstance(arg, str) or arg is None
         #self._long = arg
         if isinstance(arg, types.NoneType):
            self._long = arg
         else:
            markup = Markup(arg)
            self._long = markup
      return property(**locals( ))

   @apply
   def short( ):
      def fget(self):
         return self._short
      def fset(self, arg):
         #assert isinstance(arg, str) or arg is None
         #self._short = arg
         if isinstance(arg, types.NoneType):
            self._short = arg
         else:
            markup = Markup(arg)
            self._short = markup
      return property(**locals( ))
