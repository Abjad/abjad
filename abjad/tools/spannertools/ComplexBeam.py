# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.spannertools.Beam import Beam


class ComplexBeam(Beam):
    r'''Complex beam.

    ..  container:: example

        ::

            >>> staff = Staff("c'16 e'16 r16 f'16 g'2")
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff \with {
                autoBeaming = ##f
            } {
                c'16
                e'16
                r16
                f'16
                g'2
            }

        ::

            >>> beam = spannertools.ComplexBeam()
            >>> attach(beam, staff[:4])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff \with {
                autoBeaming = ##f
            } {
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 [
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #2
                e'16 ]
                r16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                f'16 [ ]
                g'2
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_rests',
        '_isolated_nib_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_rests=None,
        direction=None,
        isolated_nib_direction=None,
        overrides=None,
        ):
        Beam.__init__(
            self,
            direction=direction,
            overrides=overrides,
            )
        if beam_rests is not None:
            beam_rests = bool(beam_rests)
        self._beam_rests = beam_rests
        assert isolated_nib_direction in (Left, Right, True, False, None)
        self._isolated_nib_direction = isolated_nib_direction

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        Beam._copy_keyword_args(self, new)
        self._beam_rests = self.beam_rests
        new._isolated_nib_direction = self.isolated_nib_direction

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_beamable_component(leaf, beam_rests=self.beam_rests):
            if self._is_my_only_leaf(leaf):
                left, right = self._get_left_right_for_lone_leaf(leaf)
            elif self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                string = r'\set stemLeftBeamCount = #{}'.format(left)
                result.append(string)
            if right is not None:
                string = r'\set stemRightBeamCount = #{}'.format(right)
                result.append(string)
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_beamable_component(leaf, beam_rests=self.beam_rests):
            previous_leaf = leaf._get_leaf(-1)
            next_leaf = leaf._get_leaf(1)
            # isolated_nib_direction
            if self._is_my_only_leaf(leaf):
                if self.isolated_nib_direction:
                    if self.direction is not None:
                        string = '{} ['.format(self.direction)
                        result.append(string)
                    else:
                        result.append('[')
            # otherwise
            elif self._is_my_first_leaf(leaf) or not previous_leaf or \
                not self._is_beamable_component(
                    previous_leaf,
                    beam_rests=self.beam_rests,
                    ):
                if self.direction is not None:
                    string = '{} ['.format(self.direction)
                    result.append(string)
                else:
                    result.append('[')
            # isolated_nib_direction
            if self._is_my_only_leaf(leaf):
                if self.isolated_nib_direction:
                    result.append(']')
            # otherwise
            elif self._is_my_last_leaf(leaf) or not next_leaf or \
                not self._is_beamable_component(
                next_leaf, beam_rests=self.beam_rests):
                result.append(']')
        return result

    def _get_left_right_for_exterior_leaf(self, leaf):
        r'''Gets left and right flag counts for exterior leaf in spanner.
        '''
        # isolated_nib_direction
        if self._is_my_only_leaf(leaf):
            left, right = self._get_left_right_for_lone_leaf(leaf)
        # first
        elif self._is_my_first_leaf(leaf) or not leaf._get_leaf(-1):
            left = 0
            right = leaf.written_duration.flag_count
        # last
        elif self._is_my_last_leaf(leaf) or leaf._get_leaf(1):
            left = leaf.written_duration.flag_count
            right = 0
        else:
            message = 'leaf must be first or last in spanner.'
            raise ValueError(message)
        return left, right

    def _get_left_right_for_interior_leaf(self, leaf):
        r'''Interior leaves are neither first nor last in spanner.
        Interior leaves may be surrounded by beamable leaves.
        Interior leaves may be surrounded by unbeamable leaves.
        Four cases total for beamability of surrounding leaves.
        '''
        previous_leaf = leaf._get_leaf(-1)
        previous_written = previous_leaf.written_duration
        current_written = leaf.written_duration
        next_leaf = leaf._get_leaf(1)
        next_written = next_leaf.written_duration
        previous_flag_count = previous_written.flag_count
        current_flag_count = current_written.flag_count
        next_flag_count = next_written.flag_count
        # [unbeamable leaf beamable]
        if not self._is_beamable_component(
            previous_leaf, beam_rests=self.beam_rests) and \
            self._is_beamable_component(
            next_leaf, beam_rests=self.beam_rests):
            left = current_flag_count
            right = min(current_flag_count, next_flag_count)
        # [beamable leaf unbeamable]
        if self._is_beamable_component(
            previous_leaf, beam_rests=self.beam_rests) and \
            not self._is_beamable_component(
            next_leaf, beam_rests=self.beam_rests):
            left = min(current_flag_count, previous_flag_count)
            right = current_flag_count
        # [unbeamable leaf unbeamable]
        elif not self._is_beamable_component(
            previous_leaf, beam_rests=self.beam_rests) and \
            not self._is_beamable_component(
            next_leaf, beam_rests=self.beam_rests):
            left = current_flag_count
            right = current_flag_count
        # [beamable leaf beamable]
        else:
            left = min(current_flag_count, previous_flag_count)
            right = min(current_flag_count, next_flag_count)
            if left != current_flag_count and right != current_flag_count:
                left = current_flag_count
        return left, right

    def _get_left_right_for_lone_leaf(self, leaf):
        r'''Gets left and right flag counts for only leaf in spanner.
        '''
        current_flag_count = leaf.written_duration.flag_count
        left, right = None, None
        if self.isolated_nib_direction == Left:
            left = current_flag_count
            right = 0
        elif self.isolated_nib_direction == Right:
            left = 0
            right = current_flag_count
        elif self.isolated_nib_direction is True:
            left = current_flag_count
            right = current_flag_count
        elif self.isolated_nib_direction is False:
            left = None
            right = None
        else:
            message = 'long must be left, right, true or false: {!r}.'
            message = message.format(self.isolated_nib_direction)
            raise ValueError(message)
        return left, right

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        lilypond_format_bundle.get('before').spanners.extend(
            self._format_before_leaf(leaf))
        lilypond_format_bundle.get('right').spanners.extend(
            self._format_right_of_leaf(leaf))
        lilypond_format_bundle.get('after').spanners.extend(
            self._format_after_leaf(leaf))
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def beam_rests(self):
        r'''Is true when beam should include rests and skips.
        Otherwise false.

        ..  container:: example

            **Example 1.** Does not beam rests:

            ::

                >>> staff = Staff("c'8 r r d'")
                >>> beam = spannertools.ComplexBeam(beam_rests=False)
                >>> attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 2.** Does beam rests:

            ::

                >>> staff = Staff("c'8 r r d'")
                >>> beam = spannertools.ComplexBeam(beam_rests=True)
                >>> attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    r8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    r8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    d'8 ]
                }

        ..  container:: example

            **Example 3.** Does not beam skips:

            ::

                >>> staff = Staff("c'8 s s d'")
                >>> beam = spannertools.ComplexBeam(beam_rests=False)
                >>> attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 4.** Does beam skips:

            ::

                >>> staff = Staff("c'8 s s d'")
                >>> beam = spannertools.ComplexBeam(beam_rests=True)
                >>> attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    s8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    s8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    d'8 ]
                }

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._beam_rests

    @property
    def isolated_nib_direction(self):
        r'''Gets directed treatment to apply to lone nibs.

        ..  container:: example

            Beams lone leaf and forces nib to the left:

            ::

                >>> measure = Measure((1, 16), "c'16")
                >>> beam = spannertools.ComplexBeam(isolated_nib_direction=Left)
                >>> attach(beam, measure[:])
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 1/16
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #0
                    c'16 [ ]
                }

        ..  container:: example

            Beams lone leaf and forces nib to the right:

            ::

                >>> measure = Measure((1, 16), "c'16")
                >>> beam = spannertools.ComplexBeam(isolated_nib_direction=Right)
                >>> attach(beam, measure[:])
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 1/16
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #2
                    c'16 [ ]
                }

        ..  container:: example

            Beams lone leaf and forces nibs both left and right:

            ::

                >>> measure = Measure((1, 16), "c'16")
                >>> beam = spannertools.ComplexBeam(isolated_nib_direction=True)
                >>> attach(beam, measure[:])
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 1/16
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #2
                    c'16 [ ]
                }

        ..  container:: example

            Does not beam isolated_nib_direction leaf:

            ::

                >>> measure = Measure((1, 16), "c'16")
                >>> beam = spannertools.ComplexBeam(isolated_nib_direction=False)
                >>> attach(beam, measure[:])
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 1/16
                    c'16
                }

        Set to left, right, true or false.

        Ignores this setting when spanner contains more than one leaf.
        '''
        return self._isolated_nib_direction