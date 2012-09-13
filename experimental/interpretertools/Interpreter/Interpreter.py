from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Interpreter(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract interpreter class from which conrete interpreters inherit.
    ''' 

    ### SPECIAL METHODS ###

    def __call__(self, score_specification):
        '''Top-level interpretation entry point.
        
        Write custom interpreter code by extending this method.
        '''
        self.score_specification = score_specification
        self.score = self.instantiate_score()
        self.unpack_multiple_context_settings_for_score()
        
    ### PUBLIC METHODS ###

    def instantiate_score(self):
        score = self.score_specification.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        score.insert(0, context)
        return score

    def unpack_multiple_context_settings_for_score(self):
        for segment_specification in self.score_specification.segment_specifications:
            settings = self.unpack_multiple_context_settings_for_segment(segment_specification)
            self.score_specification.single_context_settings.extend(settings)

    def unpack_multiple_context_settings_for_segment(self, segment_specification):
        for multiple_context_setting in segment_specification.multiple_context_settings:
            segment_specification.single_context_settings.extend(multiple_context_setting.unpack())
        return segment_specification.single_context_settings
