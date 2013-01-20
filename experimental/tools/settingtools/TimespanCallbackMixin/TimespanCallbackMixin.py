import abc
import copy
from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import timespantools
#from experimental.tools.settingtools.Expression import Expression
from abjad.tools.abctools.AbjadObject import AbjadObject


#class TimespanCallbackMixin(Expression):
class TimespanCallbackMixin(AbjadObject):
    '''Timespan callback mixin.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> setting = red_segment.set_time_signatures([(4, 8), (3, 8)])
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> setting = blue_segment.set_time_signatures([(9, 16), (3, 16)])

    The examples below refer to the score and segment specifications defined above.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, timespan_callbacks=None):
        from experimental.tools import settingtools
        timespan_callbacks = timespan_callbacks or []
        self._timespan_callbacks = settingtools.CallbackInventory(timespan_callbacks)

    ### PRIVATE METHODS ###

    def _apply_timespan_callbacks(self, timespan):
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        start_offset, stop_offset = timespan.offsets
        evaluation_context = {
            'self': self,
            'Duration': durationtools.Duration,
            'Multiplier': durationtools.Multiplier,
            'Offset': durationtools.Offset,
            }
        for timespan_callback in self.timespan_callbacks:
            timespan_callback = timespan_callback.replace('original_start_offset', repr(start_offset))
            timespan_callback = timespan_callback.replace('original_stop_offset', repr(stop_offset))
            start_offset, stop_offset = eval(timespan_callback, evaluation_context)
            assert start_offset <= stop_offset
        return timespantools.Timespan(start_offset, stop_offset)
        
    def _copy_and_append_timespan_callback(self, callback):
        result = copy.deepcopy(self)
        result.timespan_callbacks.append(callback)
        return result
    
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
    def timespan_callbacks(self):
        '''Read-only list of timespan callbacks to be applied 
        during evaluation:

        ::

            >>> red_segment.timespan.timespan_callbacks
            CallbackInventory([])

        Return callback inventory of zero or more strings.
        '''
        return self._timespan_callbacks
    
    ### PUBLIC METHODS ###

    def divide_by_ratio(self, ratio):
        '''Divide timespan by `ratio`::

            >>> timespans = red_segment.timespan.divide_by_ratio((2, 3))

        ::
    
            >>> z(timespans[0])
            settingtools.TimespanExpression(
                anchor='red',
                timespan_callbacks=settingtools.CallbackInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, (2, 3), 0)'
                    ])
                )

        ::

            >>> z(timespans[1])
            settingtools.TimespanExpression(
                anchor='red',
                timespan_callbacks=settingtools.CallbackInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, (2, 3), 1)'
                    ])
                )

        Coerce integer `ratio` to ``Ratio(ratio*[1])``::

            >>> timespans = red_segment.timespan.divide_by_ratio(3)

        ::

            >>> z(timespans[0])
            settingtools.TimespanExpression(
                anchor='red',
                timespan_callbacks=settingtools.CallbackInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 0)'
                    ])
                )

        ::

            >>> z(timespans[1])
            settingtools.TimespanExpression(
                anchor='red',
                timespan_callbacks=settingtools.CallbackInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 1)'
                    ])
                )

        ::

            >>> z(timespans[2])
            settingtools.TimespanExpression(
                anchor='red',
                timespan_callbacks=settingtools.CallbackInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 2)'
                    ])
                )

        Return tuple of newly constructed timespans with appended callback.
        '''
        result = []
        if mathtools.is_positive_integer_equivalent_number(ratio):
            ratio = int(ratio) * [1]
        for part in range(len(ratio)):
            timespan_callback = \
                'self._divide_by_ratio(original_start_offset, original_stop_offset, {!r}, {!r})'
            timespan_callback = timespan_callback.format(ratio, part)
            result.append(self._copy_and_append_timespan_callback(timespan_callback))
        return tuple(result)

    def scale(self, multiplier):
        '''Scale timespan duration by `multiplier`.

            >>> timespan = red_segment.timespan.scale(Multiplier(4, 5))

        ::

            >>> z(timespan)
            settingtools.TimespanExpression(
                anchor='red',
                timespan_callbacks=settingtools.CallbackInventory([
                    'self._scale(original_start_offset, original_stop_offset, Multiplier(4, 5))'
                    ])
                )

        Return copy of timespan with appended callback.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        timespan_callback = \
            'self._scale(original_start_offset, original_stop_offset, {!r})'
        timespan_callback = timespan_callback.format(multiplier)
        return self._copy_and_append_timespan_callback(timespan_callback)

    def set_duration(self, duration):
        '''Set timespan duration to `duration`.

        Return copy of timespan with appended callback.
        '''
        duration = durationtools.Duration(duration)
        timespan_callback = \
            'self._set_duration(original_start_offset, original_stop_offset, {!r})'
        timespan_callback = timespan_callback.format(duration)
        return self._copy_and_append_timespan_callback(timespan_callback)

    def set_offsets(self, start_offset=None, stop_offset=None):
        '''Set timespan start offset to `start_offset`
        and stop offset to `stop_offset`.

        Return copy of timespan with appended callback.
        '''
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
        if stop_offset is not None:
            stop_offset = durationtools.Offset(stop_offset) 
        timespan_callback = \
            'self._set_offsets(original_start_offset, original_stop_offset, {!r}, {!r})'
        timespan_callback = timespan_callback.format(start_offset, stop_offset)
        return self._copy_and_append_timespan_callback(timespan_callback)

    def translate_offsets(self, start_offset_translation=None, stop_offset_translation=None):
        '''Translate timespan start offset by `start_offset_translation`
        and stop offset by `stop_offset_translation`.

        Return copy of timespan with appended callback.
        '''
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = durationtools.Duration(start_offset_translation)
        stop_offset_translation = durationtools.Duration(stop_offset_translation)
        timespan_callback = \
            'self._translate_offsets(original_start_offset, original_stop_offset, {!r}, {!r})'
        timespan_callback = timespan_callback.format(start_offset_translation, stop_offset_translation)
        return self._copy_and_append_timespan_callback(timespan_callback)
