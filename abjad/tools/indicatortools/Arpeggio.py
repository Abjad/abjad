# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Arpeggio(AbjadValueObject):
    r'''An arpeggio.

    ..  container:: example

        **Example 1.** Without direction arrow:

        ::

            >>> chord = Chord("<c' e' g' c''>4")
            >>> arpeggio = indicatortools.Arpeggio()
            >>> attach(arpeggio, chord)
            >>> show(chord) # doctest: +SKIP

        ..  doctest::

            >>> print(format(chord))
            <c' e' g' c''>4 \arpeggio

    ..  container:: example

        **Example 2.** With direction arrow:

        ::

            >>> chord = Chord("<c' e' g' c''>4")
            >>> arpeggio = indicatortools.Arpeggio(direction=Down)
            >>> attach(arpeggio, chord)
            >>> show(chord) # doctest: +SKIP

        ..  doctest::

            >>> print(format(chord))
            \arpeggioArrowDown
            <c' e' g' c''>4 \arpeggio

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_direction',
        )

    ### INITIALIZER ###

    def __init__(self, direction=None):
        self._default_scope = None
        if direction is not None:
            assert direction in (Up, Down, Center)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(r'\arpeggio')
        if self.direction in (Up, Down):
            if self.direction == Up:
                command = r'\arpeggioArrowUp'
            else:
                command = r'\arpeggioArrowDown'
            lilypond_format_bundle.before.commands.append(command)
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return r'\arpeggio'

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of arpeggio.

        ..  container:: example

            ::

                >>> arpeggio = indicatortools.Arpeggio()
                >>> arpeggio.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope

    @property
    def direction(self):
        r'''Gets direction of arpeggio.

        ..  container:: example

            **Example 1.** Without direction arrow:

            ::

                >>> arpeggio = indicatortools.Arpeggio()
                >>> arpeggio.direction is None
                True

        ..  container:: example

            **Example 2.** With direction arrow:

            ::

                >>> arpeggio = indicatortools.Arpeggio(direction=Down)
                >>> arpeggio.direction
                Down

        Returns ordinal constant or none.
        '''
        return self._direction
