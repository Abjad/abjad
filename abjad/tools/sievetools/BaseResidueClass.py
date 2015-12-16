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
            argA = self.residue_classes
        else:
            argA = [self]
        if (isinstance(arg, sievetools.Sieve) and 
            arg.logical_operator == op):
            argB = arg.residue_classes
        else:
            argB = [arg]
        sieve = sievetools.Sieve(argA + argB, op)
        return sieve