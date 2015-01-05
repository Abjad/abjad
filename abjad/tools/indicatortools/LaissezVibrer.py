# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LaissezVibrer(AbjadValueObject):
    r'''A *laissez vibrer* indication.

    ::

        >>> chord = Chord("<c' e' g' c''>4")
        >>> laissez_vibrer = indicatortools.LaissezVibrer()
        >>> attach(laissez_vibrer, chord)
        >>> show(chord) # doctest: +SKIP

    ..  doctest::

        >>> print(format(chord))
        <c' e' g' c''>4 \laissezVibrer

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''String representation of laissez vibrer.

        Returns string.
        '''
        return r'\laissezVibrer'

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return str(self)