# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Staccatissimo(AbjadValueObject):
    r'''Staccatissimo.

    ..  container:: example

        Attached to a single note:

        ::

            >>> note = Note("c'4")
            >>> staccatissimo = Staccatissimo()
            >>> attach(staccatissimo, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> f(note)
            c'4 \staccatissimo

    ..  container:: example

        Attached to notes in a staff:

        ::

            >>> staff = Staff("c'8 d' e' f' g' a' b' c''")
            >>> attach(Beam(), staff[:4])
            >>> attach(Beam(), staff[4:])
            >>> attach(Staccatissimo(), staff[3])
            >>> attach(Staccatissimo(), staff[7])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'8
                e'8
                f'8 ]
                \staccatissimo
                g'8 [
                a'8
                b'8
                c''8 ]
                \staccatissimo
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
        direction = stringtools.to_tridirectional_ordinal_constant(direction)
        directions = (Up, Down, Center, None)
        assert direction in directions, repr(direction)
        self._direction = direction

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of staccatissimo.

        ..  container:: example

            ::

                >>> str(Staccatissimo())
                '\\staccatissimo'

        Returns string.
        '''
        return r'\staccatissimo'

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
        r'''Gets default scope of staccatissimo.

        ..  container:: example

            ::

                >>> staccatissimo = Staccatissimo()
                >>> staccatissimo.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope
