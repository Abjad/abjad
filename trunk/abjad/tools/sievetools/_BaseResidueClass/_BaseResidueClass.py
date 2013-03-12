import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class _BaseResidueClass(AbjadObject):
    '''Abstract base class for ResidueClass and Sieve.
    '''

    __metaclass__ = abc.ABCMeta
    __slots__ = ()

    ### SPECIAL METHODS ###

    # TODO: implement __neg__() #

    def __and__(self, arg):
        assert isinstance(arg, _BaseResidueClass)
        return self._operate(arg, 'and')

    def __or__(self, arg):
        assert isinstance(arg, _BaseResidueClass)
        return self._operate(arg, 'or')

    def __xor__(self, arg):
        assert isinstance(arg, _BaseResidueClass)
        return self._operate(arg, 'xor')

    ### PRIVATE METHODS ###

    def _operate(self, arg, op):
        from abjad.tools.sievetools.Sieve import Sieve
        if isinstance(self, Sieve) and self.logical_operator == op:
            argA = self.rcs
        else:
            argA = [self]
        if isinstance(arg, Sieve) and arg.logical_operator == op:
            argB = arg.rcs
        else:
            argB = [arg]
        return Sieve(argA + argB, op)
