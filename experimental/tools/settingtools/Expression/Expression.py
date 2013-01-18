import copy
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    '''Expression base class.
    '''

    ### INITIALIZER ###

    def __init__(self):
        self._score_specification = None

    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _anchor_abbreviation(self):
        '''Form of expression suitable for writing to disk.
        '''
        return self

    ### PRIVATE METHODS ###

    def _set_start_segment_identifier(self, segment_identifier):
        assert isinstance(segment_identifier, str)
        if isinstance(self.anchor, str):
            self._anchor = segment_identifier
        else:
            #self.anchor._set_start_segment_identifier(segment_identifier)
            anchor = copy.deepcopy(self.anchor)
            anchor._set_start_segment_identifier(segment_identifier)
            self._anchor = anchor

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        return self._anchor

    @property
    def score_specification(self):
        return self._score_specification

    @property
    def start_offset(self):
        '''Expression start offset.

        Return offset expression.
        '''
        from experimental.tools import settingtools
        result = settingtools.OffsetExpression(anchor=self._anchor_abbreviation)
        result._score_specification = self.score_specification
        return result

    @property
    def start_segment_identifier(self):
        '''Return anchor when anchor is a string.

        Otherwise delegate to anchor start-segment identifier.

        Return string or none.
        '''
        if isinstance(self.anchor, str):
            return self.anchor
        else:
            return self.anchor.start_segment_identifier

    @property
    def stop_offset(self):
        '''Expression stop offset.

        Return offset expression.
        '''
        from experimental.tools import settingtools
        result = settingtools.OffsetExpression(anchor=self._anchor_abbreviation, edge=Right)
        result._score_specification = self.score_specification
        return result
