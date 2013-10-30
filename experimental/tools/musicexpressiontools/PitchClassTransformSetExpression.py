# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class PitchClassTransformSetExpression(LeafSetExpression):
    r'''Pitch-class transform set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute pitch-class transform expression against `score`.
        '''
        pitch_class_transform_expression = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            assert isinstance(leaf, (scoretools.Note, scoretools.Chord))
            if isinstance(leaf, scoretools.Note):
                sounding_pitch_number = abs(leaf.sounding_pitch)
                transformed_pitch_class = \
                    pitch_class_transform_expression(sounding_pitch_number)
                leaf.sounding_pitch = transformed_pitch_class
            elif isinstance(leaf, scoretools.Chord):
                transformed_pitch_classes = []
                for sounding_pitch_number in leaf.sounding_pitches:
                    sounding_pitch_number = abs(leaf.sounding_pitch)
                    transformed_pitch_class = \
                        pitch_class_transform_expression(sounding_pitch_number)
                    transformed_pitch_classes.append(transformed_pitch_class)
                    leaf[:] = transformed_pitch_classes
            else:
                raise TypeError(leaf)
