#[ -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.spannertools.ComplexBeam import ComplexBeam


class DuratedComplexBeam(ComplexBeam):
    r'''A durated complex beam spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'16 d'16 e'16 f'16")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> durations = [Duration(1, 8), Duration(1, 8)]
            >>> beam = spannertools.DuratedComplexBeam(
            ...     durations=durations, 
            ...     span=1,
            ...     )
            >>> attach(beam, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
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

    Beams all beamable leaves in spanner explicitly.

    Groups leaves in spanner according to `durations`.

    Spans leaves between duration groups according to `span`.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_durations',
        '_lone',
        '_span',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        direction=None,
        durations=None, 
        lone_nib_direction=False, 
        overrides=None,
        span=1, 
        ):
        ComplexBeam.__init__(
            self, 
            direction=direction,
            lone_nib_direction=lone_nib_direction,
            overrides=overrides,
            )
        if durations is None:
            self._durations = None
        elif isinstance(durations, list):
            for i, d in enumerate(durations):
                if isinstance(d, tuple):
                    durations[i] = durationtools.Duration(*d)
                else:
                    durations[i] = durationtools.Duration(d)
            durations = tuple(durations)
            self._durations = durations
        else:
            message = 'durations must be list of durations or none.'
            raise ValueError(message)
        self._durations = durations
        assert isinstance(span, (int, type(None)))
        self._span = span

    ### PRIVATE PROPERTIES ###

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
        ComplexBeam._copy_keyword_args(self, new)
        new._durations = self.durations[:]
        new._span = self.span

    def _format_before_leaf(self, leaf):
        result = []
        #if leaf.beam.beamable:
        if self._is_beamable_component(leaf):
            if self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            # just right of span gap
            elif self._duration_offset_in_me(leaf) in self._span_points and \
                not (self._duration_offset_in_me(leaf) + leaf._get_duration() in \
                self._span_points):
                assert isinstance(self.span, int)
                left = self.span
                #right = leaf._get_duration()._flags
                right = leaf.written_duration.flag_count
            # just left of span gap
            elif self._duration_offset_in_me(leaf) + leaf._get_duration() in \
                self._span_points and \
                not self._duration_offset_in_me(leaf) in self._span_points:
                assert isinstance(self.span, int)
                #left = leaf._get_duration()._flags
                left = leaf.written_duration.flag_count
                right = self.span
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                result.append(r'\set stemLeftBeamCount = #%s' % left)
            if right is not None:
                result.append(r'\set stemRightBeamCount = #%s' % right)
        return result

    def _fracture_left(self, i):
        self, left, right = ComplexBeam._fracture_left(self, i)
        weights = [left._get_duration(), right._get_duration()]
        assert sum(self.durations) == sum(weights)
        split_durations = sequencetools.split_sequence_by_weights(
            self.durations, 
            weights, 
            cyclic=False, 
            overhang=False,
            )
        left_durations, right_durations = split_durations
        left._durations = left_durations
        right._durations = right_durations
        return self, left, right

    def _fracture_right(self, i):
        self, left, right = ComplexBeam._fracture_right(self, i)
        weights = [left._get_duration(), right._get_duration()]
        assert sum(self.durations) == sum(weights)
        split_durations = sequencetools.split_sequence_by_weights(
            self.durations, 
            weights, 
            cyclic=False, 
            overhang=False,
            )
        left_durations, right_durations = split_durations
        left._durations = left_durations
        right._durations = right_durations
        return self, left, right

    def _reverse_components(self):
        ComplexBeam._reverse_components(self)
        durations = reversed(self.durations)
        durations = tuple(durations)
        self._durations = durations

    ### PUBLIC PROPERTIES ###

    @property
    def durations(self):
        r'''Gets spanner leaf group durations.

        ::

            >>> staff = Staff("c'16 d'16 e'16 f'16")
            >>> durations = [Duration(1, 8), Duration(1, 8)]
            >>> beam = spannertools.DuratedComplexBeam(
            ...     durations=durations,
            ...     )
            >>> attach(beam, staff[:])
            >>> beam.durations
            (Duration(1, 8), Duration(1, 8))

        Returns tuple of durations or none.
        '''
        return self._durations

    @property
    def span(self):
        r'''Gets top-level span-beam count.

        ::

            >>> staff = Staff("c'16 d'16 e'16 f'16")
            >>> durations = [Duration(1, 8), Duration(1, 8)]
            >>> beam = spannertools.DuratedComplexBeam(
            ...     durations=durations, 
            ...     span=1,
            ...     )
            >>> attach(beam, staff[:])
            >>> beam.span
            1

        Set nonnegative integer.
        '''
        return self._span
