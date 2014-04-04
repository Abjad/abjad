# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.musicexpressiontools.AttributeNameEnumeration \
    import AttributeNameEnumeration


class Interpreter(AbjadObject):
    r'''Interpreter.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta
    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self):
        self._callback_cache = {}

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, score_specification):
        self.score_specification = score_specification
        self.score = self.instantiate_score()
        self.evaluate_multiple_context_set_expressions()
        self.store_score_rooted_single_context_set_expressions_by_context()
        self.store_segment_rooted_single_context_set_expressions_by_context()

    ### PUBLIC PROPERTIES ###

    @property
    def callback_cache(self):
        return self._callback_cache

    ### PUBLIC METHODS ###

    def evaluate_multiple_context_set_expressions(self):
        for multiple_context_set_expression in \
            self.score_specification.multiple_context_set_expressions:
            multiple_context_set_expression.evaluate_and_store_in_root_specification()

    def instantiate_score(self):
        score = self.score_specification.score_template()
        context = scoretools.Context(
            name='TimeSignatureContext',
            context_name='TimeSignatureContext',
            )
        score.insert(0, context)
        return score

    def store_score_rooted_single_context_set_expressions_by_context(self):
        for fresh_single_context_set_expression in \
            self.score_specification.fresh_single_context_set_expressions:
            fresh_single_context_set_expression.store_in_root_specification_by_context_and_attribute()

    def store_segment_rooted_single_context_set_expressions_by_context(self):
        from experimental.tools import musicexpressiontools
        score = self.score_specification.score_template()
        persistent_single_context_set_expressions_by_context = \
            musicexpressiontools.ContextDictionary(score)
        for segment_specification in \
            self.score_specification.segment_specifications:
            # get persistent single-context set expressions
            persistent_single_context_set_expressions = []
            for context_proxy in \
                persistent_single_context_set_expressions_by_context.itervalues():
                for attribute, settings in \
                    context_proxy.single_context_set_expressions_by_attribute.items():
                    persistent_single_context_set_expressions.extend(settings)
            # store persistent single-context set expressions in current segment specification
            for persistent_single_context_set_expression in \
                persistent_single_context_set_expressions:
                persistent_single_context_set_expression = \
                    persistent_single_context_set_expression._copy_and_set_root_specification(
                    segment_specification.segment_name)
                persistent_single_context_set_expression.store_in_root_specification_by_context_and_attribute()
            # store fresh single-context-set expressions in current segment specification
            for fresh_single_context_set_expression in \
                segment_specification.fresh_single_context_set_expressions:
                fresh_single_context_set_expression.store_in_root_specification_by_context_and_attribute()
                if fresh_single_context_set_expression.persist:
                    scope_name = \
                        fresh_single_context_set_expression.scope_name
                    attribute = fresh_single_context_set_expression.attribute
                    expressions = \
                        persistent_single_context_set_expressions_by_context[
                        scope_name].single_context_set_expressions_by_attribute[attribute]
                    for expression in expressions[:]:
                        if expression.target_timespan == \
                            fresh_single_context_set_expression.target_timespan:
                            expressions.remove(expression)
                    expressions.append(fresh_single_context_set_expression)