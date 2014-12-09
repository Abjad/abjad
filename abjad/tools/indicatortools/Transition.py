# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Transition(AbjadObject):
    r'''A transition.

    Transitions format as text spanners.

    ..  container:: example

        ::

            >>> transition = indicatortools.Transition()
            >>> f(transition)
            Transition()

    .. todo:: add examples.

    Use transitions to start the body of a text spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
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

    ### PUBLIC PROPERTIES ###

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