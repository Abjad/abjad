import copy
from abjad.tools import timespantools
from experimental.tools.expressiontools.Expression import Expression


class AnchoredExpression(Expression):
    '''Anchored expression.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None):
        from experimental.tools import expressiontools
        assert isinstance(anchor, (expressiontools.AnchoredExpression, str, type(None))), repr(anchor)
        self._anchor = anchor
        self._score_specification = None

    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        '''Remove score specification and then reattach score specification.
        '''
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        if hasattr(self, '_lexical_rank'):
            result._lexical_rank = self._lexical_rank
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _expression_abbreviation(self):
        '''Form of anchored expression suitable for inclusion in storage format.
        '''
        return self

    ### PRIVATE METHODS ###

    def _evaluate_anchor_timespan(self):
        '''Evaluate anchor timespan.

        Return timespan when anchor timespan is evaluable.

        Return none when anchor timespan is nonevaluable.
        '''
        if isinstance(self.anchor, str):
            return self.root_specification.timespan
        elif self.anchor is None:
            return self.root_specification.timespan
        expression = self.anchor.evaluate()
        if expression is None:
            return
        if hasattr(expression, 'timespan'):
            return expression.timespan
        elif isinstance(expression.payload[0], timespantools.Timespan):
            return expression.payload[0]
        else:
            raise TypeError(expression)

    def _set_root_specification(self, root_specification_identifier):
        assert isinstance(root_specification_identifier, (str, type(None)))
        if isinstance(self.anchor, (str, type(None))):
            self._anchor = root_specification_identifier
        else:
            anchor = copy.deepcopy(self.anchor)
            anchor._set_root_specification(root_specification_identifier)
            self._anchor = anchor

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        '''Anchored expression anchor.

        Return none when anchored expression anchors to the entire score.

        Return string name of segment when anchored expression anchors to a single segment.

        Return expression when anchored expression anchors to another expression.
        '''
        return self._anchor

    @property
    def is_score_rooted(self):
        '''True when anchored expression is score-rooted.
        Otherwise false.

        Return boolean.
        '''
        return self.root_specification_identifier is None

    @property
    def is_segment_rooted(self):
        '''True when anchored expression is segment-rooted.
        Otherwise false.

        Return boolean.
        '''
        return isinstance(self.root_specification_identifier, str)

    @property
    def root_specification_identifier(self):
        '''Anchored expression root identifier.

        Segment-rooted expressions return string.

        Score-rooted expressions return none.
        '''
        if isinstance(self.anchor, (str, type(None))):
            return self.anchor
        else:
            return self.anchor.root_specification_identifier
        
    @property
    def root_specification(self):
        '''Anchored expression root specification.

        Return specification.
        '''
        if self.is_segment_rooted:
            return self.score_specification.segment_specifications[self.root_specification_identifier]
        else:
            return self.score_specification

    @property
    def score_specification(self):
        '''Anchored expression score specification.

        Return score specification.
        '''
        return self._score_specification

    @property
    def start_offset(self):
        '''Anchored expression start offset.

        Return offset expression.
        '''
        from experimental.tools import expressiontools
        result = expressiontools.OffsetExpression(anchor=self._expression_abbreviation)
        result._score_specification = self.score_specification
        return result

    @property
    def stop_offset(self):
        '''Anchored expression stop offset.

        Return offset expression.
        '''
        from experimental.tools import expressiontools
        result = expressiontools.OffsetExpression(anchor=self._expression_abbreviation, edge=Right)
        result._score_specification = self.score_specification
        return result
