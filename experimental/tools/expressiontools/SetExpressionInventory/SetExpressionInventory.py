from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.expressiontools.AttributeNameEnumeration import AttributeNameEnumeration


class SetExpressionInventory(ObjectInventory):
    r'''Single inventory.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = AttributeNameEnumeration()

    ### PUBLIC METHODS ###

    # TODO: reorder parameters attribute, timespan, target_context_name, persist
    # TODO: maybe remove segment_name parameter?
    def get_set_expression(self, attribute=None, target_context_name=None, persist=None, timespan=None, segment_name=None):
        set_expressions = self.get_set_expressions(attribute=attribute, 
            target_context_name=target_context_name, persist=persist, timespan=timespan, segment_name=segment_name)
        if not set_expressions:
            error ='no set expressions for {!r} found in segment {!r}.'.format(attribute, segment_name)
            raise Exception(error)
        elif 1 < len(set_expressions):
            error = 'multiple set expressions for {!r} found in segment {!r}.'.format(attribute, segment_name)
            raise Exception(error)
        assert len(set_expressions) == 1
        return set_expressions[0]

    # TODO: reorder input parameters
    def get_set_expressions(self, attribute=None, target_context_name=None, persist=None, timespan=None, target=None):
        assert attribute in self.attributes, repr(attribute)
        set_expressions = []
        for set_expression in self:
            if (
                (attribute is None or set_expression.attribute == attribute) and
                (target is None or set_expression.target == target) and
                (target_context_name is None or set_expression.target.target_context_name == target_context_name) and
                (timespan is None or set_expression.target.timespan == timespan) and
                (persist is None or set_expression.persist == persist)
                ):
                set_expressions.append(set_expression)
        return set_expressions
