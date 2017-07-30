# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LaissezVibrer(AbjadValueObject):
    r'''Laissez vibrer.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> chord = abjad.Chord("<c' e' g' c''>4")
            >>> laissez_vibrer = abjad.LaissezVibrer()
            >>> abjad.attach(laissez_vibrer, chord)
            >>> show(chord) # doctest: +SKIP

        ..  docs::

            >>> f(chord)
            <c' e' g' c''>4 \laissezVibrer

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _format_slot = 'right'

    _time_orientation = Right

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of laissez vibrer indicator.

        ..  container:: example

            Default:

            ::

                >>> str(abjad.LaissezVibrer())
                '\\laissezVibrer'
                    
        Returns string.
        '''
        return r'\laissezVibrer'

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.right.articulations.append(self._get_lilypond_format())
        return bundle
