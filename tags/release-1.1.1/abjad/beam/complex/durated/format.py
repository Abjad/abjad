from abjad.beam.complex.format import _BeamComplexFormatInterface


class _BeamComplexDuratedFormatInterface(_BeamComplexFormatInterface):

   ## PUBLIC METHODS ##

   def _before(self, leaf):
      '''Spanner format contribution to output before leaf.'''
      result = [ ]
      spanner = self.spanner
      if leaf.beam.beamable:
         if spanner._isExteriorLeaf(leaf):
            left, right = self._getLeftRightForExteriorLeaf(leaf)
         # just right of span gap
         elif spanner._durationOffsetInMe(leaf) in spanner._spanPoints and not \
            (spanner._durationOffsetInMe(leaf) + leaf.duration.prolated in \
            spanner._spanPoints):
            assert isinstance(spanner.span, int)
            left = spanner.span
            right = leaf.duration._flags
         # just left of span gap
         elif spanner._durationOffsetInMe(leaf) + leaf.duration.prolated in \
            spanner._spanPoints and not spanner._durationOffsetInMe(leaf) in \
            spanner._spanPoints:
            assert isinstance(spanner.span, int)
            left = leaf.duration._flags
            right = spanner.span
         else:
            left, right = self._getLeftRightForInteriorLeaf(leaf)
         if left is not None:
            result.append(r'\set stemLeftBeamCount = #%s' % left)
         if right is not None:
            result.append(r'\set stemRightBeamCount = #%s' % right)
      return result
