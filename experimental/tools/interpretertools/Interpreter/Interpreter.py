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
        self.unpack_multiple_context_settings_for_score()
        self.store_interpreter_specific_single_context_set_expressions_by_context()
        
    ### PUBLIC METHODS ###

    def instantiate_score(self):
        score = self.score_specification.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        score.insert(0, context)
        return score

    @abc.abstractmethod
    def store_interpreter_specific_single_context_set_expressions_by_context(self):
        pass

    def store_single_context_attribute_settings_by_context(self, attribute):
        for segment_specification in self.score_specification.segment_specifications:
            new_settings = segment_specification.single_context_set_expressions.get_settings(attribute=attribute)
            existing_settings = \
                self.score_specification.single_context_set_expressions_by_context.get_settings(
                attribute=attribute)
            new_context_names = [x.context_name for x in new_settings]
            forwarded_existing_settings = []
            for existing_setting in existing_settings[:]:
                if existing_setting.context_name in new_context_names:
                    existing_settings.remove(existing_setting)
                else:
                    forwarded_existing_setting = existing_setting.copy_setting_to_segment_name(
                        segment_specification.segment_name)
                    forwarded_existing_settings.append(forwarded_existing_setting)
            settings_to_store = new_settings + forwarded_existing_settings
            self.store_single_context_set_expressions_by_context(settings_to_store, clear_persistent_first=True)

    def store_single_context_set_expression_by_context(self, single_context_set_expression, clear_persistent_first=False):
        '''Copy single-context setting.

        Find single-context setting start segment.

        Store copied single-context setting by context in start segment.

        If setting persists then store setting by context in score, too.
        '''
        single_context_set_expression = copy.deepcopy(single_context_set_expression)
        anchor = single_context_set_expression.anchor
        segment_specification = self.score_specification.get_start_segment_specification(anchor)
        assert segment_specification is not None
        context_name = single_context_set_expression.context_name
        if context_name is None:
            context_name = segment_specification.single_context_set_expressions_by_context.score_name
        attribute = single_context_set_expression.attribute
        if clear_persistent_first:
            self.score_specification.clear_persistent_single_context_set_expressions_by_context(
                context_name, attribute)
        if attribute in segment_specification.single_context_set_expressions_by_context[context_name]:
            segment_specification.single_context_set_expressions_by_context[context_name][attribute].append(
                single_context_set_expression)
        else:
            segment_specification.single_context_set_expressions_by_context[context_name][attribute] = [
                single_context_set_expression]
        if single_context_set_expression.persist:
            if attribute in self.score_specification.single_context_set_expressions_by_context[context_name]:
                self.score_specification.single_context_set_expressions_by_context[context_name][attribute].append(
                    single_context_set_expression)
            else:
                self.score_specification.single_context_set_expressions_by_context[context_name][attribute] = [
                    single_context_set_expression]

    def store_single_context_set_expressions_by_context(self, single_context_set_expressions, clear_persistent_first=False):
        if single_context_set_expressions:
            self.store_single_context_set_expression_by_context(
                single_context_set_expressions[0], clear_persistent_first=clear_persistent_first)
            for single_context_set_expression in single_context_set_expressions[1:]:
                self.store_single_context_set_expression_by_context(
                    single_context_set_expression, clear_persistent_first=False)

    def unpack_multiple_context_settings_for_score(self):
        for multiple_context_setting in self.score_specification.multiple_context_settings:
            segment_specification = self.score_specification.get_start_segment_specification(
                multiple_context_setting.anchor)
            single_context_set_expressions = multiple_context_setting.evaluate()
            segment_specification.single_context_set_expressions.extend(single_context_set_expressions)
            self.score_specification.single_context_set_expressions.extend(single_context_set_expressions)
