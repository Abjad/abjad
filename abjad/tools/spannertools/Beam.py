# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override


class Beam(Spanner):
    r'''Beam.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
            >>> abjad.setting(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                c'8
                d'8
                e'8
                f'8
                g'2
            }

        ::

            >>> beam = abjad.Beam()
            >>> abjad.attach(beam, staff[:2])
            >>> beam = abjad.Beam()
            >>> abjad.attach(beam, staff[2:4])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                c'8 [
                d'8 ]
                e'8 [
                f'8 ]
                g'2
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        direction = datastructuretools.String.to_tridirectional_lilypond_symbol(
            direction)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        Spanner._copy_keyword_args(self, new)
        new._direction = self.direction

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_first_leaf(leaf):
            if self.direction is not None:
                string = '{} ['.format(self.direction)
            else:
                string = '['
            bundle.right.spanner_starts.append(string)
        if self._is_my_last_leaf(leaf):
            string = ']'
            if self._is_my_first_leaf(leaf):
                bundle.right.spanner_starts.append(string)
            else:
                bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def _is_beamable(argument, beam_rests=False):
        '''Is true when `argument` is a beamable component. Otherwise false.

        ..  container:: example

            Without allowing for beamed rests:

            ::

                >>> staff = abjad.Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
                >>> staff.extend(r"r8 e''8 ( ef'2 )")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> for leaf in staff:
                ...     result = abjad.Beam._is_beamable(leaf)
                ...     print('{:<8}\t{}'.format(leaf, result))
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

            ::

                >>> staff = abjad.Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
                >>> staff.extend(r"r8 e''8 ( ef'2 )")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> for leaf in staff:
                ...     result = abjad.Beam._is_beamable(
                ...         leaf,
                ...         beam_rests=True,
                ...         )
                ...     print('{:<8}\t{}'.format(leaf, result))
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

            Is true for skips of any duration when `beam_rests` is true:

            ::

                >>> skip = abjad.Skip((1, 32))
                >>> abjad.Beam._is_beamable(skip, beam_rests=True)
                True

            ::

                >>> skip = abjad.Skip((1))
                >>> abjad.Beam._is_beamable(skip, beam_rests=True)
                True

        ..  container:: example

            Is true for rests of any duration when `beam_rests` is true:

            ::

                >>> rest = abjad.Rest((1, 32))
                >>> abjad.Beam._is_beamable(rest, beam_rests=True)
                True

            ::

                >>> rest = abjad.Rest((1))
                >>> abjad.Beam._is_beamable(rest, beam_rests=True)
                True

        Returns true or false.
        '''
        from abjad.tools import scoretools
        prototype = (scoretools.Note, scoretools.Chord)
        if isinstance(argument, prototype):
            if 0 < argument.written_duration.flag_count:
                return True
        prototype = (
            scoretools.MultimeasureRest,
            scoretools.Rest,
            scoretools.Skip,
            )
        if beam_rests and isinstance(argument, prototype):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction.

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction
