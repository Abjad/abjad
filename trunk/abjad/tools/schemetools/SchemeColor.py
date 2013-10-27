# -*- encoding: utf-8 -*-
from abjad.tools.schemetools.Scheme import Scheme


class SchemeColor(Scheme):
    r'''Abjad model of Scheme color:

    ::

        >>> schemetools.SchemeColor('ForestGreen')
        SchemeColor('ForestGreen')

    Scheme colors are immutable.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        return "(x11-color '%s)" % self._value
