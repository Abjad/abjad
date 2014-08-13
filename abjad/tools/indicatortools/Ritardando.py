# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Ritardando(AbjadObject):
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
                    c'4 ^ \markup {
                        \large
                            {
                                \italic
                                    {
                                        rit.
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

    ..  todo:: add example tempo spanner examle.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_annotation_only',
        '_default_scope',
        '_markup',
        )

    ### INITIALIZER ###

    def __init__(self, markup=None):
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        self._annotation_only = None
        # TODO: make default scope work
        #self._default_scope = scoretools.Score
        if markup is not None:
            assert isinstance(markup, markuptools.Markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies ritardando.

        ..  container:: example

            ::

                >>> import copy
                >>> markup = Markup(r'\bold { \italic { ritardando } }')
                >>> ritardando_1 = indicatortools.Ritardando(markup=markup)
                >>> ritardando_2 = copy.copy(ritardando_1)

            ::

                >>> str(ritardando_1) == str(ritardando_2)
                True

            ::

                >>> ritardando_1 == ritardando_2
                True

            ::

                >>> ritardando_1 is ritardando_2
                False

        Returns new ritardando.

        '''
        return type(self)(markup=self.markup)

    def __eq__(self, expr):
        r'''Is true when `expr` is another ritardando. Otherwise false.

        ..  container:: example

            ::

                >>> ritardando_1 = indicatortools.Ritardando(
                ...     markup=Markup('rit.')
                ...     )
                >>> ritardando_2 = indicatortools.Ritardando(
                ...     markup=Markup('ritardando')
                ...     )

            ::

                >>> ritardando_1 == ritardando_1
                True
                >>> ritardando_1 == ritardando_2
                True

            ::

                >>> ritardando_2 == ritardando_1
                True
                >>> ritardando_2 == ritardando_2
                True

        Ignores markup of ritardando.
                
        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return True
        return False

    def __hash__(self):
        r'''Hashes ritardando.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Ritardando, self).__hash__()

    def __str__(self):
        r'''Gets string representation of ritardando.

        ..  container:: example

            String representation of ritardando with default markup:

            ::

                >>> print(str(indicatortools.Ritardando()))
                ^ \markup {
                    \large
                        {
                            \italic
                                {
                                    rit.
                                }
                        }
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
        markup = self.markup or self._default_markup
        return str(markup)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
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
        contents = r'\large { \italic { rit. } }'
        return markuptools.Markup(contents=contents, direction=Up)

    @property
    def _lilypond_format(self):
        return str(self)

    @property
    def _lilypond_format_bundle(self):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        if not self._annotation_only:
            markup = self.markup or self._default_markup
            markup_format_pieces = markup._get_format_pieces()
            lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle
        
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