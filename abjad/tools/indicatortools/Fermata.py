# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Fermata(AbjadValueObject):
    r'''A fermata.

    ..  container:: example

        Fermata:

        ::

            >>> note = Note("c'4")
            >>> fermata = indicatortools.Fermata()
            >>> attach(fermata, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 \fermata

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_command',
        )


    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, command='fermata'):
        assert command in (
            'shortfermata',
            'fermata',
            'longfermata',
            'verylongfermata',
            ), repr(fermata)
        self._command = command

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of fermata.

        ..  container:: example

            ::

                >>> str(indicatortools.Fermata())
                '\\fermata'

        Returns string.
        '''
        return r'\{}'.format(self.command)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        r'''Gets command of fermata.

        ..  container:: example

            ::

                >>> fermata = indicatortools.Fermata()
                >>> fermata.command
                'fermata'

        Returns string.
        '''
        return self._command