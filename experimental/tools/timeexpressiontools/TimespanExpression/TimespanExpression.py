import copy
from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import timespantools
from abjad.tools.timespantools.Timespan import Timespan
from experimental.tools.settingtools.SettingMakerMixin import SettingMakerMixin
from experimental.tools.timeexpressiontools.SelectMethodMixin import SelectMethodMixin


class TimespanExpression(Timespan, SelectMethodMixin, SettingMakerMixin):
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

    def __init__(self, timespan_modifiers=None):
        from experimental.tools import settingtools
        Timespan.__init__(self)
        timespan_modifiers = timespan_modifiers or []
        self._timespan_modifiers = settingtools.ModifierInventory(timespan_modifiers)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

            >>> red_segment.select('Voice 1') == red_segment.select('Voice 1')
            True

        Otherwise false::

            >>> red_segment.select('Voice 1') == blue_segment.select('Voice 1')
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
    def _keyword_argument_name_value_strings(self):
        result = Timespan._keyword_argument_name_value_strings.fget(self)
        if 'timespan_modifiers=ModifierInventory([])' in result:
            result = list(result)
            result.remove('timespan_modifiers=ModifierInventory([])')
        return tuple(result)

    @property
    def _timespan_abbreviation(self):
        '''Form of symbolic timespan suitable for writing to disk.
        '''
        return self

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
        '''Get start offset and stop offset of symbolic timespan
        when applied to `context_name` in `score_specification`.

        Return pair.
        '''
        raise NotImplemented

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

    def _translate_offsets(self, original_start_offset, original_stop_offset, 
        start_offset_translation, stop_offset_translation):
        new_start_offset = original_start_offset + start_offset_translation
        new_stop_offset = original_stop_offset + stop_offset_translation
        return new_start_offset, new_stop_offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        return self._score_specification

    @property
    def timespan_modifiers(self):
        '''Read-only list of timespan_modifiers to be applied 
        to symbolic timespan during evaluation.

            >>> red_segment.select('Voice 1').timespan_modifiers
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
            selectortools.SegmentSelector(
                anchor='red',
                voice_name='',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, (2, 3), 0)'
                    ])
                )

        ::

            >>> z(timespans[1])
            selectortools.SegmentSelector(
                anchor='red',
                voice_name='',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, (2, 3), 1)'
                    ])
                )

        Coerce integer `ratio` to ``Ratio(ratio*[1])``::

            >>> timespans = red_segment.timespan.divide_by_ratio(3)

        ::

            >>> z(timespans[0])
            selectortools.SegmentSelector(
                anchor='red',
                voice_name='',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 0)'
                    ])
                )

        ::

            >>> z(timespans[1])
            selectortools.SegmentSelector(
                anchor='red',
                voice_name='',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 1)'
                    ])
                )

        ::

            >>> z(timespans[2])
            selectortools.SegmentSelector(
                anchor='red',
                voice_name='',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
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
            new_symbolic_timespan = copy.deepcopy(self)
            timespan_modifier = \
                'self._divide_by_ratio(original_start_offset, original_stop_offset, {!r}, {!r})'
            timespan_modifier = timespan_modifier.format(ratio, part)
            new_symbolic_timespan.timespan_modifiers.append(timespan_modifier)
            result.append(new_symbolic_timespan)
        return tuple(result)

    def scale(self, multiplier):
        '''Scale timespan duration by `multiplier`.

            >>> z(red_segment.timespan.scale(Multiplier(4, 5)))
            selectortools.SegmentSelector(
                anchor='red',
                voice_name='',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
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
