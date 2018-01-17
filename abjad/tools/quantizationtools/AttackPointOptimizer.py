import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class AttackPointOptimizer(AbjadObject):
    r'''Abstract attack-point optimizer.

    Attack-point optimizers may alter the number, order, and individual
    durations of leaves in a logical tie, but may not alter the overall
    duration of that logical tie.

    They effectively "clean up" notation, post-quantization.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, argument):
        r'''Calls attack-point optimizer.
        '''
        raise NotImplementedError
