from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Ritardando(AbjadValueObject):
    r'''Ritardando.

    ..  container:: example

        Default ritardando:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> ritardando = abjad.Ritardando()
        >>> abjad.attach(ritardando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score <<
                \new Staff {
                    c'4
                        ^ \markup {
                            \large
                                \upright
                                    rit.
                            }
                    d'4
                    e'4
                    f'4
                }
            >>

    ..  container:: example

        Custom ritardando:

        >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
        >>> ritardando = abjad.Ritardando(markup=markup)
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(ritardando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score <<
                \new Staff {
                    c'4
                        ^ \markup {
                            \bold
                                {
                                    \italic
                                        {
                                            ritardando
                                        }
                                }
                            }
                    d'4
                    e'4
                    f'4
                }
            >>

    Ritardandi format as LilyPond markup.

    Ritardandi are not followed by any type of dashed line or other spanner.

    Use ritardandi with a metronome mark spanner to generate dashed lines and
    other spanners.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_markup',
        )

    ### INITIALIZER ###

    def __init__(self, markup=None):
        import abjad
        self._context = 'Score'
        if markup is not None:
            assert isinstance(markup, abjad.Markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of ritardando.

        ..  container:: example

            Default ritardando:

            >>> print(str(abjad.Ritardando()))
            \markup {
                \large
                    \upright
                        rit.
                }

        ..  container:: example

            Custom ritardando:

            >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
            >>> ritardando = abjad.Ritardando(markup=markup)
            >>> print(str(ritardando))
            \markup {
                \bold
                    {
                        \italic
                            {
                                ritardando
                            }
                    }
                }

        Returns string.
        '''
        return str(self._to_markup())

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _default_markup(self):
        from abjad.tools import markuptools
        contents = r'\large \upright rit.'
        return markuptools.Markup(contents=contents)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        markup = self._to_markup()
        markup = abjad.new(markup, direction=abjad.Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.right.markup.extend(markup_format_pieces)
        return bundle

    def _to_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of ritardando.

        ..  container:: example

            Default ritardando:

            >>> ritardando = abjad.Ritardando()
            >>> ritardando.context
            'Score'

        ..  container:: example

            Custom ritardando:

            >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
            >>> ritardando = abjad.Ritardando(markup=markup)
            >>> ritardando.context
            'Score'

        Returns context or string.
        '''
        return self._context

    @property
    def markup(self):
        r'''Gets markup of ritardando.

        ..  container:: example

            Default ritardando:

            >>> ritardando = abjad.Ritardando()
            >>> ritardando.markup is None
            True

        ..  container:: example

            Custom ritardando:

            >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
            >>> ritardando = abjad.Ritardando(markup=markup)
            >>> abjad.show(ritardando.markup) # doctest: +SKIP

            ..  docs::

                >>> print(ritardando.markup)
                \markup {
                    \bold
                        {
                            \italic
                                {
                                    ritardando
                                }
                        }
                    }

        Set to markup or none.

        Defaults to ``'rit.'``.

        Returns markup or none.
        '''
        return self._markup
