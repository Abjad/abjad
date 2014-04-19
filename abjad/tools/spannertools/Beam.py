# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override


class Beam(Spanner):
    r'''A beam.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8 g'2")
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

            >>> beam = Beam()
            >>> attach(beam, staff[:2])
            >>> beam = Beam()
            >>> attach(beam, staff[2:4])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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
        direction = stringtools.arg_to_tridirectional_lilypond_symbol(
            direction)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        Spanner._copy_keyword_args(self, new)
        new._direction = self.direction

    def _get_lilypond_format_bundle(self, leaf):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        if self._is_my_first_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'override',
                is_once=False,
                )
            lilypond_format_bundle.grob_overrides.extend(contributions)
            if self.direction is not None:
                string = '{} ['.format(self.direction)
            else:
                string = '['
            lilypond_format_bundle.right.spanner_starts.append(string)
        if self._is_my_last_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'revert',
                )
            lilypond_format_bundle.grob_reverts.extend(contributions)
            string = ']'
            if self._is_my_first_leaf(leaf):
                lilypond_format_bundle.right.spanner_starts.append(string)
            else:
                lilypond_format_bundle.right.spanner_stops.append(string)
        return lilypond_format_bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def _is_beamable_component(expr):
        '''Is true when `expr` is a beamable component. Otherwise false.

        ::

            >>> staff = Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
            >>> staff.extend(r"r8 e''8 ( ef'2 )")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> for leaf in staff.select_leaves():
            ...     beam = spannertools.Beam
            ...     result = beam._is_beamable_component(leaf)
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

        Returns boolean.
        '''
        from abjad.tools import scoretools
        if isinstance(expr, (scoretools.Note, scoretools.Chord)):
            if 0 < expr.written_duration.flag_count:
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction of beam.

        Returns up or down.
        '''
        return self._direction
