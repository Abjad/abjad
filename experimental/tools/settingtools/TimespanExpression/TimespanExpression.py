from experimental.tools.settingtools.AnchoredExpression import AnchoredExpression
from experimental.tools.settingtools.SetMethodMixin import SetMethodMixin
from experimental.tools.settingtools.SelectMethodMixin import SelectMethodMixin
from experimental.tools.settingtools.TimespanCallbackMixin import TimespanCallbackMixin


class TimespanExpression(AnchoredExpression, TimespanCallbackMixin, SelectMethodMixin, SetMethodMixin):
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

    def __init__(self, anchor=None, callbacks=None):
        from experimental.tools import settingtools
        AnchoredExpression.__init__(self, anchor=anchor)
        TimespanCallbackMixin.__init__(self, callbacks=callbacks)

    ### SPECIAL METHODS ###

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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = AnchoredExpression._keyword_argument_name_value_strings.fget(self)
        if 'callbacks=CallbackInventory([])' in result:
            result = list(result)
            result.remove('callbacks=CallbackInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification, context_name):
        '''Evaluate timespan expression when 
        applied to `context_name` in `score_specification`.

        Return pair.
        '''
        anchor_timespan = score_specification.get_anchor_timespan(self, context_name)
        timespan = self._apply_callbacks(anchor_timespan)
        return timespan

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty callback inventory.
        '''
        filtered_result = []
        result = AnchoredExpression._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'callbacks=settingtools.CallbackInventory([])' in string:
                filtered_result.append(string)
        return filtered_result
