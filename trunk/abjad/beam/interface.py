from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _BeamInterface(_Interface, _GrobHandler, _SpannerReceptor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Beam')
      _SpannerReceptor.__init__(self, ['Beam'])
      self._counts = (None, None)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _before(self):
      result = [ ]
      result.extend(_GrobHandler._before.fget(self))
      if self.counts[0] is not None:
         result.append(r'\set stemLeftBeamCount = #%s' % self.counts[0])
      if self.counts[1] is not None:
         result.append(r'\set stemRightBeamCount = #%s' % self.counts[1])
      return result

   @property
   def _flags(self):
      return self._client.duration._flags

   ## PUBLIC ATTRIBUTES ##

   @property
   def beamable(self):
      return self._client.kind(('Note', 'Chord')) and \
         self._flags > 0 and not getattr(self, '_refuse', False)

   @property
   def closing(self):
      return self.spanned and ']' in self.spanner._right(self._client)

   @apply
   def counts( ):
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

   @property
   def opening(self):
      return self.spanned and '[' in self.spanner._right(self._client)
