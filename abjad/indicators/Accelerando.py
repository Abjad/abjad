import typing
from abjad.abctools.AbjadValueObject import AbjadValueObject
from abjad.enumerations import Up
from abjad.markup.Markup import Markup
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.top.new import new


class Accelerando(AbjadValueObject):
    r"""
    Accelerando.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> accelerando = abjad.Accelerando()
        >>> abjad.attach(accelerando, staff[0])
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
                                accel.
                        }
                    d'4
                    e'4
                    f'4
                }
            >>

    Accelerandi format as LilyPond markup.

    Accelerandi are not followed by any type of dashed line or other spanner.

    Use accelerandi with a metronome mark spanner to generate dashed lines and
    other spanners. See ``abjad.MetronomeMarkMarkSpanner`` for examples.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_markup',
        )

    _context = 'Score'

    _persistent = 'abjad.MetronomeMark'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        markup: Markup = None,
        ) -> None:
        if markup is not None:
            assert isinstance(markup, Markup), repr(markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""
        Gets string representation of accelerando.

        ..  container:: example

            String representation of accelerando with default markup:

            >>> print(str(abjad.Accelerando()))
            \markup {
                \large
                    \upright
                        accel.
                }

        ..  container:: example

            String representation of accelerando with custom markup:

            >>> markup = abjad.Markup(r'\bold { \italic { accelerando } }')
            >>> accelerando = abjad.Accelerando(markup=markup)
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

        """
        return str(self._get_markup())

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _default_markup(self):
        contents = r'\large \upright accel.'
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
    def context(self) -> str:
        """
        Gets (historically conventional) context.

        ..  container:: example

            >>> abjad.Accelerando().context
            'Score'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def markup(self) -> typing.Optional[Markup]:
        r"""
        Gets markup of accelerando.

        ..  container:: example

            >>> markup = abjad.Markup(r'\bold { \italic { accel. } }')
            >>> accelerando = abjad.Accelerando(markup=markup)
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

        """
        return self._markup

    @property
    def persistent(self) -> str:
        """
        Is ``'abjad.MetronomeMark'``.

        ..  container:: example

            >>> abjad.Accelerando().persistent
            'abjad.MetronomeMark'

        """
        return self._persistent

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on accelerando.

        ..  container:: example

            Use accelerando as a piecewise part of metronome mark spanner:

            >>> staff = abjad.Staff("c'8. d' e'4. g'8. f' ef'4.")
            >>> score = abjad.Score([staff])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> spanner = abjad.MetronomeMarkSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff).text_spanner.staff_padding = 3

            >>> string = r'\large \upright accel.'
            >>> markup = abjad.Markup(string).with_color('blue')
            >>> accelerando = abjad.Accelerando(markup=markup)
            >>> spanner.attach(accelerando, spanner[0])

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> spanner.attach(mark, spanner[2])
            >>> mark = abjad.MetronomeMark((1, 4), 72)
            >>> spanner.attach(mark, spanner[3])
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> spanner.attach(mark, spanner[5])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextSpanner.staff-padding = #3
                    }
                    {
                        \time 3/8
                        c'8.
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \with-color
                                #blue
                                \large
                                    \upright
                                        accel.
                            \hspace
                                #1
                            }
                        - \tweak arrow-width 0.25
                        - \tweak dash-fraction 0.25
                        - \tweak dash-period 1.5
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right.arrow ##t
                        - \tweak bound-details.right-broken.arrow ##f
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        - \tweak bound-details.left-broken.text ##f
                        \startTextSpan
                        d'8.
                        e'4.
                        \stopTextSpan
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    90
                                }
                            \hspace
                                #1
                            }
                        - \tweak dash-period 0
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        - \tweak bound-details.left-broken.text ##f
                        \startTextSpan
                        g'8.
                        \stopTextSpan
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \fontsize
                                #-6
                                \general-align
                                    #Y
                                    #DOWN
                                    \note-by-number
                                        #2
                                        #0
                                        #1
                            \upright
                                {
                                    =
                                    72
                                }
                            \hspace
                                #1
                            }
                        - \tweak dash-period 0
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        - \tweak bound-details.right.text \markup {
                            \concat
                                {
                                    \hspace
                                        #0.5
                                    \line
                                        {
                                            \fontsize
                                                #-6
                                                \general-align
                                                    #Y
                                                    #DOWN
                                                    \note-by-number
                                                        #2
                                                        #0
                                                        #1
                                            \upright
                                                {
                                                    =
                                                    60
                                                }
                                        }
                                }
                            }
                        - \tweak bound-details.left-broken.text ##f
                        \startTextSpan
                        f'8.
                        ef'4.
                        \stopTextSpan
                    }
                >>

            See the metronome mark spanner API entry for further examples.

        """
        pass
