# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools.new import new


class Accelerando(AbjadObject):
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
                    c'4 ^ \markup {
                        \large
                            {
                                \italic
                                    {
                                        accel.
                                    }
                            }
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

    ..  todo:: add example tempo spanner examle.
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

    def __copy__(self, *args):
        r'''Copies accelerando.

        ..  container:: example

            ::

                >>> import copy
                >>> markup = Markup(r'\bold { \italic { accelerando } }')
                >>> accelerando_1 = indicatortools.Accelerando(markup=markup)
                >>> accelerando_2 = copy.copy(accelerando_1)

            ::

                >>> str(accelerando_1) == str(accelerando_2)
                True

            ::

                >>> accelerando_1 == accelerando_2
                True

            ::

                >>> accelerando_1 is accelerando_2
                False

        Returns new accelerando.

        '''
        return type(self)(markup=self.markup)

    def __eq__(self, expr):
        r'''Is true when `expr` is another accelerando. Otherwise false.

        ..  container:: example

            ::

                >>> accelerando_1 = indicatortools.Accelerando(
                ...     markup=Markup('accel.')
                ...     )
                >>> accelerando_2 = indicatortools.Accelerando(
                ...     markup=Markup('accelerando')
                ...     )

            ::

                >>> accelerando_1 == accelerando_1
                True
                >>> accelerando_1 == accelerando_2
                True

            ::

                >>> accelerando_2 == accelerando_1
                True
                >>> accelerando_2 == accelerando_2
                True

        Ignores markup of accelerando.
                
        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return True
        return False

    def __hash__(self):
        r'''Hashes accelerando.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Accelerando, self).__hash__()

    def __str__(self):
        r'''Gets string representation of accelerando.

        ..  container:: example

            String representation of accelerando with default markup:

            ::

                >>> print(str(indicatortools.Accelerando()))
                \markup {
                    \large
                        {
                            \italic
                                {
                                    accel.
                                }
                        }
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
        contents = r'\large { \italic { accel. } }'
        return markuptools.Markup(contents=contents)

    @property
    def _lilypond_format(self):
        return str(self)

    @property
    def _lilypond_format_bundle(self):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        markup = self._to_markup()
        markup = new(markup, direction=Up)
        markup_format_pieces = markup._get_format_pieces()
        lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle

    ### PRIVATE METHODS ###

    def _to_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup
        
    ### PUBLIC PROPERTIES ###

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