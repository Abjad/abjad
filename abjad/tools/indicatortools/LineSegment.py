# -*- coding: utf-8 -*-
from abjad.tools import lilypondnametools
from abjad.tools import schemetools
from abjad.tools.abctools import AbjadValueObject


class LineSegment(AbjadValueObject):
    r'''A line segment.

    Line segments format as text spanners.

    ..  container:: example

        **Example 1.** Default line segment:

        ::

            >>> line_segment = indicatortools.LineSegment()
            >>> f(line_segment)
            LineSegment()

    .. todo:: Add examples.

    Use line segments to start a markup-terminated text spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_arrow_width',
        '_dash_fraction',
        '_dash_period',
        '_default_scope',
        '_left_broken_padding',
        '_left_broken_text',
        '_left_hspace',
        '_left_padding',
        '_left_stencil_align_direction_y',
        '_right_arrow',
        '_right_broken_arrow',
        '_right_broken_padding',
        '_right_padding',
        '_right_stencil_align_direction_y',
        '_style',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        arrow_width=None,
        dash_fraction=None,
        dash_period=None,
        left_broken_padding=None,
        left_broken_text=None,
        left_hspace=None,
        left_padding=None,
        left_stencil_align_direction_y=None,
        right_arrow=None,
        right_broken_arrow=None,
        right_broken_padding=None,
        right_padding=None,
        right_stencil_align_direction_y=None,
        style=None,
        ):
        self._default_scope = None
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
        self._right_padding = right_padding
        self._right_stencil_align_direction_y = right_stencil_align_direction_y
        self._style = style

    ### PRIVATE METHODS ###

    def _get_lilypond_grob_overrides(self):
        overrides = []
        if self.arrow_width is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'arrow-width',
                    ),
                value=self.arrow_width,
                )
            overrides.append(override_)
        if self.dash_fraction is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'dash-fraction',
                    ),
                value=self.dash_fraction,
                )
            overrides.append(override_)
        if self.dash_period is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'dash-period',
                    ),
                value=self.dash_period,
                )
            overrides.append(override_)
        if self.left_broken_padding is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'left-broken',
                    'padding',
                    ),
                value=self.left_broken_padding,
                )
            overrides.append(override_)
        if self.left_broken_text is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'left-broken',
                    'text',
                    ),
                value=self.left_broken_text,
                )
            overrides.append(override_)
        if self.left_padding is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'left',
                    'padding',
                    ),
                value=self.left_padding,
                )
            overrides.append(override_)
        if self.left_stencil_align_direction_y is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'left',
                    'stencil-align-dir-y',
                    ),
                value=self.left_stencil_align_direction_y,
                )
            overrides.append(override_)
        if self.right_arrow is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'arrow',
                    ),
                value=self.right_arrow,
                )
            overrides.append(override_)
        if self.right_broken_arrow is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'right-broken',
                    'arrow',
                    ),
                value=self.right_broken_arrow,
                )
            overrides.append(override_)
        if self.right_broken_padding is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'right-broken',
                    'padding',
                    ),
                value=self.right_broken_padding,
                )
            overrides.append(override_)
        if self.right_padding is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'padding',
                    ),
                value=self.right_padding,
                )
            overrides.append(override_)
        if self.right_stencil_align_direction_y is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'stencil-align-dir-y',
                    ),
                value=self.right_stencil_align_direction_y,
                )
            overrides.append(override_)
        if self.style is not None:
            style = schemetools.Scheme(self.style, quoting="'")
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'style',
                    ),
                value=style,
                )
            overrides.append(override_)
        return overrides

    ### PUBLIC PROPERTIES ###

    @property
    def arrow_width(self):
        r'''Gets arrow width of line segment.

        Returns float or none.
        '''
        return self._arrow_width

    @property
    def dash_fraction(self):
        r'''Gets dash fraction of line segment.

        Returns float or none.
        '''
        return self._dash_fraction

    @property
    def dash_period(self):
        r'''Gets dash period of line segment.

        Returns float or none.
        '''
        return self._dash_period

    @property
    def default_scope(self):
        r'''Gets default scope of line segment.

        Returns none.
        '''
        return self._default_scope

    @property
    def left_broken_padding(self):
        r'''Gets left broken padding of line segment.

        Returns float or none.
        '''
        return self._left_broken_padding

    @property
    def left_broken_text(self):
        r'''Gets left broken text of line segment.

        Returns markup, false or none.
        '''
        return self._left_broken_text

    @property
    def left_hspace(self):
        r'''Gets left hspace of line segment.

        Returns float or none.
        '''
        return self._left_hspace

    @property
    def left_padding(self):
        r'''Gets left padding of line segment.

        Returns float or none.
        '''
        return self._left_padding

    @property
    def left_stencil_align_direction_y(self):
        r'''Gets left stencil align direction Y of line segment.

        Returns float or none.
        '''
        return self._left_stencil_align_direction_y

    @property
    def right_arrow(self):
        r'''Is true when right end of line segment carries an arrow.
        Otherwise false.

        Returns true, false or none.
        '''
        return self._right_arrow

    @property
    def right_broken_arrow(self):
        r'''Gets right broken arrow of line segment.

        Returns float or none.
        '''
        return self._right_broken_arrow
        
    @property
    def right_broken_padding(self):
        r'''Gets right broken padding of line segment.

        Returns float or none.
        '''
        return self._right_broken_padding

    @property
    def right_padding(self):
        r'''Gets right padding of line segment.

        Returns float or none.
        '''
        return self._right_padding

    @property
    def right_stencil_align_direction_y(self):
        r'''Gets right stencil align direction Y of line segment.

        Returns float or none.
        '''
        return self._right_stencil_align_direction_y

    @property
    def style(self):
        r'''Gets style of line segment.

        Returns string or none.
        '''
        return self._style
