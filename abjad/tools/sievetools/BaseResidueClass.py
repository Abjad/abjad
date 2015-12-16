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

    def _operate(self, arg, operator):
        from abjad.tools import sievetools
        if (isinstance(self, sievetools.CompoundSieve) and 
            self.logical_operator == operator):
            argument_a = self.sieves
        else:
            argument_a = [self]
        if (isinstance(arg, sievetools.CompoundSieve) and 
            arg.logical_operator == operator):
            argument_b = arg.sieves
        else:
            argument_b = [arg]
        sieve = sievetools.CompoundSieve(argument_a + argument_b, operator)
        return sieve