from abjad.tools.beamtools.ComplexBeamSpanner import ComplexBeamSpanner
from abjad.tools import durationtools
from abjad.tools import sequencetools


class DuratedComplexBeamSpanner(ComplexBeamSpanner):
    r'''Abjad durated complex beam spanner::

        staff = Staff("c'16 d'16 e'16 f'16")

    ::

        durations = [Duration(1, 8), Duration(1, 8)]
        beam = beamtools.DuratedComplexBeamSpanner(staff[:], durations, 1)

    ::

        f(staff)
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #1
            d'16
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #2
            e'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 ]
        }

    Beam all beamable leaves in spanner explicitly.

    Group leaves in spanner according to `durations`.

    Span leaves between duration groups according to `span`.

    Return durated complex beam spanner.
    '''

    def __init__(self, components=None, durations=None, span=1, lone=False, direction=None):
        ComplexBeamSpanner.__init__(self, components=components, direction=direction)
        self.durations = durations
        self.span = span
        self.lone = lone

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _span_points(self):
        result = []
        if self.durations is not None:
            result.append(self.durations[0])
            for d in self.durations[1:]:
                result.append(result[-1] + d)
        return result

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        ComplexBeamSpanner._copy_keyword_args(self, new)
        new.durations = self.durations[:]
        new.span = self.span
            
    def _format_before_leaf(self, leaf):
        from abjad.tools import beamtools
        result = []
        #if leaf.beam.beamable:
        if beamtools.is_beamable_component(leaf):
            if self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            # just right of span gap
            elif self._duration_offset_in_me(leaf) in self._span_points and not \
                (self._duration_offset_in_me(leaf) + leaf.prolated_duration in \
                self._span_points):
                assert isinstance(self.span, int)
                left = self.span
                #right = leaf.duration._flags
                right = durationtools.rational_to_flag_count(leaf.written_duration)
            # just left of span gap
            elif self._duration_offset_in_me(leaf) + leaf.prolated_duration in \
                self._span_points and not self._duration_offset_in_me(leaf) in \
                self._span_points:
                assert isinstance(self.span, int)
                #left = leaf.duration._flags
                left = durationtools.rational_to_flag_count(leaf.written_duration)
                right = self.span
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                result.append(r'\set stemLeftBeamCount = #%s' % left)
            if right is not None:
                result.append(r'\set stemRightBeamCount = #%s' % right)
        return result

    def _fracture_left(self, i):
        self, left, right = ComplexBeamSpanner._fracture_left(self, i)
        weights = [left.prolated_duration, right.prolated_duration]
        assert sum(self.durations) == sum(weights)
        split_durations = sequencetools.split_sequence_by_weights(
            self.durations, weights, cyclic=False, overhang=False)
        left_durations, right_durations = split_durations 
        left._durations = left_durations
        right._durations = right_durations
        return self, left, right

    def _fracture_right(self, i):
        self, left, right = ComplexBeamSpanner._fracture_right(self, i)
        weights = [left.prolated_duration, right.prolated_duration]
        assert sum(self.durations) == sum(weights)
        split_durations = sequencetools.split_sequence_by_weights(
            self.durations, weights, cyclic=False, overhang=False)
        left_durations, right_durations = split_durations 
        left._durations = left_durations
        right._durations = right_durations
        return self, left, right

    def _reverse_components(self):
        ComplexBeamSpanner._reverse_components(self)
        self._durations.reverse()

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def durations():
        def fget(self):
            '''Get spanner leaf group durations::

                >>> staff = Staff("c'16 d'16 e'16 f'16")
                >>> durations = [Duration(1, 8), Duration(1, 8)]
                >>> beam = beamtools.DuratedComplexBeamSpanner(staff[:], durations)
                >>> beam.durations
                [Duration(1, 8), Duration(1, 8)]

            Set spanner leaf group durations::

                >>> staff = Staff("c'16 d'16 e'16 f'16")
                >>> durations = [Duration(1, 8), Duration(1, 8)]
                >>> beam = beamtools.DuratedComplexBeamSpanner(staff[:], durations)
                >>> beam.durations = [Duration(1, 4)]
                >>> beam.durations
                [Duration(1, 4)]

            Set iterable.
            '''
            return self._durations
        def fset(self, arg):
            if arg is None:
                self._durations = None
            elif isinstance(arg, list):
                for i, d in enumerate(arg):
                    if isinstance(d, tuple):
                        arg[i] = durationtools.Duration(*d)
                    else:
                        arg[i] = durationtools.Duration(d)
                self._durations = arg
            else:
                raise ValueError('durations must be list of Durations, or None.')
        return property(**locals())

    @apply
    def span():
        def fget(self):
            r'''Get top-level beam count::

                >>> staff = Staff("c'16 d'16 e'16 f'16")
                >>> durations = [Duration(1, 8), Duration(1, 8)]
                >>> beam = beamtools.DuratedComplexBeamSpanner(staff[:], durations, 1)
                >>> beam.span
                1

            Set top-level beam count::

                >>> staff = Staff("c'16 d'16 e'16 f'16")
                >>> durations = [Duration(1, 8), Duration(1, 8)]
                >>> beam = beamtools.DuratedComplexBeamSpanner(staff[:], durations, 1)
                >>> beam.span = 2
                >>> beam.span
                2

            Set nonnegative integer.
            '''
            return self._span
        def fset(self, arg):
            assert isinstance(arg, (int, type(None)))
            self._span = arg
        return property(**locals())
