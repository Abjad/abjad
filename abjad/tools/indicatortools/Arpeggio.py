# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Arpeggio(AbjadValueObject):
    r'''Arpeggio.

    ::

        >>> import abjad

    ..  container:: example

        Without direction arrow:

        ::

            >>> chord = abjad.Chord("<c' e' g' c''>4")
            >>> arpeggio = abjad.Arpeggio()
            >>> abjad.attach(arpeggio, chord)
            >>> show(chord) # doctest: +SKIP

        ..  docs::

            >>> f(chord)
            <c' e' g' c''>4 \arpeggio

    ..  container:: example

        With direction arrow:

        ::

            >>> chord = abjad.Chord("<c' e' g' c''>4")
            >>> arpeggio = abjad.Arpeggio(direction=Down)
            >>> abjad.attach(arpeggio, chord)
            >>> show(chord) # doctest: +SKIP

        ..  docs::

            >>> f(chord)
            \arpeggioArrowDown
            <c' e' g' c''>4 \arpeggio

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        )

    ### INITIALIZER ###

    def __init__(self, direction=None):
        if direction is not None:
            assert direction in (Up, Down, Center)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return r'\arpeggio'

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.right.articulations.append(r'\arpeggio')
        if self.direction in (Up, Down):
            if self.direction == Up:
                command = r'\arpeggioArrowUp'
            else:
                command = r'\arpeggioArrowDown'
            bundle.before.commands.append(command)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction of arpeggio.

        ..  container:: example

            Without direction arrow:

            ::

                >>> arpeggio = abjad.Arpeggio()
                >>> arpeggio.direction is None
                True

        ..  container:: example

            With direction arrow:

            ::

                >>> arpeggio = abjad.Arpeggio(direction=Down)
                >>> arpeggio.direction
                Down

        Returns ordinal constant or none.
        '''
        return self._direction
