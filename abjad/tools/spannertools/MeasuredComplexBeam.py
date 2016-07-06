# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools.spannertools.ComplexBeam import ComplexBeam


class MeasuredComplexBeam(ComplexBeam):
    r'''Measured complex beam.

    ..  container:: example

        ::

            >>> staff = Staff()
            >>> staff.append(Measure((2, 16), "c'16 d'16"))
            >>> staff.append(Measure((2, 16), "e'16 f'16"))
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ::

            >>> beam = spannertools.MeasuredComplexBeam()
            >>> selector = select().by_leaf(flatten=True)
            >>> leaves = selector(staff)
            >>> attach(beam, leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff \with {
                autoBeaming = ##f
            } {
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

    Formats top-level `span_beam_count` beam between measures.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_span_beam_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        isolated_nib_direction=False,
        overrides=None,
        span_beam_count=1,
        ):
        ComplexBeam.__init__(
            self,
            direction=direction,
            isolated_nib_direction=isolated_nib_direction,
            overrides=overrides,
            )
        assert isinstance(span_beam_count, (int, type(None)))
        self._span_beam_count = span_beam_count

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        ComplexBeam._copy_keyword_args(self, new)
        new._span_beam_count = self.span_beam_count

    def _format_before_leaf(self, leaf):
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
                    assert isinstance(self.span_beam_count, int)
                    left = self.span_beam_count
                    right = leaf.written_duration.flag_count
                # leaf at end of measure
                elif measure._is_one_of_my_last_leaves(leaf):
                    assert isinstance(self.span_beam_count, int)
                    left = leaf.written_duration.flag_count
                    right = self.span_beam_count
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
    def span_beam_count(self):
        r'''Gets number of span beams between adjacent measures.

        ..  container:: example

            Use one span beam between measures:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 32), "c'32 d'32"))
                >>> staff.append(Measure((2, 32), "e'32 f'32"))
                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> beam = spannertools.MeasuredComplexBeam(span_beam_count=1)
                >>> attach(beam, leaves)
                >>> show(staff) # doctest: +SKIP

            ::

                >>> beam.span_beam_count
                1

        ..  container:: example

            Use two span beams between measures:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 32), "c'32 d'32"))
                >>> staff.append(Measure((2, 32), "e'32 f'32"))
                >>> beam = spannertools.MeasuredComplexBeam(span_beam_count=2)
                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> attach(beam, leaves)
                >>> show(staff) # doctest: +SKIP

            ::

                >>> beam.span_beam_count
                2

        Returns nonnegative integer or none.
        '''
        return self._span_beam_count