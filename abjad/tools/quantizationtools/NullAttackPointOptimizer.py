# -*- coding: utf-8 -*-
from abjad.tools.quantizationtools.AttackPointOptimizer \
	import AttackPointOptimizer


class NullAttackPointOptimizer(AttackPointOptimizer):
    r'''Concrete ``AttackPointOptimizer`` subclass which performs
    no attack point optimization.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls null attack-point optimizer.
        '''
        pass
