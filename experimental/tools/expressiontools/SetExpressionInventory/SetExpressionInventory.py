from abjad.tools.timespantools.TimespanInventory import TimespanInventory


class SetExpressionInventory(TimespanInventory):
    r'''Set expression inventory.
    '''

    ### PUBLIC METHODS ###

    # TODO: remove
    def get_set_expressions(self, attribute=None):
        set_expressions = []
        for set_expression in self:
            if attribute is None or set_expression.attribute == attribute:
                set_expressions.append(set_expression)
        return set_expressions
