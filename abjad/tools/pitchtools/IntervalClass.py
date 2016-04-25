# -*- coding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class IntervalClass(AbjadObject):
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

    def __hash__(self):
        r'''Hashes interval-class.

        Returns integer.
        '''
        return hash(repr(self))

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

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return str(self.number)

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=(
                self.number,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        r'''Number of interval-class.

        Returns number.
        '''
        return self._number
