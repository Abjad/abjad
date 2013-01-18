from abjad.tools.timespantools.Timespan import Timespan
from experimental.tools.settingtools.SetMethodMixin import SetMethodMixin
from experimental.tools.settingtools.SelectMethodMixin import SelectMethodMixin
from experimental.tools.settingtools.TimespanCallbackMixin import TimespanCallbackMixin


# TODO: looks like maybe TimespanExpression needs to *have a* timespan istead of *being a* timespan
class TimespanExpression(TimespanCallbackMixin, SelectMethodMixin, SetMethodMixin, Timespan):
    r'''Timespan expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> setting = red_segment.set_time_signatures([(4, 8), (3, 8)])
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> setting = blue_segment.set_time_signatures([(9, 16), (3, 16)])

    The examples below refer to the score and segment specifications defined above.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, timespan_callbacks=None):
        from experimental.tools import settingtools
        Timespan.__init__(self)
        TimespanCallbackMixin.__init__(self)
        assert isinstance(anchor, (str, type(None))), repr(anchor)
        self._anchor = anchor
        timespan_callbacks = timespan_callbacks or []
        self._timespan_callbacks = settingtools.CallbackInventory(timespan_callbacks)

    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        return result

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

            >>> red_segment.timespan == red_segment.timespan
            True

        Otherwise false::

            >>> red_segment.timespan == blue_segment.timespan
            False

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _anchor_abbreviation(self):
        '''Form of timespan expression suitable for writing to disk.
        '''
        return self

    @property
    def _keyword_argument_name_value_strings(self):
        result = Timespan._keyword_argument_name_value_strings.fget(self)
        if 'timespan_callbacks=CallbackInventory([])' in result:
            result = list(result)
            result.remove('timespan_callbacks=CallbackInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _get_timespan(self, score_specification, context_name):
        '''Evaluate timespan expression when 
        applied to `context_name` in `score_specification`.

        Return pair.
        '''
        anchor_timespan = score_specification.get_anchor_timespan(self, context_name)
        timespan = self._apply_timespan_callbacks(anchor_timespan)
        return timespan

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty offset payload_callbacks list.
        '''
        filtered_result = []
        result = Timespan._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'timespan_callbacks=settingtools.CallbackInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

    def _set_start_segment_identifier(self, segment_identifier):
        self._anchor = segment_identifier

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        return self._anchor

    @property
    def score_specification(self):
        return self._score_specification

    @property
    def start_offset(self):
        '''Timespan expression start offset.

        Return offset expression.
        '''            
        from experimental.tools import settingtools
        return settingtools.OffsetExpression(anchor=self)

    @property
    def start_segment_identifier(self):
        if isinstance(self.anchor, str):
            return self.anchor
        else:
            return self.anchor.start_segment_identifier

    @property
    def stop_offset(self):
        '''Timespan expression stop offset.

        Return offset expression.
        '''            
        from experimental.tools import settingtools
        return settingtools.OffsetExpression(anchor=self)
