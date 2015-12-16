# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class BaseResidueClass(AbjadObject):
    r'''Base residue class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    # TODO: implement __neg__() #

    def __and__(self, arg):
        r'''Logical AND of residue class and `arg`.

        Returns sieve.
        '''
        assert isinstance(arg, BaseResidueClass), repr(arg)
        return self._operate(arg, 'and')

    def __or__(self, arg):
        r'''Logical OR of residue class and `arg`.

        Returns sieve.
        '''
        assert isinstance(arg, BaseResidueClass), repr(arg)
        return self._operate(arg, 'or')

    def __xor__(self, arg):
        r'''Logical XOR of residue class and `arg`.

        Returns sieve.
        '''
        assert isinstance(arg, BaseResidueClass), repr(arg)
        return self._operate(arg, 'xor')

    ### PRIVATE METHODS ###

    def _operate(self, arg, op):
        from abjad.tools import sievetools
        if (isinstance(self, sievetools.Sieve) and 
            self.logical_operator == op):
            argA = self.rcs
        else:
            argA = [self]
        if (isinstance(arg, sievetools.Sieve) and 
            arg.logical_operator == op):
            argB = arg.rcs
        else:
            argB = [arg]
        sieve = sievetools.Sieve(argA + argB, op)
        return sieve

    # TODO: deprecated
    @staticmethod
    def _process_min_max_attribute(*min_max):
        r'''Process minimum and maximum attributes.
        The function expects at least one and at most two attributes.
        Lone argument taken as range maximum.
        '''
        if len(min_max) == 0 or 2 < len(min_max):
            raise ValueError(min_max)
        elif len(min_max) == 1:
            minimum = 0
            maximum = min_max[0]
        else:
            minimum = min_max[0]
            maximum = min_max[1]
        if not (minimum < maximum and
            isinstance(minimum, int) and
            isinstance(maximum, int)):
            message = 'arguments must be integers and min < max.'
            raise ValueError(message)
        return minimum, maximum