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
        self.copy_persistent_segment_rooted_set_expressions_into_segment_specifications()
        
    ### PUBLIC METHODS ###

    def copy_persistent_segment_rooted_set_expressions_into_segment_specifications(self):
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
                    persistent_single_context_set_expression.copy_and_set_root(segment_specification.segment_name)
                persistent_single_context_set_expression.store_in_segment_by_context_and_attribute()
            # store fresh single-context-set expressions in current segment specification
            for attribute in self.attributes:
                fresh_single_context_set_expressions = \
                    segment_specification.fresh_single_context_set_expressions_by_attribute[attribute]
                #fresh_context_names = [x.target_context_name for x in fresh_single_context_set_expressions]
                assert all([x.fresh for x in fresh_single_context_set_expressions])
                #persistent_single_context_set_expressions = []
                #for context_proxy in self.score_specification.context_proxies.itervalues():
                #    set_expressions = context_proxy.single_context_set_expressions_by_attribute.get(attribute, [])
                #    persistent_single_context_set_expressions.extend(set_expressions)
                #assert all([x.persist for x in persistent_single_context_set_expressions])
                set_expressions_to_store = fresh_single_context_set_expressions
                #for persistent_single_context_set_expression in persistent_single_context_set_expressions[:]:
                #    if persistent_single_context_set_expression.target_context_name not in fresh_context_names:
                #        set_expression_to_store = persistent_single_context_set_expression.copy_and_set_root(
                #            segment_specification.segment_name)
                #        set_expressions_to_store.append(set_expression_to_store)
                for set_expression_to_store in set_expressions_to_store:
                    set_expression_to_store.store_in_segment_by_context_and_attribute()
                    if set_expression_to_store.persist:
                        target_context_name = set_expression_to_store.target_context_name
                        expressions = persistent_single_context_set_expressions_by_context[
                            target_context_name].single_context_set_expressions_by_attribute[attribute]
                        # TODO: maybe also hash expressions by timespan?
                        for expression in expressions[:]:
                            if expression.target_timespan == set_expression_to_store.target_timespan:
                                expressions.remove(expression)
                        expressions.append(set_expression_to_store)

    def evaluate_multiple_context_set_expressions(self):
        for multiple_context_set_expression in self.score_specification.multiple_context_set_expressions:
            attribute = multiple_context_set_expression.attribute
            fresh_single_context_set_expressions = multiple_context_set_expression.evaluate()
            assert all([x.fresh for x in fresh_single_context_set_expressions])
            if multiple_context_set_expression.is_segment_rooted:
                root_segment_specification = multiple_context_set_expression.root_segment_specification
                root_segment_specification.fresh_single_context_set_expressions_by_attribute[
                    attribute].extend(fresh_single_context_set_expressions)
                self.score_specification.fresh_single_context_set_expressions_by_attribute[
                    attribute].extend(fresh_single_context_set_expressions)
            #if multiple_context_set_expression.is_segment_rooted:
            #    root_segment_specification = multiple_context_set_expression.root_segment_specification
            #    root_segment_specification.fresh_single_context_set_expressions_by_attribute.[
            #         attribute].extend(fresh_single_context_set_expressions)
            for fresh_single_context_set_expression in fresh_single_context_set_expressions:
                if fresh_single_context_set_expression.is_score_rooted:
                    target_context_name = fresh_single_context_set_expression.target_context_name
                    attribute = fresh_single_context_set_expression.attribute
                    self.score_specification.score_rooted_single_context_set_expressions_by_context[
                        target_context_name].single_context_set_expressions_by_attribute[
                        attribute].append(fresh_single_context_set_expression)
                
    def instantiate_score(self):
        score = self.score_specification.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        score.insert(0, context)
        return score
