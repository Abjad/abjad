from abjad.core.backtracking import _BacktrackingInterface
from abjad.core.grobhandler import _GrobHandler
from abjad.core.observer import _Observer
from abjad.spanner.receptor import _SpannerReceptor
from abjad.tempo.indication import TempoIndication
import types


class _TempoInterface(_Observer, _GrobHandler, 
   _BacktrackingInterface, _SpannerReceptor):
   '''Handle LilyPond MetronomeMark grob and Abjad Tempo spanner.'''
   
   def __init__(self, _client, _updateInterface):
      '''Bind to client and LilyPond MetronomMark grob.
         Receive Abjad Tempo spanner.'''
      from abjad.tempo.spanner import Tempo
      _Observer.__init__(self, _client, _updateInterface)
      _GrobHandler.__init__(self, 'MetronomeMark')
      _BacktrackingInterface.__init__(self, 'tempo')
      _SpannerReceptor.__init__(self, (Tempo, ))
      self._acceptableTypes = (TempoIndication, types.NoneType)
      self._effective = None
      self._forced = None
 
   ## PUBLIC ATTRIBUTES ##

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result =  [ ] 
      if self.forced or self.change:
         result.append(
            r'\tempo %s=%s' % (self.effective._dotted, self.effective.mark))
      return result
