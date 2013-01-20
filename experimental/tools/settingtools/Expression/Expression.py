import abc
import copy
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    '''Expression base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, anchor=None):
        from experimental.tools import settingtools
        assert isinstance(anchor, (settingtools.Expression, str, type(None))), repr(anchor)
        self._anchor = anchor
        self._score_specification = None

    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        '''Expression deepcopy preserves score specification.
        '''
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _anchor_abbreviation(self):
        '''Form of expression suitable for inclusion in storage format.
        '''
        return self

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _evaluate(self):
        pass

    def _set_start_segment_identifier(self, segment_identifier):
        assert isinstance(segment_identifier, str)
        if isinstance(self.anchor, str):
            self._anchor = segment_identifier
        else:
            anchor = copy.deepcopy(self.anchor)
            anchor._set_start_segment_identifier(segment_identifier)
            self._anchor = anchor

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        '''Expression anchor.

        Every expression is anchored to something.

        Expressions may be anchored to the entire score,
        to a single segment, or to another expression.

        This ability of an expression to be anchored
        to another expression is primary source of
        recursion in the model.

        Return none when expression is anchored to the entire score.

        Return string name of segment when expression is anchored to a single segment.

        Return expression when expression is anchored to another expression.
        '''
        return self._anchor

    @property
    def score_specification(self):
        '''Expression score specification.

        Return reference to score specification object.
        '''
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

        Otherwise return anchor start-segment identifier.

        Return string name of segment.
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
