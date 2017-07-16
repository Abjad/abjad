# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Staccato(AbjadValueObject):
    r'''Staccato.

    ::

        >>> import abjad

    ..  container:: example

        Attached to a single note:

        ::

            >>> note = abjad.Note("c'4")
            >>> staccato = abjad.Staccato()
            >>> abjad.attach(staccato, note)
            >>> show(note) # doctest: +SKIP

        ..  docs::

            >>> f(note)
            c'4 \staccato

    ..  container:: example

        Attached to notes in a staff:

        ::

            >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
            >>> abjad.attach(abjad.Beam(), staff[:4])
            >>> abjad.attach(abjad.Beam(), staff[4:])
            >>> abjad.attach(abjad.Staccato(), staff[3])
            >>> abjad.attach(abjad.Staccato(), staff[7])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'8
                e'8
                f'8 ]
                \staccato
                g'8 [
                a'8
                b'8
                c''8 ]
                \staccato
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        )

    _default_scope = None

    _format_slot = Right

    _split_direction = Right

    ### INITIALIZER ###

    def __init__(self, direction=None):
        direction = datastructuretools.String.to_tridirectional_ordinal_constant(
            direction)
        directions = (Up, Down, Center, None)
        assert direction in directions, repr(direction)
        self._direction = direction

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of staccato.

        ..  container:: example

            ::

                >>> str(abjad.Staccato())
                '\\staccato'

        Returns string.
        '''
        return r'\staccato'

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.after.commands.append(str(self))
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of staccato.

        ..  container:: example

            ::

                >>> staccato = abjad.Staccato()
                >>> staccato.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope
