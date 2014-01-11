# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Arpeggio(AbjadObject):
    r'''An arpeggio indication.

    ::

        >>> chord = Chord("<c' e' g' c''>4")
        >>> arpeggio = indicatortools.Arpeggio()
        >>> attach(arpeggio, chord)
        >>> show(chord) # doctest: +SKIP

    ..  doctest::

        >>> print format(chord)
        <c' e' g' c''>4 \arpeggio

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is an arpeggio indication. Otherwise false.

        Returns boolean.
        '''
        return type(expr) == type(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return r'\arpeggio'
