from experimental.tools.specificationtools.ExpressionInventory import ExpressionInventory
from experimental.tools.specificationtools.SetMethodMixin import SetMethodMixin


class SelectExpressionInventory(ExpressionInventory, SetMethodMixin):
    '''Select expression inventory.
    '''

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Select expression inventory score specification.

        Return score specification.
        '''
        return self._score_specification
