# -*- coding: utf-8 -*-
import collections
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools.spannertools.ComplexBeam import ComplexBeam


class DuratedComplexBeam(ComplexBeam):
    r'''Durated complex beam.

    ::

        >>> import abjad

    ..  container:: example

        Two groups:

        ::

            >>> staff = abjad.Staff("c'16 d'16 e'16 f'16 g'16")
            >>> abjad.setting(staff).auto_beaming = False
            >>> durations = [(2, 16), (3, 16)]
            >>> beam = abjad.DuratedComplexBeam(
            ...     durations=durations,
            ...     span_beam_count=1,
            ...     )
            >>> abjad.attach(beam, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
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
                \set stemRightBeamCount = #2
                f'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                g'16 ]
            }

    ..  container:: example

        Two different groups:

        ::

            >>> staff = abjad.Staff("c'16 d'16 e'16 f'16 g'16")
            >>> abjad.setting(staff).auto_beaming = False
            >>> durations = [(3, 16), (2, 16)]
            >>> beam = abjad.DuratedComplexBeam(
            ...     durations=durations,
            ...     span_beam_count=1,
            ...     )
            >>> abjad.attach(beam, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 [
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #2
                d'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                e'16
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                f'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                g'16 ]
            }

    Groups leaves in spanner according to `durations`.

    Spans leaves between groups according to `span_beam_count`.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_durations',
        '_isolated_nib_direction',
        '_nibs_towards_nonbeamable_components',
        '_span_beam_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_rests=None,
        direction=None,
        durations=None,
        isolated_nib_direction=False,
        nibs_towards_nonbeamable_components=True,
        overrides=None,
        span_beam_count=1,
        ):
        ComplexBeam.__init__(
            self,
            beam_rests=beam_rests,
            direction=direction,
            isolated_nib_direction=isolated_nib_direction,
            overrides=overrides,
            )
        durations = self._coerce_durations(durations)
        self._durations = durations
        assert isinstance(nibs_towards_nonbeamable_components, bool)
        self._nibs_towards_nonbeamable_components = \
            nibs_towards_nonbeamable_components
        assert isinstance(span_beam_count, (int, type(None)))
        self._span_beam_count = span_beam_count

    ### PRIVATE METHODS ###

    def _add_beam_counts(self, leaf, bundle):
        import abjad
        if (not isinstance(leaf, abjad.Leaf) or not self._is_beamable(leaf)):
            left, right = None, None
        elif self._is_exterior_leaf(leaf):
            left, right = self._get_left_right_for_exterior_leaf(leaf)
        elif self._is_just_left_of_gap(leaf):
            left = leaf.written_duration.flag_count
            if self.nibs_towards_nonbeamable_components:
                right = self.span_beam_count
            else:
                next_leaf = abjad.inspect(leaf).get_leaf(1)
                if self._is_beamable(
                    next_leaf,
                    beam_rests=self.beam_rests,
                    ):
                    right = self.span_beam_count
                else:
                    right = 0
        elif self._is_just_right_of_gap(leaf):
            if self.nibs_towards_nonbeamable_components:
                left = self.span_beam_count
            else:
                previous_leaf = abjad.inspect(leaf).get_leaf(-1)
                if self._is_beamable(
                    previous_leaf,
                    beam_rests=self.beam_rests,
                    ):
                    left = self.span_beam_count
                else:
                    left = 0
            right = leaf.written_duration.flag_count
        else:
            assert self._is_interior_leaf(leaf)
            left, right = self._get_left_right_for_interior_leaf(leaf)
        if left is not None:
            string = r'\set stemLeftBeamCount = #{}'.format(left)
            bundle.before.commands.append(string)
        if right is not None:
            string = r'\set stemRightBeamCount = #{}'.format(right)
            bundle.before.commands.append(string)

    @staticmethod
    def _coerce_durations(durations):
        durations = durations or []
        assert isinstance(durations, collections.Iterable)
        durations = [durationtools.Duration(x) for x in durations]
        durations = tuple(durations)
        return durations

    def _copy_keyword_args(self, new):
        ComplexBeam._copy_keyword_args(self, new)
        if self.durations is not None:
            new._durations = self.durations[:]
        new._span_beam_count = self.span_beam_count

    def _fracture_left(self, i):
        import abjad
        self, left, right = ComplexBeam._fracture_left(self, i)
        weights = [
            abjad.inspect(left).get_duration(),
            abjad.inspect(right).get_duration(),
            ]
        assert sum(self.durations) == sum(weights)
        split_durations = datastructuretools.Sequence(self.durations)
        split_durations = split_durations.split(
            weights,
            cyclic=False,
            overhang=False,
            )
        left_durations, right_durations = split_durations
        left._durations = left_durations
        right._durations = right_durations
        return self, left, right

    def _fracture_right(self, i):
        import abjad
        self, left, right = ComplexBeam._fracture_right(self, i)
        weights = [
            abjad.inspect(left).get_duration(),
            abjad.inspect(right).get_duration(),
            ]
        assert sum(self.durations) == sum(weights)
        split_durations = datastructuretools.Sequence(self.durations)
        split_durations = split_durations.split(
            weights,
            cyclic=False,
            overhang=False,
            )
        left_durations, right_durations = split_durations
        left._durations = left_durations
        right._durations = right_durations
        return self, left, right

    def _get_span_beam_offsets(self):
        offsets = []
        if self.durations:
            offset = durationtools.Offset(self.durations[0])
            offsets.append(offset)
            for duration in self.durations[1:]:
                offset = offsets[-1] + duration
                offsets.append(offset)
            offsets.pop()
        return offsets

    def _is_just_left_of_gap(self, leaf):
        local_start_offset = self._start_offset_in_me(leaf)
        local_stop_offset = self._stop_offset_in_me(leaf)
        span_beam_offsets = self._get_span_beam_offsets()
        #print(leaf, local_start_offset, local_stop_offset, span_beam_offsets)
        if local_stop_offset in span_beam_offsets:
            #if local_start_offset not in span_beam_offsets:
            if True:
                return True
        return False

    def _is_just_right_of_gap(self, leaf):
        local_start_offset = self._start_offset_in_me(leaf)
        local_stop_offset = self._stop_offset_in_me(leaf)
        span_beam_offsets = self._get_span_beam_offsets()
        if local_start_offset in span_beam_offsets:
            #if local_stop_offset not in span_beam_offsets:
            if True:
                return True
        return False

    def _reverse_components(self):
        ComplexBeam._reverse_components(self)
        durations = reversed(self.durations)
        durations = tuple(durations)
        self._durations = durations

    ### PUBLIC PROPERTIES ###

    @property
    def beam_rests(self):
        r'''Is true when beam should include rests and skips.
        Otherwise false.

        ..  container:: example

            Does not beam rests:

            ::

                >>> staff = abjad.Staff("c'8 r r d'")
                >>> beam = abjad.DuratedComplexBeam(beam_rests=False)
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [ ]
                    r8
                    r8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    d'8 [ ]
                }

            This is default behavior.

        ..  container:: example

            Beams rests:

            ::

                >>> staff = abjad.Staff("c'8 r r d'")
                >>> beam = abjad.DuratedComplexBeam(beam_rests=True)
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [
                    r8
                    r8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    d'8 ]
                }

        ..  container:: example

            Beams skips:

            ::

                >>> staff = abjad.Staff("c'8 s s d'")
                >>> beam = abjad.DuratedComplexBeam(beam_rests=False)
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [ ]
                    s8
                    s8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    d'8 [ ]
                }

            This is default behavior.

        ..  container:: example

            Beams skips:

            ::

                >>> staff = abjad.Staff("c'8 s s d'")
                >>> beam = abjad.DuratedComplexBeam(beam_rests=True)
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [
                    s8
                    s8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    d'8 ]
                }

        ..  container:: example

            Beams large skip with skip at end:

            ::

                >>> string = "c'8 s4 d'8 s8"
                >>> staff = abjad.Staff(string)
                >>> beam = abjad.DuratedComplexBeam(beam_rests=True)
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [
                    s4
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    d'8
                    s8 ]
                }

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        superclass = super(DuratedComplexBeam, self)
        return superclass.beam_rests

    @property
    def durations(self):
        r'''Gets durations.

        ..  container:: example

            Two groups:

            ::

                >>> staff = abjad.Staff("c'16 d'16 e'16 f'16")
                >>> durations = [(1, 8), (1, 8)]
                >>> beam = abjad.DuratedComplexBeam(durations=durations)
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
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

            ::

                >>> beam.durations
                (Duration(1, 8), Duration(1, 8))

        ..  container:: example

            Three groups:

            ::

                >>> staff = abjad.Staff("c'16 d'16 e'8 f'16 c'16")
                >>> abjad.setting(staff).auto_beaming = False
                >>> durations = [(1, 8), (1, 8), (1, 8)]
                >>> beam = abjad.DuratedComplexBeam(
                ...     durations=durations,
                ...     span_beam_count=1,
                ...     )
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #2
                    c'16 [
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #1
                    d'16
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    e'8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #2
                    f'16
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #0
                    c'16 ]
                }

            Test ensures that leaf groups format correctly when they contain
            only one leaf.

        Defaults to none.

        Set to durations or none.

        Returns tuple of durations or none.
        '''
        return self._durations

    @property
    def nibs_towards_nonbeamable_components(self):
        r'''Is true when when spanner should render nibs pointing towards
        nonbeamable components included in spanner.
        Otherwise false.

        ..  container:: example

            Does not draw nibs towards nonbeamable components:

            ::

                >>> staff = abjad.Staff("c'16 d'16 r4 e'16 f'16")
                >>> durations = [(1, 8), (1, 4), (1, 8)]
                >>> beam = abjad.DuratedComplexBeam(
                ...     durations=durations,
                ...     nibs_towards_nonbeamable_components=False
                ...     )
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #2
                    c'16 [
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #0
                    d'16 ]
                    r4
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #2
                    e'16 [
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #0
                    f'16 ]
                }

        ..  container:: example

            Draws nibs towards nonbeamable components:

            ::

                >>> staff = abjad.Staff("c'16 d'16 r4 e'16 f'16")
                >>> durations = [(1, 8), (1, 4), (1, 8)]
                >>> beam = abjad.DuratedComplexBeam(
                ...     durations=durations,
                ...     nibs_towards_nonbeamable_components=True
                ...     )
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #2
                    c'16 [
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #1
                    d'16 ]
                    r4
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #2
                    e'16 [
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #0
                    f'16 ]
                }

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._nibs_towards_nonbeamable_components

    @property
    def span_beam_count(self):
        r'''Gets span beam count.

        ..  container:: example

            Creates a single span beam between adjacent groups in spanner:

            ::

                >>> staff = abjad.Staff("c'32 d'32 e'32 f'32")
                >>> durations = [(1, 16), (1, 16)]
                >>> beam = abjad.DuratedComplexBeam(
                ...     durations=durations,
                ...     span_beam_count=1,
                ...     )
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #3
                    c'32 [
                    \set stemLeftBeamCount = #3
                    \set stemRightBeamCount = #1
                    d'32
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #3
                    e'32
                    \set stemLeftBeamCount = #3
                    \set stemRightBeamCount = #0
                    f'32 ]
                }

            ::

                >>> beam.span_beam_count
                1

        ..  container:: example

            Creates a double span beam between adjacent groups in spanner:

            ::

                >>> staff = abjad.Staff("c'32 d'32 e'32 f'32")
                >>> durations = [(1, 16), (1, 16)]
                >>> beam = abjad.DuratedComplexBeam(
                ...     durations=durations,
                ...     span_beam_count=2,
                ...     )
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #3
                    c'32 [
                    \set stemLeftBeamCount = #3
                    \set stemRightBeamCount = #2
                    d'32
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #3
                    e'32
                    \set stemLeftBeamCount = #3
                    \set stemRightBeamCount = #0
                    f'32 ]
                }

            ::

                >>> beam.span_beam_count
                2

        ..  container:: example

            Creates no span beam between adjacent groups in spanner:

            ::

                >>> staff = abjad.Staff("c'32 d'32 e'32 f'32")
                >>> durations = [(1, 16), (1, 16)]
                >>> beam = abjad.DuratedComplexBeam(
                ...     durations=durations,
                ...     span_beam_count=0,
                ...     )
                >>> abjad.attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #3
                    c'32 [
                    \set stemLeftBeamCount = #3
                    \set stemRightBeamCount = #0
                    d'32
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #3
                    e'32
                    \set stemLeftBeamCount = #3
                    \set stemRightBeamCount = #0
                    f'32 ]
                }

            ::

                >>> beam.span_beam_count
                0

        Defaults to ``1``.

        Set to nonnegative integer.

        Returns nonnegative integer.
        '''
        return self._span_beam_count
