import typing
from abjad import Center, Down, Up, VerticalAlignment
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.systemtools.LilyPondFormatBundle import LilyPondFormatBundle


class Arpeggio(AbjadValueObject):
    r'''
    Arpeggio.

    ..  container:: example

        Without direction arrow:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio()
        >>> abjad.attach(arpeggio, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <c' e' g' c''>4
            \arpeggio

    ..  container:: example

        With direction arrow:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio(direction=abjad.Down)
        >>> abjad.attach(arpeggio, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            \arpeggioArrowDown
            <c' e' g' c''>4
            \arpeggio

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: VerticalAlignment = None,
        ) -> None:
        if direction is not None:
            assert direction in (Up, Down, Center)
        self._direction = direction

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return r'\arpeggio'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        bundle.right.articulations.append(r'\arpeggio')
        if self.direction in (Up, Down):
            if self.direction is Up:
                command = r'\arpeggioArrowUp'
            else:
                command = r'\arpeggioArrowDown'
            bundle.before.commands.append(command)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[VerticalAlignment]:
        '''
        Gets direction of arpeggio.

        ..  container:: example

            Without direction arrow:

            >>> arpeggio = abjad.Arpeggio()
            >>> arpeggio.direction is None
            True

        ..  container:: example

            With direction arrow:

            >>> arpeggio = abjad.Arpeggio(direction=abjad.Down)
            >>> arpeggio.direction
            Down

        '''
        return self._direction
