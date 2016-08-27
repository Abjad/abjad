# -*- coding: utf-8 -*-
import abc
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class IntervalClass(AbjadValueObject):
    '''Interval-class base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of interval-class.

        Returns new interval-class.
        '''
        return type(self)(abs(self._number))

    def __float__(self):
        r'''Changes interval-class to float.

        Returns float.
        '''
        return float(self._number)

    def __int__(self):
        r'''Change interval-class to integer.

        Returns integer.
        '''
        return self._number

    def __str__(self):
        r'''String representation of interval-class.

        Returns string.
        '''
        return self._format_string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        if type(self).__name__.startswith('Named'):
            values = [str(self)]
        else:
            values = [
                mathtools.integer_equivalent_number_to_integer(float(self))
                ]
        return systemtools.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            template_names=['number'],
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return str(self.number)

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        r'''Number of interval-class.

        Returns number.
        '''
        return self._number
