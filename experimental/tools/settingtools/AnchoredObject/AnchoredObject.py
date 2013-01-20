import abc
import copy
from abjad.tools.abctools import AbjadObject


class AnchoredObject(AbjadObject):
    '''Anchored object.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, anchor=None):
        from experimental.tools import settingtools
        # TODO: eventually assert anchor is AnchoredExpression and not just unqualified Expression
        assert isinstance(anchor, (settingtools.Expression, str, type(None))), repr(anchor)
        self._anchor = anchor
        self._score_specification = None

    ### PRIVATE METHODS ###

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
    def start_segment_identifier(self):
        '''Return anchor when anchor is a string.

        Otherwise return anchor start-segment identifier.

        Return string name of segment.
        '''
        if isinstance(self.anchor, str):
            return self.anchor
        else:
            return self.anchor.start_segment_identifier
