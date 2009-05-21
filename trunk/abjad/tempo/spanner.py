from abjad.spanner.grobhandler import _GrobHandlerSpanner
from abjad.tempo.format import _TempoSpannerFormatInterface
from abjad.tempo.indication import TempoIndication
import types


class Tempo(_GrobHandlerSpanner):
   '''Apply tempo indication to zero or more contiguous components.
      Handle LilyPond MetronomeMark grob.'''

   def __init__(self, music = None, indication = None):
      '''Handle LilyPond MetronomeMark grob. Init tempo indication.'''
      _GrobHandlerSpanner.__init__(self, 'MetronomeMark', music)
      self._format = _TempoSpannerFormatInterface(self)
      self.indication = indication

   ## PUBLIC ATTRIBUTES ##

   @apply
   def indication( ):
      '''Read / write tempo indication.'''
      def fget(self):
         return self._indication
      def fset(self, arg):
         assert isinstance(arg, (TempoIndication, types.NoneType))
         self._indication = arg 
      return property(**locals( ))
