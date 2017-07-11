# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.selectortools.Inequality import Inequality


class LengthInequality(Inequality):
    r'''Length inequality.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> inequality = abjad.LengthInequality('<', 4)
            >>> f(inequality)
            abjad.LengthInequality(
                operator_string='<',
                length=4,
                )

        ::

            >>> inequality([1, 2, 3])
            True

        ::

            >>> inequality([1, 2, 3, 4])
            False

        ::

            >>> inequality([1, 2, 3, 4, 5])
            False

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Inequalities'

    __slots__ = (
        '_length',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        operator_string='<',
        length=mathtools.Infinity(),
        ):
        Inequality.__init__(
            self,
            operator_string=operator_string,
            )
        assert 0 <= length
        infinities = (
            mathtools.Infinity(),
            mathtools.NegativeInfinity(),
            )
        if length not in infinities:
            length = int(length)
        self._length = length

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls length inequality on `argument`.

        Returns true or false.
        '''
        length = len(argument)
        result = self._operator_function(length, self._length)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        r'''Gets length.

        Returns integer.
        '''
        return self._length
