from abjad.core.backtracking import _BacktrackingInterface
from abjad.core.grobhandler import _GrobHandler
from abjad.core.observer import _Observer
from abjad.spanner.receptor import _SpannerReceptor
from abjad.tempo.indication import TempoIndication
import types


class _TempoInterface(_Observer, _GrobHandler, 
   _BacktrackingInterface, _SpannerReceptor):
   '''Handle LilyPond MetronomeMark grob and Abjad Tempo spanner.

      The implementation of `effective` given here allows for
      tempo indication to be set either be a tempo spanner or
      by a forced value set directly on the tempo interface.
      As such, `_TempoInterface` implements two different and
      competing patterns for the way in which tempo indications
      can be set.

      This probably isn't the best situation and, in fact, the
      implementation will clean up considerably is we allow for
      only one way to set tempo indications, most likely
      through spanners only.

      Both patterns remain for now, though this situation is
      unstable and should probably resolve at some point in 
      the future.'''
   
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
   def effective(self):
      '''Effective tempo governing client.
         Decisions here arbitrate between spanner and forced attribute.'''
      if self.forced:
         return self.forced
      if self.parented:
         return self.spanner_in_parentage.indication
      return _BacktrackingInterface.effective.fget(self)

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result =  [ ] 
      if self.forced or self.change:
         result.append(
            r'\tempo %s=%s' % (self.effective._dotted, self.effective.mark))
      return result
