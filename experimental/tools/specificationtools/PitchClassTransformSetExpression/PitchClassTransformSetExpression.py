from abjad.tools import chordtools
from abjad.tools import notetools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class PitchClassTransformSetExpression(LeafSetExpression):
    '''Pitch-class transform set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute pitch-class transform expression against `score`.
        '''
        pitch_class_transform_expression = self.source_expression.payload
        for leaf in self._iterate_leaves_in_score(score):
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
