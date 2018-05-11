import typing
from abjad import Up
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.markuptools.Markup import Markup
from abjad.tools.systemtools.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.tools.topleveltools.new import new


class Ritardando(AbjadValueObject):
    r'''
    Ritardando.

    ..  container:: example

        Default ritardando:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> ritardando = abjad.Ritardando()
        >>> abjad.attach(ritardando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
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
            \new Score
            <<
                \new Staff
                {
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
        '_markup',
        )

    _context = 'Score'

    _persistent = 'abjad.MetronomeMark'

    ### INITIALIZER ###

    def __init__(self, markup: Markup = None) -> None:
        if markup is not None:
            assert isinstance(markup, Markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r'''
        Gets string representation of ritardando.

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

        '''
        return str(self._get_markup())

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _default_markup(self):
        contents = r'\large \upright rit.'
        return Markup(contents=contents)

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        markup = self._get_markup()
        markup = new(markup, direction=Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.right.markup.extend(markup_format_pieces)
        return bundle

    def _get_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup()

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''
        Gets (historically conventional) context.

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

        Override with ``abjad.attach(..., context='...')``.
        '''
        return self._context

    @property
    def markup(self) -> typing.Optional[Markup]:
        r'''
        Gets markup of ritardando.

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

        '''
        return self._markup

    @property
    def persistent(self) -> str:
        '''
        Is ``'abjad.MetronomeMark'``.

        ..  container:: example

            >>> abjad.Ritardando().persistent
            'abjad.MetronomeMark'

        '''
        return self._persistent
