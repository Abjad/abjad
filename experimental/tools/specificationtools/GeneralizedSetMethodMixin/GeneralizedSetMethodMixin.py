from experimental.tools.specificationtools.SetMethodMixin import SetMethodMixin


class GeneralizedSetMethodMixin(SetMethodMixin):
    '''Generalized set method mixin.
    '''

    ### PUBLIC METHODS ###

    def set_pitches(self, source_expression):
        r'''Set pitches to `source_expression` for select expressions in inventory.

        Return pitch set expression.
        '''
        attribute = 'pitch'
        return self._store_generalized_set_expression(attribute, source_expression)
