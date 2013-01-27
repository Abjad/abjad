from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.expressiontools.AttributeNameEnumeration import AttributeNameEnumeration


class SetExpressionInventory(ObjectInventory):
    r'''Single inventory.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = AttributeNameEnumeration()

    ### PUBLIC METHODS ###

    def get_set_expression(self, attribute=None, context_name=None, persist=None, timespan=None, segment_name=None):
        set_expressions = self.get_set_expressions(attribute=attribute, 
            context_name=context_name, persist=persist, timespan=timespan, segment_name=segment_name)
        if not set_expressions:
            error ='no set expressions for {!r} found in segment {!r}.'.format(attribute, segment_name)
            raise Exception(error)
        elif 1 < len(set_expressions):
            error = 'multiple set expressions for {!r} found in segment {!r}.'.format(attribute, segment_name)
            raise Exception(error)
        assert len(set_expressions) == 1
        return set_expressions[0]

    def get_set_expressions(self, attribute=None, context_name=None, persist=None, timespan=None, target=None):
        assert attribute in self.attributes, repr(attribute)
        set_expressions = []
        for set_expression in self:
            if (
                (attribute is None or set_expression.attribute == attribute) and
                (target is None or set_expression.target == target) and
                (context_name is None or set_expression.target.context_name == context_name) and
                (timespan is None or set_expression.target.timespan == timespan) and
                (persist is None or set_expression.persist == persist)
                ):
                set_expressions.append(set_expression)
        return set_expressions
