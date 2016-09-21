# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools.new import new


class Accelerando(AbjadValueObject):
    r'''An accelerando.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> score = Score([staff])
            >>> accelerando = indicatortools.Accelerando()
            >>> attach(accelerando, staff[0])

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    c'4
                        ^ \markup {
                            \large
                                \upright
                                    accel.
                            }
                    d'4
                    e'4
                    f'4
                }
            >>

    Accelerandi format as LilyPond markup.

    Accelerandi are not followed by any type of dashed line or other spanner.

    Use accelerandi with a tempo spanner to generate dashed lines and other
    spanners.

    ..  todo:: add example tempo spanner example.
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
        r'''Gets string representation of accelerando.

        ..  container:: example

            String representation of accelerando with default markup:

            ::

                >>> print(str(indicatortools.Accelerando()))
                \markup {
                    \large
                        \upright
                            accel.
                    }

        ..  container:: example

            String representation of accelerando with custom markup:

            ::

                >>> markup = Markup(r'\bold { \italic { accelerando } }')
                >>> accelerando = indicatortools.Accelerando(markup=markup)
                >>> print(str(accelerando))
                \markup {
                    \bold
                        {
                            \italic
                                {
                                    accelerando
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
        contents = r'\large \upright accel.'
        return markuptools.Markup(contents=contents)

    @property
    def _lilypond_format(self):
        return str(self)
        
    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of accelerando.

        ..  container:: example

            ::

                >>> accelerando = Accelerando()
                >>> accelerando.default_scope is None
                True

        .. todo:: Default scope should return score.

        Returns none (but should return score).
        '''
        return self._default_scope

    @property
    def markup(self):
        r'''Gets markup of accelerando.

        ..  container:: example

            ::

                >>> markup = Markup(r'\bold { \italic { accel. } }')
                >>> accelerando = indicatortools.Accelerando(markup=markup)
                >>> print(str(accelerando.markup))
                \markup {
                    \bold
                        {
                            \italic
                                {
                                    accel.
                                }
                        }
                    }

        Returns markup or none.
        '''
        return self._markup
