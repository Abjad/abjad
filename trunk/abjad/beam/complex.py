from abjad.beam.spanner import Beam
from abjad.duration.rational import Rational

class ComplexBeam(Beam):

   def __init__(self, leaves, durations = None, span = 1, lone = False):
      Beam.__init__(self, leaves)
      self.durations = durations
      self.span = span
      self.lone = lone

   @property
   def _spanPoints(self):
      result = [ ]
      if self.durations is not None:
         result.append(Rational(*self.durations[0]))
         for d in self.durations[1 : ]:
            result.append(result[-1] + Rational(*d))   
      return result

   def _right(self, leaf):
      result = [ ]
      if leaf.beam.beamable:
         if self._isMyFirstLeaf(leaf) or not leaf.prev or \
            not leaf.prev.beam.beamable or (self._isMyOnlyLeaf(leaf) and
            self.lone):
            result.append('[')
         if self._isMyLastLeaf(leaf) or not leaf.next or \
            not leaf.next.beam.beamable or (self._isMyOnlyLeaf(leaf) and
            self.lone):
            result.append(']')
      return result

   def _before(self, leaf):
      result = [ ]
      if leaf.beam.beamable:
         left, right = None, None
         # lone
         if self._isMyOnlyLeaf(leaf):
            if self.lone in (True, False):
               pass
            elif self.lone == 'left':
               left = leaf.beam._flags
               right = 0
            elif self.lone == 'right':
               left = 0
               right = leaf.beam._flags
            elif self.lone == 'both':
               left = leaf.beam._flags
               right = leaf.beam._flags
            else:
               raise ValueError('lone must be left, right or both.')
         # first
         elif self._isMyFirstLeaf(leaf) or not leaf.prev:
            left = 0
            right = leaf.beam._flags
         # last
         elif self._isMyLastLeaf(leaf) or not leaf.next:
            left = leaf.beam._flags
            right = 0
         # just right of span gap
         elif self._durationOffsetInMe(leaf) in self._spanPoints and not \
            (self._durationOffsetInMe(leaf) + leaf.duration.prolated in \
            self._spanPoints):
            assert isinstance(self.span, int)
            left = self.span
            right = leaf.beam._flags
         # just left of span gap
         elif self._durationOffsetInMe(leaf) + leaf.duration.prolated in \
            self._spanPoints and not self._durationOffsetInMe(leaf) in \
            self._spanPoints:
            assert isinstance(self.span, int)
            left = leaf.beam._flags
            right = self.span
         # [unbeamable leaf beamable]
         elif not leaf.prev.beam.beamable and leaf.next.beam.beamable:
            left = leaf.beam._flags
            right = min(leaf.beam._flags, leaf.next.beam._flags)
         # [beamable leaf unbeamable]
         elif leaf.prev.beam.beamable and not leaf.next.beam.beamable:
            left = min(leaf.beam._flags, leaf.prev.beam._flags)
            right = leaf.beam._flags
         # [unbeamable leaf unbeamable]
         elif not leaf.prev.beam.beamable and not leaf.next.beam.beamable:
            left = leaf.beam._flags
            right = leaf.beam._flags
         # [beamable leaf beamable]
         else:
            left = min(leaf.beam._flags, leaf.prev.beam._flags)
            right = min(leaf.beam._flags, leaf.next.beam._flags)
            if left != leaf.beam._flags and right != leaf.beam._flags:
               left = leaf.beam._flags
         if left is not None:
            result.append(r'\set stemLeftBeamCount = #%s' % left)
         if right is not None:
            result.append(r'\set stemRightBeamCount = #%s' % right)
      return result
