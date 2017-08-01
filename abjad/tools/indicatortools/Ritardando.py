# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools.new import new


class Ritardando(AbjadValueObject):
    r'''Ritardando.

    ::

        >>> import abjad

    ..  container:: example

        Default ritardando:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> score = abjad.Score([staff])
            >>> ritardando = abjad.Ritardando()
            >>> abjad.attach(ritardando, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  docs::

            >>> f(score)
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

        ::

            >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
            >>> ritardando = abjad.Ritardando(markup=markup)
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> score = abjad.Score([staff])
            >>> abjad.attach(ritardando, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  docs::

            >>> f(score)
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
        '_default_scope',
        '_markup',
        )

    ### INITIALIZER ###

    def __init__(self, markup=None):
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        self._default_scope = scoretools.Score
        if markup is not None:
            assert isinstance(markup, markuptools.Markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of ritardando.

        ..  container:: example

            Default ritardando:

            ::

                >>> print(str(abjad.Ritardando()))
                \markup {
                    \large
                        \upright
                            rit.
                    }

        ..  container:: example

            Custom ritardando:

            ::

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
        markup = abjad.new(markup, direction=Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.right.markup.extend(markup_format_pieces)
        return bundle

    def _to_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of ritardando.

        ..  container:: example

            Default ritardando:

            ::

                >>> ritardando = abjad.Ritardando()
                >>> ritardando.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        ..  container:: example

            Custom ritardando:

            ::

                >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
                >>> ritardando = abjad.Ritardando(markup=markup)
                >>> ritardando.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        Returns score.
        '''
        return self._default_scope

    @property
    def markup(self):
        r'''Gets markup of ritardando.

        ..  container:: example

            Default ritardando:

            ::

                >>> ritardando = abjad.Ritardando()
                >>> ritardando.markup is None
                True

        ..  container:: example

            Custom ritardando:

            ::

                >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
                >>> ritardando = abjad.Ritardando(markup=markup)
                >>> show(ritardando.markup) # doctest: +SKIP

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
