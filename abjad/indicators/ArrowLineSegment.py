import typing
from abjad import enums
from abjad import typings
from abjad.markups import Markup
from .LineSegment import LineSegment


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
        arrow_width: typings.Number = 0.25,
        dash_fraction: typings.Number = 1,
        dash_period: typings.Number = None,
        left_broken_padding: typings.Number = None,
        left_broken_text: typing.Union[bool, str, Markup] = None,
        left_hspace: typings.Number = 0.25,
        left_padding: typings.Number = None,
        left_stencil_align_direction_y: typing.Union[
            typings.Number, enums.VerticalAlignment, None
            ] = enums.Center,
        right_arrow: bool = True,
        right_broken_arrow: bool = None,
        right_broken_padding: typings.Number = 0,
        right_broken_text: typing.Union[bool, str, Markup] = False,
        right_padding: typings.Number = 0.5,
        right_stencil_align_direction_y: typing.Union[
            typings.Number, enums.VerticalAlignment, None
            ] = enums.Center,
        style: str = None,
        ) -> None:
        super().__init__(
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
    def arrow_width(self) -> typing.Optional[typings.Number]:
        r"""
        Gets arrow width of arrow.
        """
        return super().arrow_width

    @property
    def dash_fraction(self) -> typing.Optional[typings.Number]:
        r"""
        Gets dash fraction of arrow.
        """
        return super().dash_fraction

    @property
    def dash_period(self) -> typing.Optional[typings.Number]:
        r"""
        Gets dash period of arrow.
        """
        return super().dash_period

    @property
    def left_broken_text(self) -> typing.Union[bool, str, Markup, None]:
        r"""
        Gets left broken text of arrow.
        """
        return self._left_broken_text

    @property
    def right_broken_arrow(self) -> typing.Optional[bool]:
        r"""
        Is true when arrow should appear immediately before line break.
        """
        return self._right_broken_arrow

    @property
    def style(self) -> typing.Optional[str]:
        r"""
        Gets style of arrow.
        """
        return super().style

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on arrow line segment.
        """
        pass
