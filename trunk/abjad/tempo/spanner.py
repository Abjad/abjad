from abjad.spanner.grobhandler import _GrobHandlerSpanner
from abjad.tempo.format import _TempoSpannerFormatInterface
from abjad.tempo.indication import TempoIndication
import types


class Tempo(_GrobHandlerSpanner):

   def __init__(self, music = None, indication = None):
      _GrobHandlerSpanner.__init__(self, 'MetronomeMark', music)
      self._format = _TempoSpannerFormatInterface(self)
      self.indication = indication

   ## PUBLIC ATTRIBUTES ##

   @apply
   def indication( ):
      def fget(self):
         return self._indication
      def fset(self, arg):
         assert isinstance(arg, (TempoIndication, types.NoneType))
         self._indication = arg 
      return property(**locals( ))
