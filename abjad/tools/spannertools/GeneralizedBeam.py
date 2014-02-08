# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner


class GeneralizedBeam(Spanner):
    r'''A generalized beam.

    ..  container:: example::

        ::

            >>> staff = Staff("r4 c'8 d'16 e'16 r8 fs'8 g'4")
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ::

            >>> beam = spannertools.GeneralizedBeam()
            >>> attach(beam, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                r4
                \set stemLeftBeamCount = 0
                \set stemRightBeamCount = 1
                c'8 [
                \set stemLeftBeamCount = 1
                \set stemRightBeamCount = 2
                d'16
                \set stemLeftBeamCount = 2
                \set stemRightBeamCount = 0
                e'16 ]
                r8
                fs'8
                g'4
            }

    ..  container:: example

        ::

            >>> staff = Staff("r4 c'8 d'16 e'16 r8 fs'8 g'4")
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ::

            >>> beam = spannertools.GeneralizedBeam(
            ...     isolated_nib_direction=Right,
            ...     )
            >>> attach(beam, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                r4
                \set stemLeftBeamCount = 0
                \set stemRightBeamCount = 1
                c'8 [
                \set stemLeftBeamCount = 1
                \set stemRightBeamCount = 2
                d'16
                \set stemLeftBeamCount = 2
                \set stemRightBeamCount = 0
                e'16 ]
                r8
                \set stemLeftBeamCount = 0
                \set stemRightBeamCount = 1
                fs'8 [ ]
                g'4
            }

    ..  container:: example::

        ::

            >>> staff = Staff("r4 c'8 d'16 e'16 r8 fs'8 g'4")
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ::

            >>> beam = spannertools.GeneralizedBeam(
            ...     use_stemlets=True,
            ...     )
            >>> attach(beam, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                \override Stem.stemlet-length = 0.75
                r4
                \set stemLeftBeamCount = 0
                \set stemRightBeamCount = 1
                c'8 [
                \set stemLeftBeamCount = 1
                \set stemRightBeamCount = 2
                d'16
                \set stemLeftBeamCount = 2
                \set stemRightBeamCount = 1
                e'16
                \set stemLeftBeamCount = 1
                \set stemRightBeamCount = 1
                r8
                \set stemLeftBeamCount = 1
                \set stemRightBeamCount = 0
                fs'8 ]
                g'4
                \revert Stem.stemlet-length
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_durations',
        '_include_long_duration_notes',
        '_include_long_duration_rests',
        '_isolated_nib_direction',
        '_use_stemlets',
        '_vertical_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        durations=None,
        include_long_duration_notes=False,
        include_long_duration_rests=False,
        isolated_nib_direction=None,
        use_stemlets=False,
        vertical_direction=None,
        ):
        Spanner.__init__(
            self,
            )
        if durations:
            durations = tuple(durationtools.Duration(x) for x in durations)
        self._durations = durations
        self._include_long_duration_notes = bool(include_long_duration_notes)
        self._include_long_duration_rests = bool(include_long_duration_rests)
        assert isolated_nib_direction in (Left, Right, None)
        self._isolated_nib_direction = isolated_nib_direction
        self._use_stemlets = bool(use_stemlets)
        assert vertical_direction in (Up, Down, Center, None)
        self._vertical_direction = vertical_direction

    ### PUBLIC PROPERTIES ###

    @property
    def durations(self):
        r'''Durations to use for span-beam groupings.
        '''
        return self._durations

    @property
    def include_long_duration_notes(self):
        r'''True if beam includes long duration notes, otherwise false.
        '''
        return self._include_long_duration_notes

    @property
    def include_long_duration_rests(self):
        r'''True if beam includes long duration rests, otherwise false.
        '''
        return self._include_long_duration_rests

    @property
    def isolated_nib_direction(self):
        r'''Direction of isolated nibs.
        '''
        return self._isolated_nib_direction

    @property
    def use_stemlets(self):
        r'''True if beam uses stemlets, otherwise false.
        '''
        return self._use_stemlets

    @property
    def vertical_direction(self):
        r'''Vertical direction of the beam.
        '''
        return self._vertical_direction

    ### PRIVATE METHODS ###

    def _format_after_leaf(self, leaf):
        from abjad.tools import lilypondnametools
        result = []
        if self.use_stemlets and self._is_my_last_leaf(leaf):
            override = lilypondnametools.LilyPondGrobOverride(
                grob_name='Stem',
                property_path=('stemlet-length',),
                value=0.75,
                )
            string = '\n'.join(override.revert_format_pieces)
            result.append(string)
        if not self._is_beamable_component(leaf):
            return result
        return result

    def _format_before_leaf(self, leaf):
        from abjad.tools import lilypondnametools
        result = []
        if self.use_stemlets and self._is_my_first_leaf(leaf):
            override = lilypondnametools.LilyPondGrobOverride(
                grob_name='Stem',
                property_path=('stemlet-length',),
                value=0.75,
                )
            string = '\n'.join(override.override_format_pieces)
            result.append(string)
        if not self._is_beamable_component(leaf):
            return result
        elif not self.use_stemlets and (
            not hasattr(leaf, 'written_pitch') and
            not hasattr(leaf, 'written_pitches')):
            return result
        leaf_ids = [id(x) for x in self._leaves]
        previous_leaf = leaf._get_leaf(-1)
        previous_leaf_is_joinable = self._leaf_is_joinable(
            previous_leaf, leaf_ids)
        next_leaf = leaf._get_leaf(1)
        next_leaf_is_joinable = self._leaf_is_joinable(next_leaf, leaf_ids)
        left, right = None, None
        # leaf is orphan
        if not previous_leaf_is_joinable and not next_leaf_is_joinable:
            if self.isolated_nib_direction is Left:
                left = leaf.written_duration.flag_count
                right = 0
            elif self.isolated_nib_direction is Right:
                left = 0
                right = leaf.written_duration.flag_count
        # leaf is first of group
        elif not previous_leaf_is_joinable:
            left = 0
            right = leaf.written_duration.flag_count
        # leaf is last of group
        elif not next_leaf_is_joinable:
            left = leaf.written_duration.flag_count
            right = 0
        # leaf is interior
        elif self._span_points:
            start_offset = self._start_offset_in_me(leaf)
            stop_offset = self._stop_offset_in_me(leaf)
            # leaf starts subgroup
            if start_offset in self._span_points and \
                not stop_offset in self._span_points:
                left = min(
                    previous_leaf.written_duration.flag_count,
                    leaf.written_duration.flag_count,
                    )
                left = (left - 1) or 1
                right = leaf.written_duration.flag_count
            # leaf stops subgroup
            elif stop_offset in self._span_points and \
                not start_offset in self._span_points:
                left = leaf.written_duration.flag_count
                right = min(
                    leaf.written_duration.flag_count,
                    next_leaf.written_duration.flag_count,
                    )
                right = (right - 1) or 1
            else:
                left = min(
                    previous_leaf.written_duration.flag_count,
                    leaf.written_duration.flag_count,
                    )
                right = min(
                    leaf.written_duration.flag_count,
                    next_leaf.written_duration.flag_count,
                    )
        # leaf is simple interior leaf
        else:
            left = min(
                previous_leaf.written_duration.flag_count,
                leaf.written_duration.flag_count,
                )
            right = min(
                leaf.written_duration.flag_count,
                next_leaf.written_duration.flag_count,
                )
        if left is not None:
            setting = lilypondnametools.LilyPondContextSetting(
                context_property='stemLeftBeamCount',
                value=left,
                )
            string = '\n'.join(setting.format_pieces)
            result.append(string)
        if right is not None:
            setting = lilypondnametools.LilyPondContextSetting(
                context_property='stemRightBeamCount',
                value=right,
                )
            string = '\n'.join(setting.format_pieces)
            result.append(string)
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        if not self._is_beamable_component(leaf):
            return result
        elif not self.use_stemlets and (
            not hasattr(leaf, 'written_pitch') and
            not hasattr(leaf, 'written_pitches')):
            return result
        direction_string = ''
        if self.vertical_direction is not None:
            direction_string = \
                stringtools.arg_to_tridirectional_lilypond_symbol(
                    self.vertical_direction)
        leaf_ids = [id(x) for x in self._leaves]
        previous_leaf = leaf._get_leaf(-1)
        next_leaf = leaf._get_leaf(1)
        previous_leaf_is_beamable = \
            self._is_beamable_component(previous_leaf) and \
            id(previous_leaf) in leaf_ids
        next_leaf_is_beamable = \
            self._is_beamable_component(next_leaf) and \
            id(next_leaf) in leaf_ids
        if not previous_leaf_is_beamable:
            if not next_leaf_is_beamable:
                if self.isolated_nib_direction is not None:
                    result.append('{}['.format(direction_string))
                    result.append(']')
            else:
                result.append('{}['.format(direction_string))
        elif not next_leaf_is_beamable:
            result.append(']')
        return result

    def _is_beamable_component(self, expr):
        r'''True if `expr` is beamable, otherwise false.
        '''
        from abjad.tools import scoretools
        if isinstance(expr, scoretools.Leaf):
            if 0 < expr.written_duration.flag_count:
                if hasattr(expr, 'written_pitch') or \
                    hasattr(expr, 'written_pitches'):
                    return True
                elif self.use_stemlets:
                    return True
        return False

    def _leaf_is_joinable(self, leaf, leaf_ids):
        if id(leaf) not in leaf_ids:
            return False
        if hasattr(leaf, 'written_pitch') or hasattr(leaf, 'written_pitches'):
            if self._is_beamable_component(leaf):
                return True
            elif self.include_long_duration_notes:
                return True
        else:
            if self._is_beamable_component(leaf) and self.use_stemlets:
                return True
            elif self.include_long_duration_rests:
                return True
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _span_points(self):
        if self.durations is not None:
            return mathtools.cumulative_sums(self.durations)[1:]
        return []

