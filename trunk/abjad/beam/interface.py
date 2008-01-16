from .. core.interface import _Interface

class BeamInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Beam')
      self.counts = None

   @property
   def _beam(self):
      beams = self._client.spanners.get(classname = 'Beam')
      if beams:
         return beams[0]
      else:
         return None

   ### PUBLIC ###

   @property
   def flags(self):
      return self._client.duration.flags

   @property
   def beamable(self):
      return self._client.kind('Note') and self.flags > 0

   @property
   def beamed(self):
      return bool(self._beam)

   @property
   def first(self):
      return self._beam and self._beam._isMyFirstLeaf(self._client)

   @property
   def last(self):
      return self._beam and self._beam._isMyLastLeaf(self._client)

   @property
   def only(self):
      return self._beam and self._beam._isMyOnlyLeaf(self._client)

   ### ACCESSORS ###

   ### TODO - eliminate setLeftCount, setRightCount, setBothCounts, clear
   ###        in favor of a single managed attribute:
   ###        self.counts = (3, 0), etc.;
   ###        simplify the interface here by four methods.

   def setLeftCount(self, l = None):
      if not l:
         self.counts = (self.flags, 0)
      else:
         self.counts = (l, 0)

   def setRightCount(self, r = None):
      if not r:
         self.counts = (0, self.flags)
      else:
         self.counts = (0, r)

   def setBothCounts(self, l = None, r = None):
      if not l and not r:
         self.counts = (self.flags, self.flags)
      else:
         self.counts = (l, r)

   def clear(self):
      self.counts = None

   def spanRight(self, span = 1):
      if self.beamed:
         if self._beam._matchingSpannerAfterMe( ):
            #self._beam.fuseRight( )
            self._beam.fuse(direction = 'right')
            self.counts = self.counts[0], span
            next = self._client.next
            next.beam.counts = span, next.beam.counts[-1]

   def spanLeft(self, span = 1):
      if self.beamed:
         if self._beam._matchingSpannerBeforeMe( ):
            #self._beam.fuseLeft( )
            self._beam.fuse(direction = 'left')
            self.counts = span, self.counts[-1]
            prev = self._client.prev
            prev.beam.counts = prev.counts[0], span

   ### FORMATTING ###

   @property
   def _left(self):
      result = [ ]
      if self.counts:
         result.append(r'\beam #%s #%s' % self.counts)
      return result
