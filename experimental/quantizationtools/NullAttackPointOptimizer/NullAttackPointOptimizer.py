from experimental.quantizationtools.AttackPointOptimizer import AttackPointOptimizer

class NullAttackPointOptimizer(AttackPointOptimizer):
    '''Concrete ``AttackPointOptimizer`` subclass which performs
    no attack point optimization.

    Return ``NullAttackPointOptimizer`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        pass
