# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.ExpressionInventory \
    import ExpressionInventory
from experimental.tools.musicexpressiontools.SetMethodMixin \
    import SetMethodMixin


class SelectExpressionInventory(ExpressionInventory, SetMethodMixin):
    r'''Select expression inventory.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        r'''Select expression inventory score specification.

        Returns score specification.
        '''
        return self._score_specification