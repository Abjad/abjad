from .. core.interface import _Interface

class BeamInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Beam', ['Beam'])
      self._counts = (None, None)

   ### PROPERTIES ###

   @property
   def flags(self):
      return self._client.duration.flags

   @property
   def beamable(self):
      return self._client.kind('Note') and self.flags > 0

   @property
   def first(self):
      return self.spanned and self.spanners[0]._isMyFirstLeaf(self._client)

   @property
   def last(self):
      return self.spanned and self.spanners[0]._isMyLastLeaf(self._client)

   @property
   def only(self):
      return self.spanned and self.spanners[0]._isMyOnlyLeaf(self._client)

   ### MANAGED ATTRIBUTES ###

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

   ### METHODS ###

   def bridge(self, n, direction):
      assert isinstance(n, int) and n >=0
      assert direction in ('left', 'right')
      if self.spanned:
         if self.spanners[0]._matchingSpanner(direction = direction):
            self.spanners[0].fuse(direction = direction)
            self.subdivide(n, direction)

   def subdivide(self, n, direction):
      assert isinstance(n, int) and n >= 0 or n is None
      assert direction in ('left', 'right')
      prev = self._client.prev
      next = self._client.next
      if n is None:
         if direction == 'left':
            self.counts = None, self.counts[1]
            if prev:
               prev.beam.counts = prev.beam.counts[0], None
         else:
            self.counts = self.counts[0], None
            if next:
               next.beam.counts = None, next.beam.counts[1]
      else:
         if direction == 'left':
            self.counts = n, self.counts[1]
            prev = self._client.prev
            if prev:
               prev.beam.counts = prev.beam.counts[0], n 
         else:
            self.counts = self.counts[0], n
            next = self._client.next
            if next:
               next.beam.counts = n, next.beam.counts[1]

   ### FORMATTING ###

   @property
   def _before(self):
      result = [ ]
      result.extend(_Interface._before.fget(self))
      if self.counts[0] is not None:
         result.append(r'\set stemLeftBeamCount = #%s' % self.counts[0])
      if self.counts[1] is not None:
         result.append(r'\set stemRightBeamCount = #%s' % self.counts[1])
      return result
