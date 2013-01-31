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
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _expression_abbreviation(self):
        '''Form of anchored expression suitable for inclusion in storage format.
        '''
        return self

    ### PRIVATE METHODS ###

    # TODO: change name to self._set_root(root_identifier)
    def _set_root(self, root):
        assert isinstance(root, (str, type(None)))
        if isinstance(self.anchor, (str, type(None))):
            self._anchor = root
        else:
            anchor = copy.deepcopy(self.anchor)
            anchor._set_root(root)
            self._anchor = anchor

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        '''Expression anchor.

        Anchored expressions may be anchored to the entire score,
        to a single segment, or to another expression.

        This ability of an anchored expression to be anchored
        to another expression is primary source of recursion 
        in the model.

        Return none when anchored expression is anchored to the entire score.

        Return string name of segment when anchored expression is anchored to a single segment.

        Return expression when anchored expression is anchored to another expression.
        '''
        return self._anchor

    @property
    def is_score_rooted(self):
        '''True when anchored expression is score-rooted.
        Otherwise false.

        Return boolean.
        '''
        return self.root is None

    @property
    def is_segment_rooted(self):
        '''True when anchored expression is segment-rooted.
        Otherwise false.

        Return boolean.
        '''
        return isinstance(self.root, str)

    @property
    def root(self):
        '''Anchored expression root.

        Segment-rooted expressions return string.

        Score-rooted expressions return none.
        '''
        if isinstance(self.anchor, (str, type(None))):
            return self.anchor
        else:
            return self.anchor.root
        
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
        from experimental.tools import expressiontools
        result = expressiontools.OffsetExpression(anchor=self._expression_abbreviation)
        result._score_specification = self.score_specification
        return result

    # NEXT TODO: rename and rework this concept to apply to segment-root expressions only
    @property
    def start_segment_identifier(self):
        '''Return anchor when anchor is a string.

        Otherwise return anchor start-segment identifier.

        Return string name of segment.
        '''
        if isinstance(self.anchor, str):
            return self.anchor
        # NEXT TODO: do not return value for score-rooted expression
        elif self.anchor is None:
            return self.score_specification.segment_specifications[0].segment_name
        else:
            return self.anchor.start_segment_identifier

    @property
    def start_segment_specification(self):
        '''Start segment specification.
        '''
        if self.start_segment_identifier is not None:
            return self.score_specification.segment_specifications[self.start_segment_identifier]

    @property
    def stop_offset(self):
        '''Expression stop offset.

        Return offset expression.
        '''
        from experimental.tools import expressiontools
        result = expressiontools.OffsetExpression(anchor=self._expression_abbreviation, edge=Right)
        result._score_specification = self.score_specification
        return result

    ### PUBLIC METHODS ###

    def evaluate_anchor_timespan(self):
        '''Evaluate anchor timespan.

        Return timespan.
        '''
        from experimental.tools import expressiontools
        if isinstance(self.anchor, str):
            return self.score_specification.segment_specifications[self.anchor].timespan
        elif self.anchor is None:
            return self.score_specification.timespan
        expression = self.anchor.evaluate()
        if expression is None:
            return
        if hasattr(expression, 'timespan'):
            return expression.timespan
        elif isinstance(expression.payload[0], timespantools.Timespan):
            return expression.payload[0]
        else:
            raise TypeError(expression)
