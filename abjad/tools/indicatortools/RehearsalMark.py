from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class RehearsalMark(AbjadValueObject):
    r'''Rehearsal mark.

    ..  container:: example

        Rehearsal A:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> mark = abjad.RehearsalMark(number=1)
        >>> abjad.attach(mark, staff[0])
        >>> scheme = abjad.Scheme('format-mark-box-alphabet')
        >>> abjad.setting(score).markFormatter = scheme
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score \with {
                markFormatter = #format-mark-box-alphabet
            } <<
                \new Staff {
                    \mark #1
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

    ..  container:: example

        Rehearsal B:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> mark = abjad.RehearsalMark(number=2)
        >>> abjad.attach(mark, staff[0])
        >>> scheme = abjad.Scheme('format-mark-box-alphabet')
        >>> abjad.setting(score).markFormatter = scheme
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score \with {
                markFormatter = #format-mark-box-alphabet
            } <<
                \new Staff {
                    \mark #2
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_markup',
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, number=None, markup=None):
        import abjad
        self._context = 'Score'
        if markup is not None:
            assert isinstance(markup, abjad.Markup)
        self._markup = markup
        if number is not None:
            assert abjad.mathtools.is_positive_integer(number)
        self._number = number

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of rehearsal mark.

        ..  container:: example

            Rehearsal A

            >>> mark = abjad.RehearsalMark(number=1)
            >>> print(str(mark))
            \mark #1

        ..  container:: example

            Rehearsal B

            >>> mark = abjad.RehearsalMark(number=2)
            >>> print(str(mark))
            \mark #2

        Returns string.
        '''
        return self._get_lilypond_format()

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        if self.markup is not None:
            result = r'\mark {}'.format(self.markup)
        elif self.number is not None:
            result = r'\mark #{}'.format(self.number)
        else:
            result = r'\mark \default'
        return result

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of rehearsal mark.

        ..  container:: example

            Rehearsal A:

            >>> mark = abjad.RehearsalMark(number=1)
            >>> mark.context
            'Score'

        ..  container:: example

            Rehearsal B:

            >>> mark = abjad.RehearsalMark(number=2)
            >>> mark.context
            'Score'

        Returns context or string.
        '''
        return self._context

    @property
    def markup(self):
        r'''Gets markup of rehearsal mark.

        ..  container:: example

            Custom rehearsal A:

            >>> markup = abjad.Markup(r'\bold { \italic { A } }')
            >>> mark = abjad.RehearsalMark(markup=markup)
            >>> abjad.show(mark.markup) # doctest: +SKIP

            ..  docs::

                >>> print(str(mark.markup))
                \markup {
                    \bold
                        {
                            \italic
                                {
                                    A
                                }
                        }
                    }

        ..  container:: example

            Custom rehearsal B:

            >>> markup = abjad.Markup(r'\bold { \italic { B } }')
            >>> mark = abjad.RehearsalMark(markup=markup)
            >>> abjad.show(mark.markup) # doctest: +SKIP

            ..  docs::

                >>> print(str(mark.markup))
                \markup {
                    \bold
                        {
                            \italic
                                {
                                    B
                                }
                        }
                    }

        Returns markup or none.
        '''
        return self._markup

    @property
    def number(self):
        r'''Gets number of rehearsal mark.

        ..  container:: example

            Rehearsal A:

            >>> mark = abjad.RehearsalMark(number=1)
            >>> mark.number
            1

        ..  container:: example

            Rehearsal B:

            >>> mark = abjad.RehearsalMark(number=2)
            >>> mark.number
            2

        Returns positive integer or none.
        '''
        return self._number
