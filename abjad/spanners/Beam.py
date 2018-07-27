import collections
import typing
from abjad import enums
from abjad import typings
from abjad.core.Chord import Chord
from abjad.core.Leaf import Leaf
from abjad.core.MultimeasureRest import MultimeasureRest
from abjad.core.Note import Note
from abjad.core.Rest import Rest
from abjad.core.Skip import Skip
from abjad.core.Staff import Staff
from abjad.top.inspect import inspect
from abjad.top.new import new
from abjad.top.sequence import sequence
from abjad.utilities.Duration import Duration
from abjad.utilities.Offset import Offset
from abjad.utilities.String import String
from .Spanner import Spanner


# TODO: teach durated beam to respect beam_lone_notes
class Beam(Spanner):
    r"""
    Beam.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
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
                c'8
                d'8
                e'8
                f'8
                g'2
            }

        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[:2])
        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                [
                d'8
                ]
                e'8
                [
                f'8
                ]
                g'2
            }

    ..  container:: example

        Tweaks beam positions:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> beam = abjad.Beam()
        >>> abjad.tweak(beam).positions = (3, 3)
        >>> abjad.attach(beam, staff[:2])
        >>> beam = abjad.Beam()
        >>> abjad.tweak(beam).positions = (3, 3)
        >>> abjad.attach(beam, staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                - \tweak positions #'(3 . 3)
                [
                d'8
                ]
                e'8
                - \tweak positions #'(3 . 3)
                [
                f'8
                ]
                g'2
            }

    ..  container:: example

        Spanners can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
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
                c'8
                d'8
                e'8
                f'8
                g'2
            }

        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[:2], tag='BEAM')
        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        \with
        {
            autoBeaming = ##f
        }
        {
            c'8
            [ %! BEAM
            d'8
            ] %! BEAM
            e'8
            [
            f'8
            ]
            g'2
        }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_lone_notes',
        '_beam_rests',
        '_direction',
        '_durations',
        '_span_beam_count',
        '_stemlet_length',
        )

    _start_command = '['

    _stop_command = ']'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        beam_lone_notes: bool = None,
        beam_rests: bool = None,
        direction: typing.Union[str, enums.VerticalAlignment] = None,
        durations: typing.Iterable[Duration] = None,
        span_beam_count: int = 1,
        stemlet_length: typings.Number = None,
        ) -> None:
        Spanner.__init__(self)
        direction = String.to_tridirectional_lilypond_symbol(direction)
        if beam_lone_notes is not None:
            beam_lone_notes = bool(beam_lone_notes)
        self._beam_lone_notes = beam_lone_notes
        if beam_rests is not None:
            beam_rests = bool(beam_rests)
        self._beam_rests = beam_rests
        self._direction = direction
        durations = self._coerce_durations(durations)
        self._durations: typing.Tuple[Duration, ...] = durations
        if span_beam_count is not None:
            assert isinstance(span_beam_count, int)
        self._span_beam_count = span_beam_count
        self._stemlet_length = stemlet_length

    ### PRIVATE METHODS ###

    def _add_beam_counts(self, leaf, bundle):
        if (not isinstance(leaf, Leaf) or not self._is_beamable(leaf)):
            left, right = None, None
        elif self._is_exterior_leaf(leaf):
            left, right = self._get_left_right_for_exterior_leaf(leaf)
        elif self._is_just_left_of_gap(leaf):
            left = leaf.written_duration.flag_count
            next_leaf = inspect(leaf).leaf(1)
            if self._is_beamable(
                next_leaf,
                beam_rests=self.beam_rests,
                ):
                right = self.span_beam_count
            else:
                right = 0
        elif self._is_just_right_of_gap(leaf):
            previous_leaf = inspect(leaf).leaf(-1)
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
            string = rf'\set stemLeftBeamCount = {left}'
            bundle.before.commands.append(string)
        if right is not None:
            string = rf'\set stemRightBeamCount = {right}'
            bundle.before.commands.append(string)

    def _add_start_and_stops(self, leaf, bundle):
        if self._is_beamable(leaf, beam_rests=self.beam_rests):
            previous_leaf = leaf._get_leaf(-1)
            next_leaf = leaf._get_leaf(1)
            if (leaf is self[0] or
                not previous_leaf or
                not self._is_beamable(
                    previous_leaf,
                    beam_rests=self.beam_rests,
                    )
                ):
                strings = self._tweaked_start_command_strings()
                bundle.after.spanner_starts.extend(strings)
            if (leaf is self[-1] or
                not next_leaf or
                not self._is_beamable(next_leaf, beam_rests=self.beam_rests)):
                string = self._stop_command_string()
                for spanner_start in bundle.after.spanner_starts:
                    if '[' in spanner_start:
                        bundle.after.spanner_starts.append(string)
                        break
                else:
                    bundle.after.spanner_stops.append(string)

    def _add_stemlet_length(self, leaf, bundle):
        if self.stemlet_length is None:
            return
        if leaf is self[0]:
            parentage = inspect(leaf).parentage()
            staff = parentage.get_first(Staff)
            lilypond_type = staff.lilypond_type
            string = r'\override {}.Stem.stemlet-length = {}'
            string = string.format(lilypond_type, self.stemlet_length)
            bundle.before.commands.append(string)
        if leaf is self[-1]:
            parentage = inspect(leaf).parentage()
            staff = parentage.get_first(Staff)
            lilypond_type = staff.lilypond_type
            string = r'\revert {}.Stem.stemlet-length'
            string = string.format(lilypond_type, self.stemlet_length)
            bundle.before.commands.append(string)

    @staticmethod
    def _coerce_durations(durations) -> typing.Tuple[Duration, ...]:
        durations = durations or []
        assert isinstance(durations, collections.Iterable)
        durations = [Duration(_) for _ in durations]
        return tuple(durations)

    def _copy_keywords(self, new):
        Spanner._copy_keywords(self, new)
        new._beam_lone_notes = self.beam_lone_notes
        new._beam_rests = self.beam_rests
        new._direction = self.direction
        if self.durations is not None:
            new._durations = self.durations[:]
        new._span_beam_count = self.span_beam_count
        new._stemlet_length = self.stemlet_length

    def _fracture_left(self, i):
        self, left, right = Spanner._fracture_left(self, i)
        if self.durations:
            weights = [
                inspect(left).duration(),
                inspect(right).duration(),
                ]
            assert sum(self.durations) == sum(weights)
            split_durations = sequence(self.durations)
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
        self, left, right = Spanner._fracture_right(self, i)
        if self.durations:
            weights = [
                inspect(left).duration(),
                inspect(right).duration(),
                ]
            assert sum(self.durations) == sum(weights)
            split_durations = sequence(self.durations)
            split_durations = split_durations.split(
                weights,
                cyclic=False,
                overhang=False,
                )
            left_durations, right_durations = split_durations
            left._durations = left_durations
            right._durations = right_durations
        return self, left, right

    def _get_beam_count_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        self._add_stemlet_length(leaf, bundle)
        self._add_beam_counts(leaf, bundle)
        self._add_start_and_stops(leaf, bundle)
        return bundle

    def _get_left_right_for_exterior_leaf(self, leaf):
        # lone
        if self._is_my_only(leaf):
            left, right = None, None
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
        # [beamable leaf unbeamable]
        elif (self._is_beamable(
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

    def _get_lilypond_format_bundle(self, leaf):
        if self.durations:
            return self._get_beam_count_lilypond_format_bundle(leaf)
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if not self._is_beamable(leaf, beam_rests=self.beam_rests):
            return bundle
        beamable_leaf_count = 0
        for leaf_ in self.leaves:
            if self._is_beamable(leaf_, beam_rests=self.beam_rests):
                beamable_leaf_count += 1
        if self.beam_lone_notes or 2 <= beamable_leaf_count:
            previous_leaf = leaf._get_leaf(-1)
            if previous_leaf not in self.leaves:
                previous_leaf = None
            if (previous_leaf in self.leaves and
                self._is_beamable(
                    previous_leaf,
                    beam_rests=self.beam_rests,
                    )):
                previous_leaf_is_beamable = True
            else:
                previous_leaf_is_beamable = False
            next_leaf = leaf._get_leaf(1)
            if (next_leaf in self.leaves and
                self._is_beamable(
                    next_leaf,
                    beam_rests=self.beam_rests,
                    )):
                next_leaf_is_beamable = True
            else:
                next_leaf_is_beamable = False
            start_pieces = []
            stop_piece = None
            if leaf is self[0]:
                if next_leaf_is_beamable or self.beam_lone_notes:
                    start_pieces = self._tweaked_start_command_strings()
            else:
                if (not previous_leaf_is_beamable and
                    (next_leaf_is_beamable or self.beam_lone_notes)):
                    start_pieces = self._tweaked_start_command_strings()
            if leaf is self[-1]:
                if previous_leaf_is_beamable or self.beam_lone_notes:
                    stop_piece = self._stop_command_string()
            else:
                if ((previous_leaf_is_beamable or self.beam_lone_notes) and
                    not next_leaf_is_beamable):
                    stop_piece = self._stop_command_string()
            if start_pieces and stop_piece:
                bundle.after.spanner_starts.extend(start_pieces)
                bundle.after.spanner_starts.append(stop_piece)
            elif start_pieces:
                bundle.after.spanner_starts.extend(start_pieces)
            elif stop_piece:
                bundle.after.spanner_stops.append(stop_piece)
        self._add_stemlet_length(leaf, bundle)
        return bundle

    def _get_span_beam_offsets(self):
        offsets = []
        if self.durations:
            offset = Offset(self.durations[0])
            offsets.append(offset)
            for duration in self.durations[1:]:
                offset = offsets[-1] + duration
                offsets.append(offset)
            offsets.pop()
        return offsets

    @staticmethod
    def _is_beamable(argument, beam_rests=False) -> bool:
        """
        Is true when ``argument`` is a beamable component.

        ..  container:: example

            Without allowing for beamed rests:

            >>> staff = abjad.Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
            >>> staff.extend(r"r8 e''8 ( ef'2 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> for leaf in staff:
            ...     result = abjad.Beam._is_beamable(leaf)
            ...     print(f'{str(leaf):<8}\t{result}')
            ...
            r32     False
            a'32    True
            gs'32   True
            fs''32  True
            f''8    True
            r8      False
            e''8    True
            ef'2    False

        ..  container:: example

            Allowing for beamed rests:

            >>> staff = abjad.Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
            >>> staff.extend(r"r8 e''8 ( ef'2 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> for leaf in staff:
            ...     result = abjad.Beam._is_beamable(
            ...         leaf,
            ...         beam_rests=True,
            ...         )
            ...     print(f'{str(leaf):<8}\t{result}')
            ...
            r32	True
            a'32	True
            gs'32	True
            fs''32	True
            f''8	True
            r8	True
            e''8	True
            ef'2	False

        ..  container:: example

            Is true for skips of any duration when ``beam_rests`` is true:

            >>> skip = abjad.Skip((1, 32))
            >>> abjad.Beam._is_beamable(skip, beam_rests=True)
            True

            >>> skip = abjad.Skip((1))
            >>> abjad.Beam._is_beamable(skip, beam_rests=True)
            True

        ..  container:: example

            Is true for rests of any duration when ``beam_rests`` is true:

            >>> rest = abjad.Rest((1, 32))
            >>> abjad.Beam._is_beamable(rest, beam_rests=True)
            True

            >>> rest = abjad.Rest((1))
            >>> abjad.Beam._is_beamable(rest, beam_rests=True)
            True

        """
        if isinstance(argument, (Chord, Note)):
            if 0 < argument.written_duration.flag_count:
                return True
        prototype = (
            MultimeasureRest,
            Rest,
            Skip,
            )
        if beam_rests and isinstance(argument, prototype):
            return True
        return False

    def _is_just_left_of_gap(self, leaf):
        local_stop_offset = self._stop_offset_in_me(leaf)
        span_beam_offsets = self._get_span_beam_offsets()
        if local_stop_offset in span_beam_offsets:
            return True
        return False

    def _is_just_right_of_gap(self, leaf):
        local_start_offset = self._start_offset_in_me(leaf)
        span_beam_offsets = self._get_span_beam_offsets()
        if local_start_offset in span_beam_offsets:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def beam_lone_notes(self) -> typing.Optional[bool]:
        r"""
        Is true when beam should include lone notes.

        ..  todo:: Teach durated beams to respect ``beam_lone_notes``.

        ..  container:: example

            Does not beam lone notes:

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam()
            >>> abjad.attach(beam, staff[:1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> staff = abjad.Staff("c'8 d'4 e'8 f'4 g'8")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam()
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    d'4
                    e'8
                    f'4
                    g'8
                }

        ..  container:: example

            Does beam lone notes:

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(beam_lone_notes=True)
            >>> abjad.attach(beam, staff[:1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    [
                    ]
                    d'8
                    e'8
                    f'8
                }

            >>> staff = abjad.Staff("c'8 d'4 e'8 f'4 g'8")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(beam_lone_notes=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    [
                    ]
                    d'4
                    e'8
                    [
                    ]
                    f'4
                    g'8
                    [
                    ]
                }

        """
        return self._beam_lone_notes

    @property
    def beam_rests(self) -> typing.Optional[bool]:
        r"""
        Is true when beam should include rests.

        ..  container:: example

            Without beamed rests:

            >>> staff = abjad.Staff("c'8 d'8 r8 f'8 g'8 r4.")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam()
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                [
                d'8
                ]
                r8
                f'8
                [
                g'8
                ]
                r4.
            }

            Abjad beams no rests.

            LilyPond beams no rests.

        ..  container:: example

            With beamed rests:

            >>> staff = abjad.Staff("c'8 d'8 r8 f'8 g'8 r4.")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(beam_rests=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                [
                d'8
                r8
                f'8
                g'8
                r4.
                ]
            }

            Abjad beams all rests.

            LilyPond beams only small-duration rests.

        ..  container:: example

            With beamed rests:

            >>> staff = abjad.Staff("c'8 d'8 r4. f'8 g'8 r8")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(beam_rests=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                [
                d'8
                r4.
                f'8
                g'8
                r8
                ]
            }

            Abjad beams all rests.

            LilyPond beams only small-duration rests.

        ..  container:: example

            With beamed skips:

            >>> staff = abjad.Staff("c'8 d'8 s4. f'8 g'8 s8")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(beam_rests=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                [
                d'8
                s4.
                f'8
                g'8
                s8
                ]
            }

            Abjad beams all skips.

            LilyPond beams all (internal) skips.

        """
        return self._beam_rests

    @property
    def direction(self) -> typing.Optional[String]:
        """
        Gets direction.
        """
        return self._direction
        
    @property
    def durations(self) -> typing.Tuple[Duration, ...]:
        r"""
        Gets durations.

        ..  container:: example

            Two groups:

            >>> staff = abjad.Staff("c'16 d'16 e'16 f'16")
            >>> durations = [(1, 8), (1, 8)]
            >>> beam = abjad.Beam(durations=durations)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 2
                    c'16
                    [
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 1
                    d'16
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 2
                    e'16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 0
                    f'16
                    ]
                }

            >>> beam.durations
            (Duration(1, 8), Duration(1, 8))

        ..  container:: example

            Three groups:

            >>> staff = abjad.Staff("c'16 d'16 e'8 f'16 c'16")
            >>> abjad.setting(staff).auto_beaming = False
            >>> durations = [(1, 8), (1, 8), (1, 8)]
            >>> beam = abjad.Beam(
            ...     durations=durations,
            ...     span_beam_count=1,
            ...     )
            >>> abjad.attach(beam, staff[:])
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
                    \set stemRightBeamCount = 1
                    d'16
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    e'8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 2
                    f'16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 0
                    c'16
                    ]
                }

            Test ensures that leaf groups format correctly when they contain
            only one leaf.

        """
        return self._durations

    @property
    def span_beam_count(self) -> int:
        r"""
        Gets span beam count.

        ..  container:: example

            Creates a single span beam between adjacent groups in spanner:

            >>> staff = abjad.Staff("c'32 d'32 e'32 f'32")
            >>> durations = [(1, 16), (1, 16)]
            >>> beam = abjad.Beam(
            ...     durations=durations,
            ...     span_beam_count=1,
            ...     )
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 3
                    c'32
                    [
                    \set stemLeftBeamCount = 3
                    \set stemRightBeamCount = 1
                    d'32
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 3
                    e'32
                    \set stemLeftBeamCount = 3
                    \set stemRightBeamCount = 0
                    f'32
                    ]
                }

            >>> beam.span_beam_count
            1

        ..  container:: example

            Creates a double span beam between adjacent groups in spanner:

            >>> staff = abjad.Staff("c'32 d'32 e'32 f'32")
            >>> durations = [(1, 16), (1, 16)]
            >>> beam = abjad.Beam(
            ...     durations=durations,
            ...     span_beam_count=2,
            ...     )
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 3
                    c'32
                    [
                    \set stemLeftBeamCount = 3
                    \set stemRightBeamCount = 2
                    d'32
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 3
                    e'32
                    \set stemLeftBeamCount = 3
                    \set stemRightBeamCount = 0
                    f'32
                    ]
                }

            >>> beam.span_beam_count
            2

        ..  container:: example

            Creates no span beam between adjacent groups in spanner:

            >>> staff = abjad.Staff("c'32 d'32 e'32 f'32")
            >>> durations = [(1, 16), (1, 16)]
            >>> beam = abjad.Beam(
            ...     durations=durations,
            ...     span_beam_count=0,
            ...     )
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 3
                    c'32
                    [
                    \set stemLeftBeamCount = 3
                    \set stemRightBeamCount = 0
                    d'32
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 3
                    e'32
                    \set stemLeftBeamCount = 3
                    \set stemRightBeamCount = 0
                    f'32
                    ]
                }

            >>> beam.span_beam_count
            0

        """
        return self._span_beam_count

    @property
    def stemlet_length(self) -> typing.Optional[typings.Number]:
        r"""
        Gets stemlet length.

        ..  container:: example

            >>> staff = abjad.Staff(
            ...     "r8 c' r c' g'2",
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(beam_rests=True, stemlet_length=2)
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
                    r8
                    [
                    c'8
                    r8
                    \revert RhythmicStaff.Stem.stemlet-length
                    c'8
                    ]
                    g'2
                }

        """
        return self._stemlet_length
