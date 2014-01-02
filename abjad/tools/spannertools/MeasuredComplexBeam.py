# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.ComplexBeam import ComplexBeam
from abjad.tools import durationtools


class MeasuredComplexBeam(ComplexBeam):
    r'''A measured complex beam spanner.

    ..  container:: example

        ::

            >>> staff = Staff()
            >>> staff.append(Measure((2, 16), "c'16 d'16"))
            >>> staff.append(Measure((2, 16), "e'16 f'16"))
            >>> show(staff) # doctest: +SKIP

        ::

            >>> beam = spannertools.MeasuredComplexBeam()
            >>> attach(beam, staff.select_leaves())
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
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

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_lone',
        '_span',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        lone_nib_direction=False, 
        span=1, 
        direction=None,
        overrides=None,
        ):
        ComplexBeam.__init__(
            self, 
            direction=direction,
            lone_nib_direction=lone_nib_direction, 
            overrides=overrides,
            )
        assert isinstance(span, (int, type(None)))
        self._span = span

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        ComplexBeam._copy_keyword_args(self, new)
        new.span = self.span

    def _format_before_leaf(self, leaf):
        from abjad.tools import scoretools
        from abjad.tools import scoretools
        result = []
        left, right = None, None
        #if leaf.beam.beamable:
        if self._is_beamable_component(leaf):
            if self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            elif leaf._get_parentage(include_self=False).get_first(
                scoretools.Measure) is not None:
                measure = leaf._get_parentage(include_self=False).get_first(
                    scoretools.Measure)
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
                string = r'\set stemLeftBeamCount = #{}'.format(left)
                result.append(string)
            if right is not None:
                string = r'\set stemRightBeamCount = #{}'.format(right)
                result.append(string)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def span(self):
        r'''Gets top-level span-beam count.

        ::

            >>> staff = Staff()
            >>> staff.append(Measure((2, 16), "c'16 d'16"))
            >>> staff.append(Measure((2, 16), "e'16 f'16"))
            >>> beam = spannertools.MeasuredComplexBeam()
            >>> attach(beam, staff.select_leaves())
            >>> beam.span
            1

        Returns nonnegative integer or none.
        '''
        return self._span
