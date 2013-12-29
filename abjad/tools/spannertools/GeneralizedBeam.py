# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner


class GeneralizedBeam(Spanner):
    r'''A generalized beam.

    ..  container:: example::

        ::

            >>> staff = Staff("r4 c'8 d'16 e'16 r8 fs'8 g'4")
            >>> contextualize(staff).auto_beaming = False
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
                c'8 [
                d'16
                e'16 ]
                r8
                fs'8
                g'4
            }

    ..  container:: example

        ::

            >>> staff = Staff("r4 c'8 d'16 e'16 r8 fs'8 g'4")
            >>> contextualize(staff).auto_beaming = False
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
                c'8 [
                d'16
                e'16 ]
                r8
                fs'8 [ ]
                g'4
            }

    ..  container:: example::

        ::

            >>> staff = Staff("r4 c'8 d'16 e'16 r8 fs'8 g'4")
            >>> contextualize(staff).auto_beaming = False
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
                c'8 [
                d'16
                e'16
                r8
                fs'8 ]
                g'4
                \revert Stem.stemlet-length
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_long_duration_notes',
        '_include_long_duration_rests',
        '_isolated_nib_direction',
        '_use_stemlets'
        '_vertical_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        include_long_duration_notes=False,
        include_long_duration_rests=False,
        isolated_nib_direction=None,
        use_stemlets=False,
        vertical_direction=None,
        ):
        Spanner.__init__(
            self,
            components=components,
            )
        self._include_long_duration_notes = bool(include_long_duration_notes)
        self._include_long_duration_rests = bool(include_long_duration_rests)
        assert isolated_nib_direction in (Left, Right, None)
        self._isolated_nib_direction = isolated_nib_direction
        self._use_stemlets = bool(use_stemlets)
        assert vertical_direction in (Up, Down, Center, None)
        self._vertical_direction = vertical_direction

    ### PUBLIC PROPERTIES ###

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

    def _format_before_leaf(self, leaf):
        result = []
        if self.use_stemlets and self._is_my_first_leaf(leaf):
            result.append(r'\override Stem.stemlet-length = 0.75')
        if not self.is_beamable_component(leaf):
            return result
        leaf_ids = [id(x) for x in self.leaves]
        previous_leaf_is_joinable = self._leaf_is_joinable(
            leaf._get_leaf(-1), leaf_ids)
        next_leaf_is_joinable = self._leaf_is_joinable(
            leaf._get_leaf(1), leaf_ids)
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        if not self.is_beamable_component(leaf):
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
        leaf_ids = [id(x) for x in self.leaves]
        previous_leaf_is_joinable = self._leaf_is_joinable(
            leaf._get_leaf(-1), leaf_ids)
        next_leaf_is_joinable = self._leaf_is_joinable(
            leaf._get_leaf(1), leaf_ids)
        if not previous_leaf_is_joinable:
            if not next_leaf_is_joinable:
                if self.isolated_nib_direction is not None:
                    result.append('{}['.format(direction_string))
                    result.append(']')
            else:
                result.append('{}['.format(direction_string))
        elif not next_leaf_is_joinable:
            result.append(']')
        return result

    def _format_after_leaf(self, leaf):
        result = []
        if self.use_stemlets and self._is_my_last_leaf(leaf):
            result.append(r'\revert Stem.stemlet-length')
        if not self.is_beamable_component(leaf):
            return result
        return result

    def _leaf_is_joinable(self, leaf, leaf_ids):
        if id(leaf) not in leaf_ids:
            return False
        if hasattr(leaf, 'written_pitch') or hasattr(leaf, 'written_pitches'):
            if self.is_beamable_component(leaf):
                return True
            elif self.include_long_duration_notes:
                return True
        else:
            if self.is_beamable_component(leaf) and self.use_stemlets:
                return True
            elif self.include_long_duration_rests:
                return True
        return False

    ### PUBLIC METHODS ###

    @staticmethod
    def is_beamable_component(expr):
        r'''True if `expr` is beamable, otherwise false.
        '''
        from abjad.tools import scoretools
        if isinstance(expr, scoretools.Leaf):
            if 0 < expr.written_duration.flag_count:
                return True
        return False
