from abjad.spanners.ComplexBeamSpanner._ComplexBeamSpannerFormatInterface import _ComplexBeamSpannerFormatInterface
from abjad.tools import durtools


class _MeasuredComplexBeamSpannerFormatInterface(_ComplexBeamSpannerFormatInterface):

   ## PUBLIC ATTRIBUTES ##

   def _before(self, leaf):
      '''Spanner format contribution to output before leaf.'''
      from abjad.components._Measure import _Measure
      from abjad.tools import componenttools
      result = [ ]
      spanner = self.spanner
      #if leaf.beam.beamable:
      if componenttools.is_beamable_component(leaf):
         if spanner._is_exterior_leaf(leaf):
            left, right = self._get_left_right_for_exterior_leaf(leaf)
         elif componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
            leaf, _Measure) is not None:
            measure = componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
               leaf, _Measure)
            # leaf at beginning of measure
            if measure._is_one_of_my_first_leaves(leaf):
               assert isinstance(spanner.span, int)
               left = spanner.span
               #right = leaf.duration._flags
               right = durtools.rational_to_flag_count(leaf.duration.written)
            # leaf at end of measure
            elif measure._is_one_of_my_last_leaves(leaf):
               assert isinstance(spanner.span, int)
               #left = leaf.duration._flags
               left = durtools.rational_to_flag_count(leaf.duration.written)
               right = spanner.span
         else:
            left, right = self._get_left_right_for_interior_leaf(leaf)
         if left is not None:
            result.append(r'\set stemLeftBeamCount = #%s' % left)
         if right is not None:
            result.append(r'\set stemRightBeamCount = #%s' % right)
      return result
