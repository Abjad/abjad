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
        self.store_interpreter_specific_single_context_set_expressions_by_context()
        
    ### PUBLIC METHODS ###

    def evaluate_multiple_context_set_expressions(self):
        for multiple_context_set_expression in self.score_specification.multiple_context_set_expressions:
            attribute = multiple_context_set_expression.attribute
            fresh_single_context_set_expressions_by_attribute = multiple_context_set_expression.evaluate()
            assert all([x.fresh for x in fresh_single_context_set_expressions_by_attribute])
            root_segment_specification = multiple_context_set_expression.root_segment_specification
            root_segment_specification.fresh_single_context_set_expressions_by_attribute[
                attribute].extend(fresh_single_context_set_expressions_by_attribute)
            self.score_specification.fresh_single_context_set_expressions_by_attribute[
                attribute].extend(fresh_single_context_set_expressions_by_attribute)
            #if multiple_context_set_expression.is_segment_rooted:
            #    root_segment_specification = multiple_context_set_expression.root_segment_specification
            #    root_segment_specification.fresh_single_context_set_expressions_by_attribute.[
            #         attribute].extend(fresh_single_context_set_expressions_by_attribute)
                
    def instantiate_score(self):
        score = self.score_specification.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        score.insert(0, context)
        return score

    @abc.abstractmethod
    def store_interpreter_specific_single_context_set_expressions_by_context(self):
        pass

    def store_single_context_attribute_set_expressions_by_context(self, attribute):
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
            self.store_single_context_set_expressions_by_context(
                set_expressions_to_store, clear_persistent_first=True)

    # TODO: migrate to SingleContextSetExpression
    def store_single_context_set_expression_by_context(self, single_context_set_expression, 
        clear_persistent_first=False):
        '''Copy single-context set expression.

        Find single-context set expression root segment specification.

        Store copied single-context set expression by context in root segment specification.

        If set expression persists then store set expression by context in score specification, too.
        '''
        single_context_set_expression = copy.deepcopy(single_context_set_expression)
        root_segment_specification = single_context_set_expression.root_segment_specification
        # TODO: this will have to be extended to handle score-rooted expressions
        assert root_segment_specification is not None
        target_context_name = single_context_set_expression.target_context_name
        if target_context_name is None:
            target_context_name = root_segment_specification.context_proxies.score_name
        attribute = single_context_set_expression.attribute
        if clear_persistent_first:
            self.score_specification.clear_persistent_single_context_set_expressions_by_context(
                attribute, target_context_name)
        root_segment_specification.context_proxies[
            target_context_name].single_context_set_expressions_by_attribute[attribute].append(
            single_context_set_expression)
        if single_context_set_expression.persist:
            self.score_specification.context_proxies[
                target_context_name].single_context_set_expressions_by_attribute[attribute].append(
                single_context_set_expression)

    def store_single_context_set_expressions_by_context(self, single_context_set_expressions, 
        clear_persistent_first=False):
        if single_context_set_expressions:
            self.store_single_context_set_expression_by_context(
                single_context_set_expressions[0], clear_persistent_first=clear_persistent_first)
            for single_context_set_expression in single_context_set_expressions[1:]:
                self.store_single_context_set_expression_by_context(
                    single_context_set_expression, clear_persistent_first=False)
