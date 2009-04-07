from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _BeamInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond Beam grob.
      Interface to LilyPond \setStemLeftBeamCount, \setStemRightBeamCount.'''

   def __init__(self, client):
      '''Bind to client, LilyPond Beam grob and Abjad Beam spanner.
         Set 'counts' to (None, None).'''
      from abjad.beam.spanner import Beam
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Beam')
      _SpannerReceptor.__init__(self, (Beam, ))
      self._counts = (None, None)

   ## PUBLIC ATTRIBUTES ##

   @property
   def beamable(self):
      '''True when client is beamable, otherwise False.'''
      from abjad.chord.chord import Chord
      from abjad.note.note import Note
      client = self.client
      flags = client.duration._flags
      return isinstance(client, (Note, Chord)) and 0 < flags

   @property
   def before(self):
      '''Format contribution before leaf.'''
      result = [ ]
      result.extend(_GrobHandler.before.fget(self))
      if self.counts[0] is not None:
         result.append(r'\set stemLeftBeamCount = #%s' % self.counts[0])
      if self.counts[1] is not None:
         result.append(r'\set stemRightBeamCount = #%s' % self.counts[1])
      return result

   @apply
   def counts( ):
      '''Interface to LilyPond \setStemLeftBeamCount, \setStemRightBeamCount.
         Set to nonzero integer, pair or None.'''
      def fget(self):
         return self._counts
      def fset(self, expr):
         if expr is None:
            self._counts = (None, None)
         elif isinstance(expr, int):
            self._counts = (expr, expr)
         elif isinstance(expr, (tuple, list)):
            self._counts = (expr[0], expr[1])
         else:
            raise ValueError('must be nonzero integer, pair or None.')
      return property(**locals( ))
