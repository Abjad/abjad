import abc
import copy
from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Interpreter(AbjadObject):
    r'''

    Abstract interpreter class from which conrete interpreters inherit.
    ''' 

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, score_specification):
        '''Top-level interpretation entry point.
        
        Write custom interpreter code by extending this method.
        '''
        self.score_specification = score_specification
        self.score = self.instantiate_score()
        self.evaluate_multiple_context_set_expressions()
        self.store_single_context_set_expressions_by_segment_context_and_attribute()
        
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

    def store_single_context_set_expressions_by_segment_context_and_attribute(self):
        self.store_attribute_specified_single_context_set_expressions_by_segment_context_and_attribute('time_signatures')
        self.store_attribute_specified_single_context_set_expressions_by_segment_context_and_attribute('divisions')
        self.store_attribute_specified_single_context_set_expressions_by_segment_context_and_attribute('rhythm')
        self.store_attribute_specified_single_context_set_expressions_by_segment_context_and_attribute('pitch_classes')
        self.store_attribute_specified_single_context_set_expressions_by_segment_context_and_attribute('registration')

    def store_attribute_specified_single_context_set_expressions_by_segment_context_and_attribute(self, attribute):
        for segment_specification in self.score_specification.segment_specifications:
            fresh_set_expressions = \
                segment_specification.fresh_single_context_set_expressions_by_attribute[attribute]
            assert all([x.fresh for x in fresh_set_expressions])
            existing_set_expressions = []
            for context_proxy in self.score_specification.context_proxies.itervalues():
                existing_set_expressions.extend(
                    context_proxy.single_context_set_expressions_by_attribute.get(attribute, []))
            new_context_names = [x.target_context_name for x in fresh_set_expressions]
            holdover_set_expressions = []
            for existing_set_expression in existing_set_expressions[:]:
                if existing_set_expression.is_score_rooted:
                    continue
                if existing_set_expression.target_context_name in new_context_names:
                    existing_set_expressions.remove(existing_set_expression)
                else:
                    holdover_set_expression = \
                        existing_set_expression.copy_and_set_root(segment_specification.segment_name)
                    holdover_set_expressions.append(holdover_set_expression)
            assert all([not x.fresh for x in holdover_set_expressions])
            set_expressions_to_store = fresh_set_expressions + holdover_set_expressions
            if set_expressions_to_store:
                set_expressions_to_store[0].store_by_segment_context_and_attribute(clear_persistent_first=True)
                for set_expression_to_store in set_expressions_to_store[1:]:
                    set_expression_to_store.store_by_segment_context_and_attribute(clear_persistent_first=False)
