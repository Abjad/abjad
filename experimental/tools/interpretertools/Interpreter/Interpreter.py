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
        self.evaluate_multiple_context_set_expressions_for_score()
        self.store_interpreter_specific_single_context_set_expressions_by_context()
        
    ### PUBLIC METHODS ###

    def evaluate_multiple_context_set_expressions_for_score(self):
        for multiple_context_set_expression in self.score_specification.multiple_context_set_expressions:
            single_context_set_expressions = multiple_context_set_expression.evaluate()
            segment_specification = multiple_context_set_expression.start_segment_specification
            segment_specification.single_context_set_expressions.extend(single_context_set_expressions)
            self.score_specification.single_context_set_expressions.extend(single_context_set_expressions)

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
            #self._debug(segment_specification, 'SEG')
            new_set_expressions = segment_specification.single_context_set_expressions.get_set_expressions(
            attribute=attribute)
            existing_set_expressions = \
                self.score_specification.context_proxies.get_set_expressions(
                attribute=attribute)
            new_context_names = [x.target_context_name for x in new_set_expressions]
            forwarded_existing_set_expressions = []
            for existing_set_expression in existing_set_expressions[:]:
                # TODO: stop copying score-rooted set expressions
                if existing_set_expression.is_score_rooted:
                    continue
                if existing_set_expression.target_context_name in new_context_names:
                    existing_set_expressions.remove(existing_set_expression)
                else:
                    forwarded_existing_set_expression = \
                        existing_set_expression.copy_set_expression_to_segment_name(
                        segment_specification.segment_name)
                    #if not forwarded_existing_set_expression == 'score-anchored expression':
                    #    forwarded_existing_set_expressions.append(forwarded_existing_set_expression)
                    forwarded_existing_set_expressions.append(forwarded_existing_set_expression)
            set_expressions_to_store = new_set_expressions + forwarded_existing_set_expressions
            #self._debug_values(set_expressions_to_store, 'sxts', blank=True)
            self.store_single_context_set_expressions_by_context(
                set_expressions_to_store, clear_persistent_first=True)

    def store_single_context_set_expression_by_context(self, single_context_set_expression, 
        clear_persistent_first=False):
        '''Copy single-context set expression.

        Find single-context set expression start segment.

        Store copied single-context set expression by context in start segment.

        If set expression persists then store set expression by context in score, too.
        '''
        single_context_set_expression = copy.deepcopy(single_context_set_expression)
        segment_specification = single_context_set_expression.start_segment_specification
        assert segment_specification is not None
        context_name = single_context_set_expression.target_context_name
        if context_name is None:
            context_name = segment_specification.context_proxies.score_name
        attribute = single_context_set_expression.attribute
        if clear_persistent_first:
            self.score_specification.clear_persistent_single_context_set_expressions_by_context(
                context_name, attribute)
        if attribute in segment_specification.context_proxies[
            context_name].single_context_set_expressions_by_attribute:
            segment_specification.context_proxies[
                context_name].single_context_set_expressions_by_attribute[attribute].append(
                single_context_set_expression)
        else:
            segment_specification.context_proxies[
                context_name].single_context_set_expressions_by_attribute[attribute] = [
                single_context_set_expression]
        if single_context_set_expression.persist:
            if attribute in self.score_specification.context_proxies[
                context_name].single_context_set_expressions_by_attribute:
                self.score_specification.context_proxies[
                    context_name].single_context_set_expressions_by_attribute[attribute].append(
                    single_context_set_expression)
            else:
                self.score_specification.context_proxies[
                    context_name].single_context_set_expressions_by_attribute[attribute] = [
                    single_context_set_expression]

    def store_single_context_set_expressions_by_context(self, 
        single_context_set_expressions, clear_persistent_first=False):
        if single_context_set_expressions:
            self.store_single_context_set_expression_by_context(
                single_context_set_expressions[0], clear_persistent_first=clear_persistent_first)
            for single_context_set_expression in single_context_set_expressions[1:]:
                self.store_single_context_set_expression_by_context(
                    single_context_set_expression, clear_persistent_first=False)
