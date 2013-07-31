import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class BaseResidueClass(AbjadObject):
    r'''Abstract base class for ResidueClass and Sieve.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta
    
    __slots__ = ()

    ### SPECIAL METHODS ###

    # TODO: implement __neg__() #

    def __and__(self, arg):
        assert isinstance(arg, BaseResidueClass)
        return self._operate(arg, 'and')

    def __or__(self, arg):
        assert isinstance(arg, BaseResidueClass)
        return self._operate(arg, 'or')

    def __xor__(self, arg):
        assert isinstance(arg, BaseResidueClass)
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
