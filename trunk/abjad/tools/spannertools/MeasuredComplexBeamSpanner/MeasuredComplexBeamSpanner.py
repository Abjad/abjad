from abjad.tools.spannertools.ComplexBeamSpanner import ComplexBeamSpanner
from abjad.tools import durationtools


class MeasuredComplexBeamSpanner(ComplexBeamSpanner):
    r'''Abjad measured complex beam spanner::

        abjad> staff = Staff([Measure((2, 16), "c'16 d'16"), Measure((2, 16), "e'16 f'16")])

    ::

        abjad> spannertools.MeasuredComplexBeamSpanner(staff.leaves)
        MeasuredComplexBeamSpanner(c'16, d'16, e'16, f'16)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/16
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 [
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                d'16
            }
            {
                \time 2/16
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                e'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                f'16 ]
            }
        }

    Beam leaves in spanner explicitly.

    Group leaves by measures.

    Format top-level `span` beam between measures.

    Return measured complex beam spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None, lone=False, span=1, direction=None):
        ComplexBeamSpanner.__init__(self, components=components, lone=lone, direction=direction)
        self.span = span

    ### PRIVATE METHODS ###

    def _format_before_leaf(self, leaf):
        from abjad.tools.measuretools.Measure import Measure
        from abjad.tools import componenttools
        result = []
        #if leaf.beam.beamable:
        if componenttools.is_beamable_component(leaf):
            if self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            elif componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
                leaf, Measure) is not None:
                measure = componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
                    leaf, Measure)
                # leaf at beginning of measure
                if measure._is_one_of_my_first_leaves(leaf):
                    assert isinstance(self.span, int)
                    left = self.span
                    #right = leaf.duration._flags
                    right = durationtools.rational_to_flag_count(leaf.written_duration)
                # leaf at end of measure
                elif measure._is_one_of_my_last_leaves(leaf):
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

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def span():
        def fget(self):
            '''Get top-level beam count::

                abjad> staff = Staff([Measure((2, 16), "c'16 d'16"), Measure((2, 16), "e'16 f'16")])
                abjad> beam = spannertools.MeasuredComplexBeamSpanner(staff.leaves)
                abjad> beam.span
                1

            Set top-level beam count::

                abjad> staff = Staff([Measure((2, 16), "c'16 d'16"), Measure((2, 16), "e'16 f'16")])
                abjad> beam = spannertools.MeasuredComplexBeamSpanner(staff.leaves)
                abjad> beam.span = 2
                abjad> beam.span
                2

            Set nonnegative integer.
            '''
            return self._span
        def fset(self, arg):
            assert isinstance(arg, (int, type(None)))
            self._span = arg
        return property(**locals())
