from abjad.tools import chordtools
from abjad.tools import notetools
from experimental.tools.specificationtools.GeneralizedSetExpression import GeneralizedSetExpression


class PitchClassTransformSetExpression(GeneralizedSetExpression):
    '''Pitch-class transform set expression.
    '''

    ### INTIALIZER ###

    def __init__(self, source_expression=None, target_select_expression_inventory=None):
        GeneralizedSetExpression.__init__(self, attribute='pitch_class_transform',
            source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory)

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute pitch-class transform expression against `score`.
        '''
        from experimental.tools import specificationtools
        pitch_class_transform_expression = self.source_expression.payload
        leaves = []
        for target_select_expression in self.target_select_expression_inventory:
            iterable_payload_expression = target_select_expression.evaluate_against_score(score)
            leaves.extend(iterable_payload_expression.payload)
        for leaf in leaves:
            assert isinstance(leaf, (notetools.Note, chordtools.Chord)), repr(leaf)
            if isinstance(leaf, notetools.Note):
                sounding_pitch_number = abs(leaf.sounding_pitch)
                transformed_pitch_class = pitch_class_transform_expression(sounding_pitch_number)
                leaf.sounding_pitch = transformed_pitch_class
            elif isinstance(leaf, chordtools.Chord):
                transformed_pitch_classes = []
                for sounding_pitch_number in leaf.sounding_pitches:
                    sounding_pitch_number = abs(leaf.sounding_pitch)
                    transformed_pitch_class = pitch_class_transform_expression(sounding_pitch_number)
                    transformed_pitch_classes.append(transformed_pitch_class)
                    leaf[:] = transformed_pitch_classes
            else:
                raise TypeError(leaf)
