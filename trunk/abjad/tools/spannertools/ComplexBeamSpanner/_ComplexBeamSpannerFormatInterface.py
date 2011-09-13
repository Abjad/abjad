from abjad.tools import durationtools
from abjad.tools.spannertools.BeamSpanner._BeamSpannerFormatInterface import _BeamSpannerFormatInterface


class _ComplexBeamSpannerFormatInterface(_BeamSpannerFormatInterface):

    def __init__(self, spanner):
        _BeamSpannerFormatInterface.__init__(self, spanner)

    ### PRIVATE METHODS ###

    def _get_left_right_for_exterior_leaf(self, leaf):
        '''Get left and right flag counts for exterior leaf in spanner.'''
        spanner = self.spanner
        # lone
        if spanner._is_my_only_leaf(leaf):
            left, right = self._get_left_right_for_lone_leaf(leaf)
        # first
        elif spanner._is_my_first_leaf(leaf) or not leaf._navigator._prev_bead:
            left = 0
            right = durationtools.rational_to_flag_count(leaf.written_duration)
        # last
        elif spanner._is_my_last_leaf(leaf) or not leaf._navigator._next_bead:
            left = durationtools.rational_to_flag_count(leaf.written_duration)
            right = 0
        else:
            raise ValueError('leaf must be first or last in spanner.')
        return left, right

    def _get_left_right_for_interior_leaf(self, leaf):
        '''Interior leaves are neither first nor last in spanner.
        Interior leaves may be surrounded by beamable leaves.
        Interior leaves may be surrounded by unbeamable leaves.
        Four cases total for beamability of surrounding leaves.'''
        from abjad.tools import componenttools
        prev_written = leaf._navigator._prev_bead.written_duration
        cur_written = leaf.written_duration
        next_written = leaf._navigator._next_bead.written_duration
        prev_flag_count = durationtools.rational_to_flag_count(prev_written)
        cur_flag_count = durationtools.rational_to_flag_count(cur_written)
        next_flag_count = durationtools.rational_to_flag_count(next_written)
        # [unbeamable leaf beamable]
        if not componenttools.is_beamable_component(leaf._navigator._prev_bead) and \
            componenttools.is_beamable_component(leaf._navigator._next_bead):
            left = cur_flag_count
            right = min(cur_flag_count, next_flag_count)
        # [beamable leaf unbeamable]
        if componenttools.is_beamable_component(leaf._navigator._prev_bead) and \
            not componenttools.is_beamable_component(leaf._navigator._next_bead):
            left = min(cur_flag_count, prev_flag_count)
            right = cur_flag_count
        # [unbeamable leaf unbeamable]
        elif not componenttools.is_beamable_component(leaf._navigator._prev_bead) and \
            not componenttools.is_beamable_component(leaf._navigator._next_bead):
            left = cur_flag_count
            right = cur_flag_count
        # [beamable leaf beamable]
        else:
            left = min(cur_flag_count, prev_flag_count)
            right = min(cur_flag_count, next_flag_count)
            if left != cur_flag_count and right != cur_flag_count:
                left = cur_flag_count
        return left, right

    def _get_left_right_for_lone_leaf(self, leaf):
        '''Get left and right flag counts for only leaf in spanner.'''
        spanner = self.spanner
        cur_flag_count = durationtools.rational_to_flag_count(leaf.written_duration)
        left, right = None, None
        if spanner.lone == 'left':
            left = cur_flag_count
            right = 0
        elif spanner.lone == 'right':
            left = 0
            right = cur_flag_count
        elif spanner.lone in ('both', True):
            left = cur_flag_count
            right = cur_flag_count
        elif spanner.lone in ('neither', False):
            left = None
            right = None
        else:
            raise ValueError("'lone' must be left, right, both.")
        return left, right

    ### PUBLIC METHODS ###

    def _before(self, leaf):
        '''Spanner format contribution to output before leaf.'''
        from abjad.tools import componenttools
        result = []
        result.extend(_BeamSpannerFormatInterface._before(self, leaf))
        spanner = self.spanner
        if componenttools.is_beamable_component(leaf):
            if spanner._is_my_only_leaf(leaf):
                left, right = self._get_left_right_for_lone_leaf(leaf)
            elif spanner._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                result.append(r'\set stemLeftBeamCount = #%s' % left)
            if right is not None:
                result.append(r'\set stemRightBeamCount = #%s' % right)
        return result

    def _right(self, leaf):
        '''Spanner format contribution to output right of leaf.'''
        from abjad.tools import componenttools
        result = []
        spanner = self.spanner
        #if leaf.beam.beamable:
        if componenttools.is_beamable_component(leaf):
            # lone
            if spanner._is_my_only_leaf(leaf):
                if spanner.lone:
                    result.append('[')
            # otherwise
            elif spanner._is_my_first_leaf(leaf) or not leaf._navigator._prev_bead or \
                not componenttools.is_beamable_component(leaf._navigator._prev_bead):
                result.append('[')
            # lone
            if spanner._is_my_only_leaf(leaf):
                if spanner.lone:
                    result.append(']')
            # otherwise
            elif spanner._is_my_last_leaf(leaf) or not leaf._navigator._next_bead or \
                not componenttools.is_beamable_component(leaf._navigator._next_bead):
                result.append(']')
        return result
