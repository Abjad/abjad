from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor
from abjad.tempo.indication import TempoIndication
import types


class _TempoInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond MetronomeMark grob and Abjad Tempo spanner.'''
   
   def __init__(self, client):
      '''Bind to client and LilyPond MetronomMark grob.
         Receive Abjad Tempo spanner.'''
      from abjad.tempo.spanner import Tempo
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'MetronomeMark')
      _SpannerReceptor.__init__(self, (Tempo, ))
      self._indication = None
 
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

   ## PUBLIC METHODS ##

   ## TODO: Replace interface clear( ) method with override interface ##

   def clear(self):
      self.indication = None
      _GrobHandler.clear(self)

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result =  [ ] 
      if self.indication is not None:
         result.append(
            r'\tempo %s=%s' % (self.indication.dotted, self.indication.mark))
      return result
