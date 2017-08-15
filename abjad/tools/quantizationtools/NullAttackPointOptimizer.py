from abjad.tools.quantizationtools.AttackPointOptimizer \
    import AttackPointOptimizer


class NullAttackPointOptimizer(AttackPointOptimizer):
    r'''Null attack-point optimizer.

    Performs no attack point optimization.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls null attack-point optimizer.
        '''
        pass
