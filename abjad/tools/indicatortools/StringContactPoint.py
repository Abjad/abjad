# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class StringContactPoint(AbjadObject):
    r'''String contact point indicator.

    ::

        >>> indicator = indicatortools.StringContactPoint('pont')
        >>> print(format(indicator))
        indicatortools.StringContactPoint(
            contact_point='pont',
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contact_point',
        )

    ### INITIALIZER ###

    def __init__(self,
        contact_point=None,
        ):
        self._contact_point = contact_point

    ### PUBLIC PROPERTIES ###

    @property
    def contact_point(self):
        r'''Gets contact point.

        ::

            >>> indicator = indicatortools.StringContactPoint('tasto')
            >>> indicator.contact_point
            'tasto'

        '''
        return self._contact_point
