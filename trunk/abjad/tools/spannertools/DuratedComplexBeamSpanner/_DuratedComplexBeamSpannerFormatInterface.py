from abjad.tools import durationtools
from abjad.tools.spannertools.ComplexBeamSpanner._ComplexBeamSpannerFormatInterface import _ComplexBeamSpannerFormatInterface


class _DuratedComplexBeamSpannerFormatInterface(_ComplexBeamSpannerFormatInterface):

    ### PUBLIC METHODS ###

    def _before(self, leaf):
        '''Spanner format contribution to output before leaf.'''
        from abjad.tools import componenttools
        result = []
        spanner = self.spanner
        #if leaf.beam.beamable:
        if componenttools.is_beamable_component(leaf):
            if spanner._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            # just right of span gap
            elif spanner._duration_offset_in_me(leaf) in spanner._span_points and not \
                (spanner._duration_offset_in_me(leaf) + leaf.prolated_duration in \
                spanner._span_points):
                assert isinstance(spanner.span, int)
                left = spanner.span
                #right = leaf.duration._flags
                right = durationtools.rational_to_flag_count(leaf.written_duration)
            # just left of span gap
            elif spanner._duration_offset_in_me(leaf) + leaf.prolated_duration in \
                spanner._span_points and not spanner._duration_offset_in_me(leaf) in \
                spanner._span_points:
                assert isinstance(spanner.span, int)
                #left = leaf.duration._flags
                left = durationtools.rational_to_flag_count(leaf.written_duration)
                right = spanner.span
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                result.append(r'\set stemLeftBeamCount = #%s' % left)
            if right is not None:
                result.append(r'\set stemRightBeamCount = #%s' % right)
        return result
