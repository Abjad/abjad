# -*- encoding: utf-8 -*-
from abjad.tools import lilypondnametools
from abjad.tools.abctools import AbjadObject


class LineSegment(AbjadObject):
    r'''A transition.

    Transitions format as text spanners.

    ..  container:: example

        ::

            >>> transition = indicatortools.LineSegment()
            >>> f(transition)
            LineSegment()

    .. todo:: add examples.

    Use transitions to start the body of a text spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_arrow_width',
        '_dash_fraction',
        '_dash_period',
        '_left_arrow',
        '_left_attach_direction',
        '_left_broken_padding',
        '_left_padding',
        '_right_arrow',
        '_right_attach_direction',
        '_right_broken_padding',
        '_right_padding',
        '_style',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        arrow_width=None,
        dash_fraction=None,
        dash_period=None,
        left_arrow=None,
        left_attach_direction=None,
        left_broken_padding=None,
        left_padding=None,
        right_arrow=None,
        right_attach_direction=None,
        right_broken_padding=None,
        right_padding=None,
        style=None,
        ):
        self._arrow_width = arrow_width
        self._dash_fraction = dash_fraction
        self._dash_period = dash_period
        self._left_arrow = left_arrow
        self._left_attach_direction = left_attach_direction
        self._left_broken_padding = left_broken_padding
        self._left_padding = left_padding
        self._right_arrow = right_arrow
        self._right_attach_direction = right_attach_direction
        self._right_broken_padding = right_broken_padding
        self._right_padding = right_padding
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
        if self.left_arrow is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'left',
                    'arrow',
                    ),
                value=self.left_arrow,
                )
            overrides.append(override_)
        if self.left_attach_direction is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'left',
                    'attach-dir',
                    ),
                value=self.left_attach_direction,
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
        if self.right_attach_direction is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'attach-dir',
                    ),
                value=self.right_attach_direction,
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
        if self.style is not None:
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='TextSpanner',
                is_once=True,
                property_path=(
                    'style',
                    ),
                value=self.style,
                )
            overrides.append(override_)
        return overrides

    ### PUBLIC PROPERTIES ###

    @property
    def arrow_width(self):
        r'''Gets arrow width of transition.

        Returns float or none.
        '''
        return self._arrow_width

    @property
    def dash_fraction(self):
        r'''Gets dash fraction of transition.

        Returns float or none.
        '''
        return self._dash_fraction

    @property
    def dash_period(self):
        r'''Gets dash period of transition.

        Returns float or none.
        '''
        return self._dash_period

    @property
    def left_arrow(self):
        r'''Is true when left end of transition carries an arrow.
        Otherwise false.

        Returns true, false or none.
        '''
        return self._left_arrow

    @property
    def left_attach_direction(self):
        r'''Gets left attach direction of transition.

        Returns float or none.
        '''
        return self._left_attach_direction

    @property
    def left_broken_padding(self):
        r'''Gets left broken padding of transition.

        Returns float or none.
        '''
        return self._left_broken_padding

    @property
    def left_padding(self):
        r'''Gets left padding of transition.

        Returns float or none.
        '''
        return self._left_padding

    @property
    def right_arrow(self):
        r'''Is true when right end of transition carries an arrow.
        Otherwise false.

        Returns true, false or none.
        '''
        return self._right_arrow

    @property
    def right_attach_direction(self):
        r'''Gets right attach direction of transition.

        Returns float or none.
        '''
        return self._right_attach_direction

    @property
    def right_broken_padding(self):
        r'''Gets right broken padding of transition.

        Returns float or none.
        '''
        return self._right_broken_padding

    @property
    def right_padding(self):
        r'''Gets right padding of transition.

        Returns float or none.
        '''
        return self._right_padding

    @property
    def style(self):
        r'''Gets style of transition.

        Returns string or none.
        '''
        return self._style