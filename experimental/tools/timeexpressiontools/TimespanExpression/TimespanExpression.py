import copy
from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import timespantools
from abjad.tools.timespantools.Timespan import Timespan
from experimental.tools.settingtools.SetMethodMixin import SetMethodMixin
from experimental.tools.timeexpressiontools.SelectMethodMixin import SelectMethodMixin


class TimespanExpression(Timespan, SelectMethodMixin, SetMethodMixin):
    r'''Timespan expression.

    ::
        
        >>> from experimental.tools import *

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

    def __init__(self, anchor=None, timespan_modifiers=None):
        from experimental.tools import settingtools
        Timespan.__init__(self)
        assert isinstance(anchor, (str, type(None))), repr(anchor)
        self._anchor = anchor
        timespan_modifiers = timespan_modifiers or []
        self._timespan_modifiers = settingtools.ModifierInventory(timespan_modifiers)

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
        '''Form of time expression suitable for writing to disk.
        '''
        return self

    @property
    def _keyword_argument_name_value_strings(self):
        result = Timespan._keyword_argument_name_value_strings.fget(self)
        if 'timespan_modifiers=ModifierInventory([])' in result:
            result = list(result)
            result.remove('timespan_modifiers=ModifierInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _apply_timespan_modifiers(self, timespan):
        assert isinstance(timespan, timespantools.Timespan)
        start_offset, stop_offset = timespan.offsets
        evaluation_context = {
            'self': self,
            'Duration': durationtools.Duration,
            'Multiplier': durationtools.Multiplier,
            'Offset': durationtools.Offset,
            }
        for timespan_modifier in self.timespan_modifiers:
            timespan_modifier = timespan_modifier.replace('original_start_offset', repr(start_offset))
            timespan_modifier = timespan_modifier.replace('original_stop_offset', repr(stop_offset))
            start_offset, stop_offset = eval(timespan_modifier, evaluation_context)
            assert start_offset <= stop_offset
        return timespantools.Timespan(start_offset, stop_offset)
        
    def _divide_by_ratio(self, start_offset, stop_offset, ratio, the_part):
        original_start_offset, original_stop_offset = start_offset, stop_offset
        original_duration = original_stop_offset - original_start_offset
        duration_shards = mathtools.divide_number_by_ratio(original_duration, ratio)
        duration_shards_before = duration_shards[:the_part]
        duration_before = sum(duration_shards_before)
        selected_duration_shard = duration_shards[the_part]
        new_start_offset = original_start_offset + duration_before
        new_stop_offset = new_start_offset + selected_duration_shard
        return new_start_offset, new_stop_offset

    def _get_timespan(self, score_specification, context_name):
        '''Evaluate timespan expression when 
        applied to `context_name` in `score_specification`.

        Return pair.
        '''
        anchor_timespan = score_specification.get_anchor_timespan(self, context_name)
        timespan = self._apply_timespan_modifiers(anchor_timespan)
        return timespan

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty offset request_modifiers list.
        '''
        filtered_result = []
        result = Timespan._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'timespan_modifiers=settingtools.ModifierInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

    def _scale(self, start_offset, stop_offset, multiplier):
        assert 0 < multiplier
        duration = stop_offset - start_offset
        new_duration = multiplier * duration
        new_stop_offset = start_offset + new_duration
        return start_offset, new_stop_offset

    def _set_duration(self, original_start_offset, original_stop_offset, duration):
        assert 0 < duration
        new_stop_offset = original_start_offset + duration
        return original_start_offset, new_stop_offset

    def _set_offsets(self, original_start_offset, original_stop_offset, 
        candidate_start_offset, candidate_stop_offset):
        if candidate_start_offset is not None and 0 <= candidate_start_offset:
            new_start_offset = candidate_start_offset
        elif candidate_start_offset is not None and candidate_start_offset < 0:
            new_start_offset = original_stop_offset + candidate_start_offset
        else:
            new_start_offset = original_start_offset
        if candidate_stop_offset is not None and 0 <= candidate_stop_offset:
            new_stop_offset = candidate_stop_offset
        elif candidate_stop_offset is not None and candidate_stop_offset < 0:
            new_stop_offset = original_stop_offset + candidate_stop_offset
        else:
            new_stop_offset = original_stop_offset
        return new_start_offset, new_stop_offset

    def _set_start_segment_identifier(self, segment_identifier):
        self._anchor = segment_identifier

    def _translate_offsets(self, original_start_offset, original_stop_offset, 
        start_offset_translation, stop_offset_translation):
        new_start_offset = original_start_offset + start_offset_translation
        new_stop_offset = original_stop_offset + stop_offset_translation
        return new_start_offset, new_stop_offset

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
        from experimental.tools import timeexpressiontools
        return timeexpressiontools.OffsetExpression(anchor=self)

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
        from experimental.tools import timeexpressiontools
        return timeexpressiontools.OffsetExpression(anchor=self)

    @property
    def timespan_modifiers(self):
        '''Read-only list of timespan modifiers to be applied 
        to timespan expression during evaluation.

            >>> red_segment.timespan.timespan_modifiers
            ModifierInventory([])

        Return object inventory of zero or more strings.
        '''
        return self._timespan_modifiers

    ### PUBLIC METHODS ###

    def divide_by_ratio(self, ratio):
        '''Divide timespan by `ratio`::

            >>> timespans = red_segment.timespan.divide_by_ratio((2, 3))

        ::
    
            >>> z(timespans[0])
            timeexpressiontools.TimespanExpression(
                anchor='red',
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, (2, 3), 0)'
                    ])
                )

        ::

            >>> z(timespans[1])
            timeexpressiontools.TimespanExpression(
                anchor='red',
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, (2, 3), 1)'
                    ])
                )

        Coerce integer `ratio` to ``Ratio(ratio*[1])``::

            >>> timespans = red_segment.timespan.divide_by_ratio(3)

        ::

            >>> z(timespans[0])
            timeexpressiontools.TimespanExpression(
                anchor='red',
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 0)'
                    ])
                )

        ::

            >>> z(timespans[1])
            timeexpressiontools.TimespanExpression(
                anchor='red',
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 1)'
                    ])
                )

        ::

            >>> z(timespans[2])
            timeexpressiontools.TimespanExpression(
                anchor='red',
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 2)'
                    ])
                )

        Return tuple of newly constructed timespans with appended modifier.
        '''
        result = []
        if mathtools.is_positive_integer_equivalent_number(ratio):
            ratio = int(ratio) * [1]
        for part in range(len(ratio)):
            new_timespan_expression = copy.deepcopy(self)
            timespan_modifier = \
                'self._divide_by_ratio(original_start_offset, original_stop_offset, {!r}, {!r})'
            timespan_modifier = timespan_modifier.format(ratio, part)
            new_timespan_expression.timespan_modifiers.append(timespan_modifier)
            result.append(new_timespan_expression)
        return tuple(result)

    def scale(self, multiplier):
        '''Scale timespan duration by `multiplier`.

            >>> timespan = red_segment.timespan.scale(Multiplier(4, 5))

        ::

            >>> z(timespan)
            timeexpressiontools.TimespanExpression(
                anchor='red',
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._scale(original_start_offset, original_stop_offset, Multiplier(4, 5))'
                    ])
                )

        Return copy of timespan with appended modifier.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        timespan_modifier = \
            'self._scale(original_start_offset, original_stop_offset, {!r})'
        timespan_modifier = timespan_modifier.format(multiplier)
        result = copy.deepcopy(self)
        result.timespan_modifiers.append(timespan_modifier)
        return result

    def set_duration(self, duration):
        '''Set timespan duration to `duration`.

        Return copy of timespan with appended modifier.
        '''
        duration = durationtools.Duration(duration)
        timespan_modifier = \
            'self._set_duration(original_start_offset, original_stop_offset, {!r})'
        timespan_modifier = timespan_modifier.format(duration)
        result = copy.deepcopy(self)
        result.timespan_modifiers.append(timespan_modifier)
        return result

    def set_offsets(self, start_offset=None, stop_offset=None):
        '''Set timespan start offset to `start_offset`
        and stop offset to `stop_offset`.

        Return copy of timespan with appended modifier.
        '''
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
        if stop_offset is not None:
            stop_offset = durationtools.Offset(stop_offset) 
        timespan_modifier = \
            'self._set_offsets(original_start_offset, original_stop_offset, {!r}, {!r})'
        timespan_modifier = timespan_modifier.format(start_offset, stop_offset)
        result = copy.deepcopy(self)
        result.timespan_modifiers.append(timespan_modifier)
        return result

    def translate_offsets(self, start_offset_translation=None, stop_offset_translation=None):
        '''Translate timespan start offset by `start_offset_translation`
        and stop offset by `stop_offset_translation`.

        Return copy of timespan with appended modifier.
        '''
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = durationtools.Duration(start_offset_translation)
        stop_offset_translation = durationtools.Duration(stop_offset_translation)
        timespan_modifier = \
            'self._translate_offsets(original_start_offset, original_stop_offset, {!r}, {!r})'
        timespan_modifier = timespan_modifier.format(start_offset_translation, stop_offset_translation)
        result = copy.deepcopy(self)
        result.timespan_modifiers.append(timespan_modifier)
        return result
