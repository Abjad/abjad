import typing
from abjad.enumerations import Center, VerticalAlignment
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.lilypondnametools.LilyPondGrobOverride import (
    LilyPondGrobOverride,
)
from abjad.tools.markuptools.Markup import Markup
from abjad.tools.schemetools.Scheme import Scheme
from abjad.tools.systemtools.LilyPondFormatManager import LilyPondFormatManager
Number = typing.Union[int, float]


class LineSegment(AbjadValueObject):
    """
    Line segment.

    Line segments format as text spanners.

    ..  container:: example

        >>> line_segment = abjad.LineSegment()
        >>> abjad.f(line_segment)
        abjad.LineSegment()

    .. todo:: Add examples.

    Use line segments to start a markup-terminated text spanner.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_arrow_width',
        '_dash_fraction',
        '_dash_period',
        '_left_broken_padding',
        '_left_broken_text',
        '_left_hspace',
        '_left_padding',
        '_left_stencil_align_direction_y',
        '_right_arrow',
        '_right_broken_arrow',
        '_right_broken_padding',
        '_right_broken_text',
        '_right_padding',
        '_right_stencil_align_direction_y',
        '_right_text',
        '_style',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        arrow_width: Number = None,
        dash_fraction: Number = None,
        dash_period: Number = None,
        left_broken_padding: Number = None,
        left_broken_text: typing.Union[bool, str, Markup] = None,
        left_hspace: Number = None,
        left_padding: Number = None,
        left_stencil_align_direction_y: typing.Union[
            Number, VerticalAlignment] = None,
        right_arrow: bool = None,
        right_broken_arrow: bool = None,
        right_broken_padding: Number = None,
        right_broken_text: typing.Union[bool, str, Markup] = None,
        right_padding: Number = None,
        right_stencil_align_direction_y: typing.Union[
            Number, VerticalAlignment] = None,
        right_text: typing.Union[bool, str, Markup] = None,
        style: str = None,
        ) -> None:
        self._arrow_width = arrow_width
        self._dash_fraction = dash_fraction
        self._dash_period = dash_period
        self._left_broken_padding = left_broken_padding
        self._left_broken_text = left_broken_text
        self._left_padding = left_padding
        self._left_hspace = left_hspace
        self._left_stencil_align_direction_y = left_stencil_align_direction_y
        self._right_arrow = right_arrow
        self._right_broken_arrow = right_broken_arrow
        self._right_broken_padding = right_broken_padding
        self._right_broken_text = right_broken_text
        self._right_padding = right_padding
        self._right_stencil_align_direction_y = right_stencil_align_direction_y
        self._right_text = right_text
        self._style = style

    ### PRIVATE METHODS ###

    def _get_lilypond_grob_overrides(self, tweaks=False):
        overrides = []
        if self.arrow_width is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'arrow-width',
                    ),
                value=self.arrow_width,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.dash_fraction is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'dash-fraction',
                    ),
                value=self.dash_fraction,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.dash_period is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'dash-period',
                    ),
                value=self.dash_period,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.left_broken_padding is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'left-broken',
                    'padding',
                    ),
                value=self.left_broken_padding,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.left_broken_text is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'left-broken',
                    'text',
                    ),
                value=self.left_broken_text,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.left_padding is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'left',
                    'padding',
                    ),
                value=self.left_padding,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.left_stencil_align_direction_y is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'left',
                    'stencil-align-dir-y',
                    ),
                value=self.left_stencil_align_direction_y,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.right_arrow is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'arrow',
                    ),
                value=self.right_arrow,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.right_broken_arrow is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'right-broken',
                    'arrow',
                    ),
                value=self.right_broken_arrow,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.right_broken_padding is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'right-broken',
                    'padding',
                    ),
                value=self.right_broken_padding,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.right_broken_text is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'right-broken',
                    'text',
                    ),
                value=self.right_broken_text,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.right_padding is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'padding',
                    ),
                value=self.right_padding,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.right_stencil_align_direction_y is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'stencil-align-dir-y',
                    ),
                value=self.right_stencil_align_direction_y,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.right_text is not None:
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'text',
                    ),
                value=self.right_text,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        if self.style is not None:
            style = Scheme(self.style, quoting="'")
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'style',
                    ),
                value=style,
                )
            if tweaks is True:
                overrides.append(override.tweak_string())
            else:
                overrides.append(override.override_string)
        assert all(isinstance(_, str) for _ in overrides)
        return overrides

    ### PUBLIC PROPERTIES ###

    @property
    def arrow_width(self) -> typing.Optional[Number]:
        """
        Gets arrow width of line segment.
        """
        return self._arrow_width

    @property
    def dash_fraction(self) -> typing.Optional[Number]:
        """
        Gets dash fraction of line segment.
        """
        return self._dash_fraction

    @property
    def dash_period(self) -> typing.Optional[Number]:
        """Gets dash period of line segment.
        """
        return self._dash_period

    @property
    def left_broken_padding(self) -> typing.Optional[Number]:
        """
        Gets left broken padding of line segment.
        """
        return self._left_broken_padding

    @property
    def left_broken_text(self) -> typing.Union[bool, str, Markup, None]:
        """
        Gets left broken text of line segment.
        """
        return self._left_broken_text

    @property
    def left_hspace(self) -> typing.Optional[Number]:
        """
        Gets left hspace of line segment.
        """
        return self._left_hspace

    @property
    def left_padding(self) -> typing.Optional[Number]:
        """
        Gets left padding of line segment.
        """
        return self._left_padding

    @property
    def left_stencil_align_direction_y(self) -> typing.Union[
        Number, VerticalAlignment, None]:
        """
        Gets left stencil align direction Y of line segment.
        """
        return self._left_stencil_align_direction_y

    @property
    def right_arrow(self) -> typing.Optional[bool]:
        """
        Is true when right end of line segment carries an arrow.
        """
        return self._right_arrow

    @property
    def right_broken_arrow(self) -> typing.Optional[bool]:
        """
        Gets right broken arrow of line segment.
        """
        return self._right_broken_arrow

    @property
    def right_broken_padding(self) -> typing.Optional[Number]:
        """
        Gets right broken padding of line segment.
        """
        return self._right_broken_padding

    @property
    def right_broken_text(self) -> typing.Union[bool, str, Markup, None]:
        """
        Gets right broken text of line segment.
        """
        return self._right_broken_text

    @property
    def right_padding(self) -> typing.Optional[Number]:
        """
        Gets right padding of line segment.
        """
        return self._right_padding

    @property
    def right_stencil_align_direction_y(self) -> typing.Union[
        Number, VerticalAlignment, None]:
        """
        Gets right stencil align direction Y of line segment.
        """
        return self._right_stencil_align_direction_y

    @property
    def right_text(self) -> typing.Union[bool, str, Markup, None]:
        """
        Gets right text.
        """
        return self._right_text

    @property
    def style(self) -> typing.Optional[str]:
        """
        Gets style of line segment.
        """
        return self._style

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on line segment.
        """
        pass
