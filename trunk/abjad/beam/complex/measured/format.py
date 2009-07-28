from abjad.beam.complex.format import _BeamComplexFormatInterface
#from abjad.measure.measure import _Measure


class _BeamComplexMeasuredFormatInterface(_BeamComplexFormatInterface):

   ## PUBLIC ATTRIBUTES ##

   def _before(self, leaf):
      '''Spanner format contribution to output before leaf.'''
      from abjad.measure.measure import _Measure
      from abjad.tools import parenttools
      result = [ ]
      spanner = self.spanner
      if leaf.beam.beamable:
         if spanner._isExteriorLeaf(leaf):
            left, right = self._getLeftRightForExteriorLeaf(leaf)
         #elif leaf.parentage.first(_Measure) is not None:
         elif parenttools.get_first(leaf, _Measure) is not None:
            #measure = leaf.parentage.first(_Measure)
            measure = parenttools.get_first(leaf, _Measure)
            # leaf at beginning of measure
            if measure._isOneOfMyFirstLeaves(leaf):
               assert isinstance(spanner.span, int)
               left = spanner.span
               right = leaf.duration._flags
            # leaf at end of measure
            elif measure._isOneOfMyLastLeaves(leaf):
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
