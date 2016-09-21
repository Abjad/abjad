# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Fermata(AbjadValueObject):
    r'''A fermata.

    ..  container:: example

        **Example 1.** A short fermata:

        ::

            >>> score = Score([Staff([Note("c'4")])])
            >>> fermata = indicatortools.Fermata(command='shortfermata')
            >>> attach(fermata, score[0][0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    c'4 \shortfermata
                }
            >>

    ..  container:: example

        **Example 2.** A fermata:

        ::

            >>> score = Score([Staff([Note("c'4")])])
            >>> fermata = indicatortools.Fermata()
            >>> attach(fermata, score[0][0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    c'4 \fermata
                }
            >>

    ..  container:: example

        **Example 3.** A long fermata:

        ::

            >>> score = Score([Staff([Note("c'4")])])
            >>> fermata = indicatortools.Fermata('longfermata')
            >>> attach(fermata, score[0][0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    c'4 \longfermata
                }
            >>

    ..  container:: example

        **Example 4.** A very long fermata:

        ::

            >>> score = Score([Staff([Note("c'4")])])
            >>> fermata = indicatortools.Fermata('verylongfermata')
            >>> attach(fermata, score[0][0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    c'4 \verylongfermata
                }
            >>

    '''

    ### CLASS VARIABLES ###

    _allowable_commands = (
        'fermata',
        'longfermata',
        'shortfermata',
        'verylongfermata',
        )

    __slots__ = (
        '_command',
        '_default_scope',
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, command='fermata'):
        from abjad.tools import scoretools
        assert command in self._allowable_commands, repr(command)
        self._command = command
        self._default_scope = scoretools.Score

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of fermata.

        ..  container:: example

            **Example 1.** Fermata:

            ::

                >>> str(indicatortools.Fermata())
                '\\fermata'

        ..  container:: example

            **Example 2.** Long fermata:

            ::

                >>> str(indicatortools.Fermata('longfermata'))
                '\\longfermata'

        Returns string.
        '''
        return r'\{}'.format(self.command)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_commands():
        r'''Lists allowable commands:

        ..  container:: example

            **Example 1.** All allowable commands:

            ::

                >>> commands = indicatortools.Fermata.list_allowable_commands()
                >>> for command in commands:
                ...     command
                'fermata'
                'longfermata'
                'shortfermata'
                'verylongfermata'

        Returns tuple of strings.
        '''
        return Fermata._allowable_commands

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

            **Example 1.** Fermata:

            ::

                >>> fermata = indicatortools.Fermata()
                >>> fermata.command
                'fermata'

        ..  container:: example

            **Example 2.** Long fermata:

            ::

                >>> fermata = indicatortools.Fermata('longfermata')
                >>> fermata.command
                'longfermata'

        Returns string.
        '''
        return self._command

    @property
    def default_scope(self):
        r'''Gets default scope of fermata.

        ..  container:: example

            **Example 1.** Fermata:

            ::

                >>> fermata = indicatortools.Fermata()
                >>> fermata.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        ..  container:: example

            **Example 2.** Long fermata:

            ::

                >>> fermata = indicatortools.Fermata('longfermata')
                >>> fermata.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        Fermatas are score-scoped by default.

        Returns score.
        '''
        return self._default_scope
