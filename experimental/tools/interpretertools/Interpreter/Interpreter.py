import abc
import copy
from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.expressiontools.AttributeNameEnumeration import AttributeNameEnumeration


class Interpreter(AbjadObject):
    r'''

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
        self.store_single_context_set_expressions_in_segments_by_context_and_attribute()
        
    ### PUBLIC METHODS ###

    def evaluate_multiple_context_set_expressions(self):
        for multiple_context_set_expression in self.score_specification.multiple_context_set_expressions:
            attribute = multiple_context_set_expression.attribute
            fresh_single_context_set_expressions = multiple_context_set_expression.evaluate()
            assert all([x.fresh for x in fresh_single_context_set_expressions])
            root_segment_specification = multiple_context_set_expression.root_segment_specification
            root_segment_specification.fresh_single_context_set_expressions_by_attribute[
                attribute].extend(fresh_single_context_set_expressions)
            self.score_specification.fresh_single_context_set_expressions_by_attribute[
                attribute].extend(fresh_single_context_set_expressions)
            #if multiple_context_set_expression.is_segment_rooted:
            #    root_segment_specification = multiple_context_set_expression.root_segment_specification
            #    root_segment_specification.fresh_single_context_set_expressions_by_attribute.[
            #         attribute].extend(fresh_single_context_set_expressions)
                
    def instantiate_score(self):
        score = self.score_specification.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        score.insert(0, context)
        return score

    def store_single_context_set_expressions_in_segments_by_context_and_attribute(self):
        for segment_specification in self.score_specification.segment_specifications:
            for attribute in self.attributes:
                fresh_single_context_set_expressions = \
                    segment_specification.fresh_single_context_set_expressions_by_attribute[attribute]
                fresh_context_names = [x.target_context_name for x in fresh_single_context_set_expressions]
                assert all([x.fresh for x in fresh_single_context_set_expressions])
                persistent_single_context_set_expressions = []
                for context_proxy in self.score_specification.context_proxies.itervalues():
                    set_expressions = context_proxy.single_context_set_expressions_by_attribute.get(attribute, [])
                    persistent_single_context_set_expressions.extend(set_expressions)
                assert all([x.persist for x in persistent_single_context_set_expressions])
                set_expressions_to_store = fresh_single_context_set_expressions
                for persistent_single_context_set_expression in persistent_single_context_set_expressions[:]:
                    if persistent_single_context_set_expression.target_context_name not in fresh_context_names:
                        set_expression_to_store = persistent_single_context_set_expression.copy_and_set_root(
                            segment_specification.segment_name)
                        set_expressions_to_store.append(set_expression_to_store)
                for set_expression_to_store in set_expressions_to_store:
                    set_expression_to_store.store_in_segment_by_context_and_attribute()
