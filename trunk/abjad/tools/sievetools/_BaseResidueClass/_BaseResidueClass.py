import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class _BaseResidueClass(AbjadObject):
    '''Abstract base class for ResidueClass and ResidueClassExpression.
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
        from abjad.tools.sievetools.ResidueClassExpression import ResidueClassExpression
        if isinstance(self, ResidueClassExpression) and self.operator == op:
            argA = self.rcs
        else:
            argA = [self]
        if isinstance(arg, ResidueClassExpression) and arg.operator == op:
            argB = arg.rcs
        else:
            argB = [arg]
        return ResidueClassExpression(argA + argB, op)
