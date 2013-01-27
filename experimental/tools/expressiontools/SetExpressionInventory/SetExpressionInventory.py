from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.expressiontools.AttributeNameEnumeration import AttributeNameEnumeration


class SetExpressionInventory(ObjectInventory):
    r'''Single inventory.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = AttributeNameEnumeration()

    ### PUBLIC METHODS ###

    # TODO: reorder parameters attribute, timespan, target_context_name, persist
    def get_set_expression(self, attribute=None, target_context_name=None, persist=None, timespan=None):
        set_expressions = self.get_set_expressions(attribute=attribute, 
            target_context_name=target_context_name, persist=persist, timespan=timespan)
        if not set_expressions:
            error ='no set expressions for {!r} found.'.format(attribute)
            raise Exception(error)
        elif 1 < len(set_expressions):
            error = 'multiple set expressions for {!r} found.'.format(attribute)
            raise Exception(error)
        assert len(set_expressions) == 1
        return set_expressions[0]

    # TODO: reorder input parameters
    def get_set_expressions(self, attribute=None, target_context_name=None, persist=None, timespan=None):
        assert attribute in self.attributes, repr(attribute)
        set_expressions = []
        for set_expression in self:
            if (
                (attribute is None or set_expression.attribute == attribute) and
                (target_context_name is None or set_expression.target_context_name == target_context_name) and
                (timespan is None or set_expression.target_timespan == timespan) and
                (persist is None or set_expression.persist == persist)
                ):
                set_expressions.append(set_expression)
        return set_expressions
