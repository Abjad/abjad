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
        '_default_scope',
        )

    _format_slot = 'right'

    _split_direction = Right

    ### INITIALIZER ###

    def __init__(self):
        self._default_scope = None

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
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of laissez vibrer indicator.

        ..  container:: example

            Default:

            ::

                >>> indicator = abjad.LaissezVibrer()
                >>> indicator.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope
