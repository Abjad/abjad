import typing
from abjad.enumerations import (
    HorizontalAlignment, Left, Right, VerticalAlignment,
)
from .Beam import Beam
Number = typing.Union[int, float]


class ComplexBeam(Beam):
    r"""
    Complex beam.

    ..  container:: example

        >>> staff = abjad.Staff("c'16 e'16 r16 f'16 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'16
                e'16
                r16
                f'16
                g'2
            }

        >>> beam = abjad.ComplexBeam()
        >>> abjad.attach(beam, staff[:4])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \set stemLeftBeamCount = 0
                \set stemRightBeamCount = 2
                c'16
                [
                \set stemLeftBeamCount = 2
                \set stemRightBeamCount = 2
                e'16
                ]
                r16
                \set stemLeftBeamCount = 2
                \set stemRightBeamCount = 0
                f'16
                [
                ]
                g'2
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_rests',
        '_isolated_nib_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_rests: bool = None,
        direction: typing.Union[str, VerticalAlignment] = None,
        isolated_nib_direction: typing.Union[bool, HorizontalAlignment] = None,
        leak: bool = None,
        stemlet_length: Number = None,
        ) -> None:
        Beam.__init__(
            self,
            direction=direction,
            leak=leak,
            stemlet_length=stemlet_length,
            )
        if beam_rests is not None:
            beam_rests = bool(beam_rests)
        self._beam_rests = beam_rests
        prototype = (Left, Right, True, False, None)
        assert isolated_nib_direction in prototype
        self._isolated_nib_direction = isolated_nib_direction

    ### PRIVATE METHODS ###

    def _add_beam_counts(self, leaf, bundle):
        if self._is_beamable(leaf, beam_rests=self.beam_rests):
            if self._is_my_only(leaf):
                left, right = self._get_left_right_for_lone_leaf(leaf)
            elif self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                string = r'\set stemLeftBeamCount = {}'.format(left)
                bundle.before.commands.append(string)
            if right is not None:
                string = r'\set stemRightBeamCount = {}'.format(right)
                bundle.before.commands.append(string)

    def _add_start_and_stops(self, leaf, bundle):
        if self._is_beamable(leaf, beam_rests=self.beam_rests):
            previous_leaf = leaf._get_leaf(-1)
            next_leaf = leaf._get_leaf(1)
            # isolated_nib_direction
            if self._is_my_only(leaf):
                if self.isolated_nib_direction:
                    strings = self.start_command()
                    bundle.right.spanner_starts.extend(strings)
            # otherwise
            elif (leaf is self[0] or
                not previous_leaf or
                not self._is_beamable(
                    previous_leaf,
                    beam_rests=self.beam_rests,
                    )
                ):
                strings = self.start_command()
                bundle.right.spanner_starts.extend(strings)
            # isolated_nib_direction
            if self._is_my_only(leaf):
                if self.isolated_nib_direction:
                    string = self.stop_command()
                    for spanner_start in bundle.right.spanner_starts:
                        if '[' in spanner_start:
                            bundle.right.spanner_starts.append(string)
                            break
                    else:
                        bundle.right.spanner_stops.append(string)
            # otherwise
            elif (leaf is self[-1] or
                not next_leaf or
                not self._is_beamable(next_leaf, beam_rests=self.beam_rests)):
                string = self.stop_command()
                for spanner_start in bundle.right.spanner_starts:
                    if '[' in spanner_start:
                        bundle.right.spanner_starts.append(string)
                        break
                else:
                    bundle.right.spanner_stops.append(string)

    def _copy_keywords(self, new):
        Beam._copy_keywords(self, new)
        self._beam_rests = self.beam_rests
        new._isolated_nib_direction = self.isolated_nib_direction

    def _get_left_right_for_exterior_leaf(self, leaf):
        """
        Gets left and right flag counts for exterior leaf in spanner.
        """
        # isolated_nib_direction
        if self._is_my_only(leaf):
            left, right = self._get_left_right_for_lone_leaf(leaf)
        # first
        elif leaf is self[0] or not leaf._get_leaf(-1):
            left = 0
            right = leaf.written_duration.flag_count
        # last
        elif leaf is self[-1] or leaf._get_leaf(1):
            left = leaf.written_duration.flag_count
            right = 0
        else:
            message = 'leaf must be first or last in spanner.'
            raise ValueError(message)
        return left, right

    def _get_left_right_for_interior_leaf(self, leaf):
        """
        Interior leaves are neither first nor last in spanner.
        Interior leaves may be surrounded by beamable leaves.
        Interior leaves may be surrounded by unbeamable leaves.
        Four cases total for beamability of surrounding leaves.
        """
        import abjad
        previous_leaf = leaf._get_leaf(-1)
        previous_written = previous_leaf.written_duration
        current_written = leaf.written_duration
        next_leaf = leaf._get_leaf(1)
        next_written = next_leaf.written_duration
        previous_flag_count = previous_written.flag_count
        current_flag_count = current_written.flag_count
        next_flag_count = next_written.flag_count
        rest_prototype = (
            abjad.MultimeasureRest,
            abjad.Rest,
            abjad.Skip,
            )
        #print(previous_leaf, leaf, next_leaf)
        # [unbeamable leaf beamable]
        if (not self._is_beamable(
                previous_leaf,
                beam_rests=self.beam_rests,
                ) and
            self._is_beamable(
                next_leaf,
                beam_rests=self.beam_rests,
                )
            ):
            left = current_flag_count
            right = min(current_flag_count, next_flag_count)
        # TODO: should be following be elif instead of if?
        # [beamable leaf unbeamable]
        if (self._is_beamable(
                previous_leaf,
                beam_rests=self.beam_rests,
                ) and
            not self._is_beamable(
                next_leaf,
                beam_rests=self.beam_rests,
                )
            ):
            left = min(current_flag_count, previous_flag_count)
            right = current_flag_count
        # [unbeamable leaf unbeamable]
        elif (not self._is_beamable(
                previous_leaf,
                beam_rests=self.beam_rests,
                ) and
            not self._is_beamable(
                next_leaf,
                beam_rests=self.beam_rests,
                )
            ):
            left = current_flag_count
            right = current_flag_count
        # [beamable leaf beamable]
        else:
            if isinstance(previous_leaf, rest_prototype):
                left = current_flag_count
            else:
                left = min(current_flag_count, previous_flag_count)
            if isinstance(next_leaf, rest_prototype):
                right = current_flag_count
            else:
                right = min(current_flag_count, next_flag_count)
            if left != current_flag_count and right != current_flag_count:
                left = current_flag_count
        return left, right

    def _get_left_right_for_lone_leaf(self, leaf):
        """
        Gets left and right flag counts for only leaf in spanner.
        """
        current_flag_count = leaf.written_duration.flag_count
        left, right = None, None
        if self.isolated_nib_direction is Left:
            left = current_flag_count
            right = 0
        elif self.isolated_nib_direction is Right:
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
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        self._add_stemlet_length(leaf, bundle)
        self._add_beam_counts(leaf, bundle)
        self._add_start_and_stops(leaf, bundle)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def beam_rests(self) -> typing.Optional[bool]:
        r"""
        Is true when beam should include rests and skips.

        ..  container:: example

            Does not beam rests:

            >>> staff = abjad.Staff("c'8 r r d'")
            >>> beam = abjad.ComplexBeam(beam_rests=False)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 1
                    c'8
                    [
                    ]
                    r8
                    r8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 0
                    d'8
                    [
                    ]
                }

            This is default behavior.

        ..  container:: example

            Does beam rests:

            >>> staff = abjad.Staff("c'8 r r d'")
            >>> beam = abjad.ComplexBeam(beam_rests=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 1
                    c'8
                    [
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    r8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    r8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 0
                    d'8
                    ]
                }

        ..  container:: example

            Does not beam skips:

            >>> staff = abjad.Staff("c'8 s s d'")
            >>> beam = abjad.ComplexBeam(beam_rests=False)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 1
                    c'8
                    [
                    ]
                    s8
                    s8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 0
                    d'8
                    [
                    ]
                }

            This is default behavior.

        ..  container:: example

            Does beam skips:

            >>> staff = abjad.Staff("c'8 s s d'")
            >>> beam = abjad.ComplexBeam(beam_rests=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 1
                    c'8
                    [
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    s8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    s8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 0
                    d'8
                    ]
                }

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._beam_rests

    @property
    def isolated_nib_direction(self) -> typing.Union[
        bool, HorizontalAlignment, None]:
        r"""
        Gets directed treatment to apply to lone nibs.

        ..  container:: example

            Beams lone leaf and forces nib to the left:

            >>> measure = abjad.Measure((1, 16), "c'16")
            >>> beam = abjad.ComplexBeam(isolated_nib_direction=abjad.Left)
            >>> abjad.attach(beam, measure[:])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                {   % measure
                    \time 1/16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 0
                    c'16
                    [
                    ]
                }   % measure

        ..  container:: example

            Beams lone leaf and forces nib to the right:

            >>> measure = abjad.Measure((1, 16), "c'16")
            >>> beam = abjad.ComplexBeam(isolated_nib_direction=abjad.Right)
            >>> abjad.attach(beam, measure[:])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                {   % measure
                    \time 1/16
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 2
                    c'16
                    [
                    ]
                }   % measure

        ..  container:: example

            Beams lone leaf and forces nibs both left and right:

            >>> measure = abjad.Measure((1, 16), "c'16")
            >>> beam = abjad.ComplexBeam(isolated_nib_direction=True)
            >>> abjad.attach(beam, measure[:])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                {   % measure
                    \time 1/16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 2
                    c'16
                    [
                    ]
                }   % measure

        ..  container:: example

            Does not beam isolated_nib_direction leaf:

            >>> measure = abjad.Measure((1, 16), "c'16")
            >>> beam = abjad.ComplexBeam(isolated_nib_direction=False)
            >>> abjad.attach(beam, measure[:])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                {   % measure
                    \time 1/16
                    c'16
                }   % measure

        Set to left, right, true or false.

        Ignores this setting when spanner contains more than one leaf.
        """
        return self._isolated_nib_direction

    @property
    def leak(self):
        r"""
        Is true when beam leaks one leaf to the right with LilyPond empty chord
        ``<>`` construct.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'16 e'16 r16 f'16 g'2")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.ComplexBeam(beam_rests=True)
            >>> abjad.attach(beam, staff[:3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 2
                    c'16
                    [
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 2
                    e'16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 0
                    r16
                    ]
                    f'16
                    g'2
                }

            With leak:

            >>> staff = abjad.Staff("c'16 e'16 r16 f'16 g'2")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.ComplexBeam(beam_rests=True, leak=True)
            >>> abjad.attach(beam, staff[:3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 2
                    c'16
                    [
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 2
                    e'16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 0
                    r16
                    <> ]
                    f'16
                    g'2
                }

        """
        return super(ComplexBeam, self).leak

    @property
    def stemlet_length(self) -> typing.Optional[Number]:
        r"""
        Gets stemlet length.

        ..  container:: example

            >>> staff = abjad.Staff(
            ...     "r8 c' r c' g'2",
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.ComplexBeam(beam_rests=True, stemlet_length=2)
            >>> abjad.attach(beam, staff[:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new RhythmicStaff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \override RhythmicStaff.Stem.stemlet-length = 2
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 1
                    r8
                    [
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    c'8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    r8
                    \revert RhythmicStaff.Stem.stemlet-length
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 0
                    c'8
                    ]
                    g'2
                }

        """
        return self._stemlet_length

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.List[str]:
        """
        Gets start command.

        ..  container:: example

            >>> abjad.ComplexBeam().start_command()
            ['[']

            With direction:

            >>> abjad.ComplexBeam(direction=abjad.Up).start_command()
            ['^ [']

        """
        return super(ComplexBeam, self).start_command()

    def stop_command(self) -> typing.Optional[str]:
        """
        Gets stop command.

        ..  container:: example

            >>> abjad.ComplexBeam().stop_command()
            ']'

            With leak:

            >>> abjad.ComplexBeam(leak=True).stop_command()
            '<> ]'

        """
        return super(ComplexBeam, self).stop_command()
