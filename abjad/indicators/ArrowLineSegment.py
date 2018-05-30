import typing
from abjad.enumerations import Center, VerticalAlignment
from abjad.markup.Markup import Markup
from .LineSegment import LineSegment
Number = typing.Union[int, float]


class ArrowLineSegment(LineSegment):
    r"""
    Arrow line segment.

    ..  container:: example

        String contact position spanner:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])

        >>> abjad.f(abjad.ArrowLineSegment())
        abjad.ArrowLineSegment(
            arrow_width=0.25,
            dash_fraction=1,
            left_hspace=0.25,
            left_stencil_align_direction_y=Center,
            right_arrow=True,
            right_broken_padding=0,
            right_broken_text=False,
            right_padding=0.5,
            right_stencil_align_direction_y=Center,
            )

        >>> spanner.attach(abjad.Markup('pont.'), staff[0])
        >>> spanner.attach(abjad.Markup('ord.'), staff[-1])
        >>> spanner.attach(abjad.ArrowLineSegment(), staff[0])

        >>> abjad.override(staff).text_script.staff_padding = 1.25
        >>> abjad.override(staff).text_spanner.staff_padding = 2
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextScript.staff-padding = #1.25
                \override TextSpanner.staff-padding = #2
            }
            {
                c'4
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            pont.
                            \hspace
                                #0.25
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 0.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                - \tweak bound-details.right.text \markup {
                    \concat
                        {
                            \hspace
                                #0.0
                            ord.
                        }
                    }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    Arrow line segment is a preconfigured line segment.

    Follow the piecewise definition protocol shown here.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        arrow_width: Number = 0.25,
        dash_fraction: Number = 1,
        dash_period: Number = None,
        left_broken_padding: Number = None,
        left_broken_text: typing.Union[bool, str, Markup] = None,
        left_hspace: Number = 0.25,
        left_padding: Number = None,
        left_stencil_align_direction_y: typing.Union[
            Number, VerticalAlignment, None] = VerticalAlignment.Center,
        right_arrow: bool = True,
        right_broken_arrow: bool = None,
        right_broken_padding: Number = 0,
        right_broken_text: typing.Union[bool, str, Markup] = False,
        right_padding: Number = 0.5,
        right_stencil_align_direction_y: typing.Union[
            Number, VerticalAlignment, None] = VerticalAlignment.Center,
        style: str = None,
        ) -> None:
        super(ArrowLineSegment, self).__init__(
            arrow_width=arrow_width,
            dash_fraction=dash_fraction,
            dash_period=dash_period,
            left_broken_padding=left_broken_padding,
            left_broken_text=left_broken_text,
            left_hspace=left_hspace,
            left_padding=left_padding,
            left_stencil_align_direction_y=left_stencil_align_direction_y,
            right_arrow=right_arrow,
            right_broken_arrow=right_broken_arrow,
            right_broken_padding=right_broken_padding,
            right_broken_text=right_broken_text,
            right_padding=right_padding,
            right_stencil_align_direction_y=right_stencil_align_direction_y,
            style=style,
            )

    ### PRIVATE METHODS ###

    """No _get_lilypond_format(), _get_lilypond_format_bundle()
    because class is used only by piecewise spanner.
    """

    ### PUBLIC PROPERTIES ###

    @property
    def arrow_width(self) -> typing.Optional[Number]:
        r"""
        Gets arrow width of arrow.

        ..  container:: example

            Arrow line segment width equals ``0.25``:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(arrow_width=0.25)

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            Results in thin arrow head.

            This is default behavior.

        ..  container:: example

            Arrow line segment width equals ``0.5``:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(arrow_width=0.5)

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.5
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            Results in wide arrow head.

        ..  container:: example

            Arrow line segment width equals ``1``:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(arrow_width=1)

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 1
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            Results in very wide arrow head.

        Defaults to ``0.25``.
        """
        return super(ArrowLineSegment, self).arrow_width

    @property
    def dash_fraction(self) -> typing.Optional[Number]:
        r"""
        Gets dash fraction of arrow.

        ..  container:: example

            Dash fraction equals 100% of dash period:


            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(dash_fraction=1)

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            This is default behavior.

        ..  container:: example

            Dash fraction equals 50% of dash period:


            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(dash_fraction=0.5)

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 0.5
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            Dash fraction equals 10% of dash period:


            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(dash_fraction=0.1)

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 0.1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        Defaults to ``1``.
        """
        return super(ArrowLineSegment, self).dash_fraction

    @property
    def dash_period(self) -> typing.Optional[Number]:
        r"""
        Gets dash period of arrow.

        ..  container:: example

            Dash period equals none:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(
            ...     dash_period=None,
            ...     )

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            Results in a solid line.

            This is default behavior.

        ..  container:: example

            Dash period equals ``1`` (with dash fraction equal to 25%):

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(
            ...     dash_fraction=0.25,
            ...     dash_period=1,
            ...     )

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 0.25
                    - \tweak dash-period 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            Results in fine dashes.

        ..  container:: example

            Dash period equals ``4`` (with dash fraction equal to 25%):

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(
            ...     dash_fraction=0.25,
            ...     dash_period=4,
            ...     )

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 0.25
                    - \tweak dash-period 4
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            Results in coarse dashes.

        Defaults to none.
        """
        return super(ArrowLineSegment, self).dash_period

    @property
    def left_broken_text(self) -> typing.Union[bool, str, Markup, None]:
        r"""
        Gets left broken text of arrow.

        ..  container:: example

            Left broken text set to false:

            ..  container:: example

                >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
                >>> score = abjad.Score([staff])
                >>> command = abjad.LilyPondLiteral(r'\break', 'after')
                >>> abjad.attach(command, staff[3])

                >>> spanner = abjad.TextSpanner()
                >>> abjad.attach(spanner, staff[2:])
                >>> start_markup = abjad.Markup('pont.').upright()
                >>> stop_markup = abjad.Markup('ord.').upright()
                >>> arrow = abjad.ArrowLineSegment()

                >>> abjad.f(arrow)
                abjad.ArrowLineSegment(
                    arrow_width=0.25,
                    dash_fraction=1,
                    left_hspace=0.25,
                    left_stencil_align_direction_y=Center,
                    right_arrow=True,
                    right_broken_padding=0,
                    right_broken_text=False,
                    right_padding=0.5,
                    right_stencil_align_direction_y=Center,
                    )

                >>> spanner.attach(start_markup, staff[2])
                >>> spanner.attach(stop_markup, staff[6])
                >>> spanner.attach(arrow, staff[2])

                >>> abjad.override(staff).text_script.staff_padding = 1.25
                >>> abjad.override(staff).text_spanner.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #1.25
                        \override TextSpanner.staff-padding = #2
                    }
                    {
                        \time 3/8
                        c'4.
                        d'4.
                        e'4.
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        pont.
                                    \hspace
                                        #0.25
                                }
                            }
                        - \tweak arrow-width 0.25
                        - \tweak dash-fraction 1
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right.arrow ##t
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4.
                        \stopTextSpan
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        ord.
                                    \hspace
                                        #0.25
                                }
                            }
                        - \tweak dash-period 0
                        - \tweak bound-details.left-broken.text ##f
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        c''4.
                        \stopTextSpan
                    }

            Results in no text immediately after line break.
            (This is default behavior.)

        ..  container:: example

            Left broken text set explicitly:

            ..  container:: example

                >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
                >>> score = abjad.Score([staff])
                >>> command = abjad.LilyPondLiteral(r'\break', 'after')
                >>> abjad.attach(command, staff[3])

                >>> spanner = abjad.TextSpanner()
                >>> abjad.attach(spanner, staff[2:])
                >>> start_markup = abjad.Markup('pont.').upright()
                >>> stop_markup = abjad.Markup('ord.').upright()
                >>> left_broken_markup = abjad.Markup('(pont./ord.)').upright()
                >>> arrow = abjad.ArrowLineSegment(
                ...     left_broken_text=left_broken_markup,
                ... )

                >>> abjad.f(arrow)
                abjad.ArrowLineSegment(
                    arrow_width=0.25,
                    dash_fraction=1,
                    left_broken_text=abjad.Markup(
                        contents=[
                            abjad.MarkupCommand(
                                'upright',
                                '(pont./ord.)'
                                ),
                            ],
                        ),
                    left_hspace=0.25,
                    left_stencil_align_direction_y=Center,
                    right_arrow=True,
                    right_broken_padding=0,
                    right_broken_text=False,
                    right_padding=0.5,
                    right_stencil_align_direction_y=Center,
                    )

                >>> spanner.attach(start_markup, staff[2])
                >>> spanner.attach(stop_markup, staff[6])
                >>> spanner.attach(arrow, staff[2])

                >>> abjad.override(staff).text_script.staff_padding = 1.25
                >>> abjad.override(staff).text_spanner.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #1.25
                        \override TextSpanner.staff-padding = #2
                    }
                    {
                        \time 3/8
                        c'4.
                        d'4.
                        e'4.
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        pont.
                                    \hspace
                                        #0.25
                                }
                            }
                        - \tweak arrow-width 0.25
                        - \tweak dash-fraction 1
                        - \tweak bound-details.left-broken.text \markup {
                            \upright
                                (pont./ord.)
                            }
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right.arrow ##t
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4.
                        \stopTextSpan
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        ord.
                                    \hspace
                                        #0.25
                                }
                            }
                        - \tweak dash-period 0
                        - \tweak bound-details.left-broken.text ##f
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        c''4.
                        \stopTextSpan
                    }

        """
        return self._left_broken_text

    @property
    def right_broken_arrow(self) -> typing.Optional[bool]:
        r"""
        Is true when arrow should appear immediately before line break.

        ..  container:: example

            Right broken arrow set to none:

            ..  container:: example

                >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
                >>> score = abjad.Score([staff])
                >>> command = abjad.LilyPondLiteral(r'\break', 'after')
                >>> abjad.attach(command, staff[3])

                >>> spanner = abjad.TextSpanner()
                >>> abjad.attach(spanner, staff[2:])
                >>> start_markup = abjad.Markup('pont.').upright()
                >>> stop_markup = abjad.Markup('ord.').upright()
                >>> arrow = abjad.ArrowLineSegment()

                >>> abjad.f(arrow)
                abjad.ArrowLineSegment(
                    arrow_width=0.25,
                    dash_fraction=1,
                    left_hspace=0.25,
                    left_stencil_align_direction_y=Center,
                    right_arrow=True,
                    right_broken_padding=0,
                    right_broken_text=False,
                    right_padding=0.5,
                    right_stencil_align_direction_y=Center,
                    )

                >>> spanner.attach(start_markup, staff[2])
                >>> spanner.attach(stop_markup, staff[6])
                >>> spanner.attach(arrow, staff[2])

                >>> abjad.override(staff).text_script.staff_padding = 1.25
                >>> abjad.override(staff).text_spanner.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #1.25
                        \override TextSpanner.staff-padding = #2
                    }
                    {
                        \time 3/8
                        c'4.
                        d'4.
                        e'4.
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        pont.
                                    \hspace
                                        #0.25
                                }
                            }
                        - \tweak arrow-width 0.25
                        - \tweak dash-fraction 1
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right.arrow ##t
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4.
                        \stopTextSpan
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        ord.
                                    \hspace
                                        #0.25
                                }
                            }
                        - \tweak dash-period 0
                        - \tweak bound-details.left-broken.text ##f
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        c''4.
                        \stopTextSpan
                    }

            Results in arrow immediately before line break.
            (This is default behavior.)

        ..  container:: example

            Right broken arrow set to false:

            ..  container:: example

                >>> staff = abjad.Staff("c'4. d' e' f' g' a' b' c''")
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
                >>> score = abjad.Score([staff])
                >>> command = abjad.LilyPondLiteral(r'\break', 'after')
                >>> abjad.attach(command, staff[3])

                >>> spanner = abjad.TextSpanner()
                >>> abjad.attach(spanner, staff[2:])
                >>> start_markup = abjad.Markup('pont.').upright()
                >>> stop_markup = abjad.Markup('ord.').upright()
                >>> arrow = abjad.ArrowLineSegment(
                ...     right_broken_arrow=False,
                ... )

                >>> abjad.f(arrow)
                abjad.ArrowLineSegment(
                    arrow_width=0.25,
                    dash_fraction=1,
                    left_hspace=0.25,
                    left_stencil_align_direction_y=Center,
                    right_arrow=True,
                    right_broken_arrow=False,
                    right_broken_padding=0,
                    right_broken_text=False,
                    right_padding=0.5,
                    right_stencil_align_direction_y=Center,
                    )

                >>> spanner.attach(start_markup, staff[2])
                >>> spanner.attach(stop_markup, staff[6])
                >>> spanner.attach(arrow, staff[2])

                >>> abjad.override(staff).text_script.staff_padding = 1.25
                >>> abjad.override(staff).text_spanner.staff_padding = 2
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #1.25
                        \override TextSpanner.staff-padding = #2
                    }
                    {
                        \time 3/8
                        c'4.
                        d'4.
                        e'4.
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        pont.
                                    \hspace
                                        #0.25
                                }
                            }
                        - \tweak arrow-width 0.25
                        - \tweak dash-fraction 1
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right.arrow ##t
                        - \tweak bound-details.right-broken.arrow ##f
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4.
                        \stopTextSpan
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        ord.
                                    \hspace
                                        #0.25
                                }
                            }
                        - \tweak dash-period 0
                        - \tweak bound-details.left-broken.text ##f
                        - \tweak bound-details.left.stencil-align-dir-y #center
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        c''4.
                        \stopTextSpan
                    }

        """
        return self._right_broken_arrow

    @property
    def style(self) -> typing.Optional[str]:
        r"""
        Gets style of arrow.

        ..  container:: example

            Style equals none:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(style=None)

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            LilyPond defaults to solid line.

            This is default behavior.

        ..  container:: example

            Style equals zig-zag:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(style='zigzag')

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak style #'zigzag
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            Style equals trill:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(style='trill')

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak style #'trill
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            Style equals dotted line:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> start_markup = abjad.Markup('pont.').upright()
            >>> stop_markup = abjad.Markup('ord.').upright()
            >>> arrow = abjad.ArrowLineSegment(style='dotted-line')

            >>> spanner.attach(start_markup, staff[0])
            >>> spanner.attach(stop_markup, staff[-1])
            >>> spanner.attach(arrow, staff[0])

            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak style #'dotted-line
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        """
        return super(ArrowLineSegment, self).style

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on arrow line segment.
        """
        pass
