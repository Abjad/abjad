from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Fermata(AbjadValueObject):
    r'''Fermata.

    ..  container:: example

        A short fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata(command='shortfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \shortfermata
                }
            >>

    ..  container:: example

        A fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata()
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \fermata
                }
            >>

    ..  container:: example

        A long fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata('longfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \longfermata
                }
            >>

    ..  container:: example

        A very long fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata('verylongfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \verylongfermata
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
        )

    _context = 'Score'

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, command='fermata'):
        assert command in self._allowable_commands, repr(command)
        self._command = command

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of fermata.

        ..  container:: example

            Fermata:

            >>> str(abjad.Fermata())
            '\\fermata'

        ..  container:: example

            Long fermata:

            >>> str(abjad.Fermata('longfermata'))
            '\\longfermata'

        Returns string.
        '''
        return r'\{}'.format(self.command)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.right.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_commands():
        r'''Lists allowable commands:

        ..  container:: example

            All allowable commands:

            >>> commands = abjad.Fermata.list_allowable_commands()
            >>> for command in commands:
            ...     command
            'fermata'
            'longfermata'
            'shortfermata'
            'verylongfermata'

        Returns tuple of strings.
        '''
        return Fermata._allowable_commands

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        r'''Gets command of fermata.

        ..  container:: example

            Fermata:

            >>> fermata = abjad.Fermata()
            >>> fermata.command
            'fermata'

        ..  container:: example

            Long fermata:

            >>> fermata = abjad.Fermata('longfermata')
            >>> fermata.command
            'longfermata'

        Returns string.
        '''
        return self._command

    @property
    def context(self):
        r'''Gets (historically conventional) context.

        ..  container:: example

            Fermata:

            >>> fermata = abjad.Fermata()
            >>> fermata.context
            'Score'

        ..  container:: example

            Long fermata:

            >>> fermata = abjad.Fermata('longfermata')
            >>> fermata.context
            'Score'

        Returns ``'Score'``.

        Override with ``abjad.attach(..., context='...')``.
        '''
        return self._context
