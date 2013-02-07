import abc
import copy
from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.expressiontools.AttributeNameEnumeration import AttributeNameEnumeration


class Interpreter(AbjadObject):
    r'''Interpreter.

    Abstract interpreter class from which conrete interpreters inherit.
    ''' 

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = AttributeNameEnumeration()

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, score_specification):
        '''Top-level interpretation entry point.
        
        Write custom interpreter code by extending this method.
        '''
        self.score_specification = score_specification
        self.score = self.instantiate_score()
        self.evaluate_multiple_context_set_expressions()
        self.store_score_rooted_single_context_set_expressions_by_context()
        self.store_segment_rooted_single_context_set_expressions_by_context()
        
    ### PUBLIC METHODS ###

    def evaluate_multiple_context_set_expressions(self):
        for multiple_context_set_expression in self.score_specification.multiple_context_set_expressions:
            multiple_context_set_expression.evaluate_and_store_in_root_specification()
                
    def instantiate_score(self):
        '''Instantiate score.

        Include time signature context.
        
        Return score.
        '''
        score = self.score_specification.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        score.insert(0, context)
        return score

    def store_score_rooted_single_context_set_expressions_by_context(self):
        for fresh_single_context_set_expression in self.score_specification.fresh_single_context_set_expressions:
            fresh_single_context_set_expression.store_in_score_specification_by_context_and_attribute()

    def store_segment_rooted_single_context_set_expressions_by_context(self):
        from experimental.tools import specificationtools
        score = self.score_specification.score_template()
        persistent_single_context_set_expressions_by_context = specificationtools.ContextProxyDictionary(score)
        for segment_specification in self.score_specification.segment_specifications:
            # get persistent single-context set expressions
            persistent_single_context_set_expressions = []
            for context_proxy in persistent_single_context_set_expressions_by_context.itervalues():
                for attribute, settings in context_proxy.single_context_set_expressions_by_attribute.items():
                    persistent_single_context_set_expressions.extend(settings)
            # store persistent single-context set expressions in current segment specification
            for persistent_single_context_set_expression in persistent_single_context_set_expressions:
                persistent_single_context_set_expression = \
                    persistent_single_context_set_expression.copy_and_set_root(
                    segment_specification.segment_name)
                persistent_single_context_set_expression.store_in_segment_specification_by_context_and_attribute()
            # store fresh single-context-set expressions in current segment specification
            for fresh_single_context_set_expression in segment_specification.fresh_single_context_set_expressions:
                fresh_single_context_set_expression.store_in_segment_specification_by_context_and_attribute()
                if fresh_single_context_set_expression.persist:
                    target_context_name = fresh_single_context_set_expression.target_context_name
                    attribute = fresh_single_context_set_expression.attribute
                    expressions = persistent_single_context_set_expressions_by_context[
                        target_context_name].single_context_set_expressions_by_attribute[attribute]
                    for expression in expressions[:]:
                        if expression.target_timespan == \
                            fresh_single_context_set_expression.target_timespan:
                            expressions.remove(expression)
                    expressions.append(fresh_single_context_set_expression)
