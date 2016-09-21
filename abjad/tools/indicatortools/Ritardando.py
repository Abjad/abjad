# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools.new import new


class Ritardando(AbjadValueObject):
    r'''A ritardando.

    ..  container:: example

        **Example 1.** Default ritardando:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> score = Score([staff])
            >>> ritardando = indicatortools.Ritardando()
            >>> attach(ritardando, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
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

        **Example 2.** Custom ritardando:

        ::

            >>> markup = Markup(r'\bold { \italic { ritardando } }')
            >>> ritardando = indicatortools.Ritardando(markup=markup)
            >>> staff = Staff("c'4 d' e' f'")
            >>> score = Score([staff])
            >>> attach(ritardando, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
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

    Use ritardandi with a tempo spanner to generate dashed lines and other
    spanners.
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
        # TODO: make default scope work
        #self._default_scope = scoretools.Score
        self._default_scope = None
        if markup is not None:
            assert isinstance(markup, markuptools.Markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of ritardando.

        ..  container:: example

            **Example 1.** Default ritardando:

            ::

                >>> print(str(indicatortools.Ritardando()))
                \markup {
                    \large
                        \upright
                            rit.
                    }

        ..  container:: example

            **Example 2.** Custom ritardando:

            ::

                >>> markup = Markup(r'\bold { \italic { ritardando } }')
                >>> ritardando = indicatortools.Ritardando(markup=markup)
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

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        markup = self._to_markup()
        markup = new(markup, direction=Up)
        markup_format_pieces = markup._get_format_pieces()
        lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle

    def _to_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _default_markup(self):
        from abjad.tools import markuptools
        contents = r'\large \upright rit.'
        return markuptools.Markup(contents=contents)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of ritardando.

        ..  container:: example

            **Example 1.** Default ritardando:

            ::

                >>> ritardando = indicatortools.Ritardando()
                >>> ritardando.default_scope is None
                True

        ..  container:: example

            **Example 2.** Custom ritardando:

            ::

                >>> markup = Markup(r'\bold { \italic { ritardando } }')
                >>> ritardando = indicatortools.Ritardando(markup=markup)
                >>> ritardando.default_scope is None
                True

        ..  todo:: Make ritardandi score-scoped.

        Returns none (but should return score).
        '''
        return self._default_scope

    @property
    def markup(self):
        r'''Gets markup of ritardando.

        ..  container:: example

            **Example 1.** Default ritardando:

            ::

                >>> ritardando = indicatortools.Ritardando()
                >>> ritardando.markup is None
                True

        ..  container:: example

            **Example 2.** Custom ritardando:

            ::

                >>> markup = Markup(r'\bold { \italic { ritardando } }')
                >>> ritardando = indicatortools.Ritardando(markup=markup)
                >>> show(ritardando.markup) # doctest: +SKIP

            ..  doctest::

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
