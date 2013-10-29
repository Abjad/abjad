# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.ComplexBeamSpanner import ComplexBeamSpanner
from abjad.tools import durationtools


class MeasuredComplexBeamSpanner(ComplexBeamSpanner):
    r'''A measured complex beam spanner.

    ::

        >>> staff = Staff()
        >>> staff.append(Measure((2, 16), "c'16 d'16"))
        >>> staff.append(Measure((2, 16), "e'16 f'16"))
        >>> show(staff) # doctest: +SKIP

    ::

        >>> beam = spannertools.MeasuredComplexBeamSpanner()
        >>> attach(beam, staff.select_leaves())
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
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
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                e'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                f'16 ]
            }
        }

    Beams leaves in spanner explicitly.

    Groups leaves by measures.

    Formats top-level `span` beam between measures.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None, 
        lone=False, 
        span=1, 
        direction=None,
        overrides=None,
        ):
        ComplexBeamSpanner.__init__(
            self, 
            components=components, 
            lone=lone, 
            direction=direction,
            overrides=overrides,
            )
        self.span = span

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        ComplexBeamSpanner._copy_keyword_args(self, new)
        new.span = self.span

    def _format_before_leaf(self, leaf):
        from abjad.tools import scoretools
        from abjad.tools import measuretools
        result = []
        left, right = None, None
        #if leaf.beam.beamable:
        if self.is_beamable_component(leaf):
            if self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            elif leaf._get_parentage(include_self=False).get_first(
                measuretools.Measure) is not None:
                measure = leaf._get_parentage(include_self=False).get_first(
                    measuretools.Measure)
                # leaf at beginning of measure
                if measure._is_one_of_my_first_leaves(leaf):
                    assert isinstance(self.span, int)
                    left = self.span
                    right = leaf.written_duration.flag_count
                # leaf at end of measure
                elif measure._is_one_of_my_last_leaves(leaf):
                    assert isinstance(self.span, int)
                    left = leaf.written_duration.flag_count
                    right = self.span
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                result.append(r'\set stemLeftBeamCount = #%s' % left)
            if right is not None:
                result.append(r'\set stemRightBeamCount = #%s' % right)
        return result

    ### PUBLIC PROPERTIES ###

    @apply
    def span():
        def fget(self):
            r'''Get top-level beam count:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 16), "c'16 d'16"))
                >>> staff.append(Measure((2, 16), "e'16 f'16"))
                >>> beam = spannertools.MeasuredComplexBeamSpanner()
                >>> attach(beam, staff.select_leaves())
                >>> beam.span
                1

            Set top-level beam count:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 16), "c'16 d'16"))
                >>> staff.append(Measure((2, 16), "e'16 f'16"))
                >>> beam = spannertools.MeasuredComplexBeamSpanner()
                >>> attach(beam, staff.select_leaves())
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
