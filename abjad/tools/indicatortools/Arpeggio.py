# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Arpeggio(AbjadValueObject):
    r'''An arpeggio indication.

    ::

        >>> chord = Chord("<c' e' g' c''>4")
        >>> arpeggio = indicatortools.Arpeggio()
        >>> attach(arpeggio, chord)
        >>> show(chord) # doctest: +SKIP

    ..  doctest::

        >>> print(format(chord))
        <c' e' g' c''>4 \arpeggio

    An arpeggio arrow direction can be specified:

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
        '_direction',
        )

    ### INITIALIZER ###

    def __init__(self, direction=None):
        if direction is not None:
            assert direction in (Up, Down, Center)
        self._direction = direction

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return r'\arpeggio'

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

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets arpeggio arrow direction.

        Return ordinal constant or none.
        '''
        return self._direction