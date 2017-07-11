# -*- coding: utf-8 -*-
from abjad.tools.schemetools.Scheme import Scheme


class SchemeColor(Scheme):
    r'''Abjad model of Scheme color.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> abjad.SchemeColor('ForestGreen')
            SchemeColor('ForestGreen')

    Scheme colors are immutable.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        string = "(x11-color '{})"
        string = string.format(self._value)
        return string
