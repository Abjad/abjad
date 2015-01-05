# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools.new import new


class Ritardando(AbjadValueObject):
    r'''A ritardando.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> score = Score([staff])
            >>> ritardando = indicatortools.Ritardando()
            >>> attach(ritardando, staff[0])

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
                                    rit.
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
        if markup is not None:
            assert isinstance(markup, markuptools.Markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of ritardando.

        ..  container:: example

            String representation of ritardando with default markup:

            ::

                >>> print(str(indicatortools.Ritardando()))
                \markup {
                    \large
                        \upright
                            rit.
                    }

        ..  container:: example

            String representation of ritardando with custom markup:

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

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='markup',
                command='m',
                editor=idetools.getters.get_markup,
                ),
            )

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

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self):
        r'''Gets markup of ritardando.

        ..  container:: example

            ::

                >>> markup = Markup(r'\bold { \italic { ritardando } }')
                >>> ritardando = indicatortools.Ritardando(markup=markup)
                >>> print(str(ritardando.markup))
                \markup {
                    \bold
                        {
                            \italic
                                {
                                    ritardando
                                }
                        }
                    }

        Returns markup or none.
        '''
        return self._markup