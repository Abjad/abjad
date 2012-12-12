import abc
import copy
import numbers
from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import timerelationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class SymbolicTimespan(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which conrete symbolic timespans inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, timespan_modifications=None):
        self._timespan_modifications = timespan_modifications or []

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

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
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'timespan_modifications=[]' in result:
            result = list(result)
            result.remove('timespan_modifications=[]')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _adjust_timespan_offsets(self, start_offset, stop_offset, start_adjustment, stop_adjustment):
        original_start_offset, original_stop_offset = start_offset, stop_offset
        new_start_offset, new_stop_offset = start_offset, stop_offset
        if start_adjustment is not None and 0 <= start_adjustment:
            new_start_offset = original_start_offset + start_adjustment
        elif start_adjustment is not None and start_adjustment < 0:
            new_start_offset = original_stop_offset + start_adjustment
        if stop_adjustment is not None and 0 <= stop_adjustment:
            new_stop_offset = original_start_offset + stop_adjustment
        elif stop_adjustment is not None and stop_adjustment < 0:
            new_stop_offset = original_stop_offset + stop_adjustment
        return new_start_offset, new_stop_offset

    def _apply_timespan_modifications(self, start_offset, stop_offset):
        evaluation_context = {
            'self': self,
            'Offset': durationtools.Offset,
            }
        for timespan_modification in self.timespan_modifications:
            timespan_modification = timespan_modification.replace('start_offset', repr(start_offset))
            timespan_modification = timespan_modification.replace('stop_offset', repr(stop_offset))
            start_offset, stop_offset = eval(timespan_modification, evaluation_context)
        return start_offset, stop_offset
        
    def _divide_timespan_by_ratio(self, start_offset, stop_offset, ratio, the_part):
        original_start_offset, original_stop_offset = start_offset, stop_offset
        original_duration = original_stop_offset - original_start_offset
        duration_shards = mathtools.divide_number_by_ratio(original_duration, ratio)
        duration_shards_before = duration_shards[:the_part]
        duration_before = sum(duration_shards_before)
        selected_duration_shard = duration_shards[the_part]
        new_start_offset = original_start_offset + duration_before
        new_stop_offset = new_start_offset + selected_duration_shard
        return new_start_offset, new_stop_offset

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty offset modifications list.
        '''
        filtered_result = []
        result = AbjadObject._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'timespan_modifications=[]' in string:
                filtered_result.append(string)
        return filtered_result
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def moniker(self):
        '''Form of symbolic timespan suitable for writing to disk.
        '''
        return self

    @property
    def timespan_modifications(self):
        '''Read-only list of timespan_modifications to be applied 
        to symbolic timespan during evaluation.

        Return list.
        '''
        return self._timespan_modifications

    ### PUBLIC METHODS ###

    def adjust_timespan_offsets(self, start=None, stop=None):
        '''Add delayed evaluation offset setting command to symbolic timespan.
        
        Return symbolic timespan copy with offset modification.
        '''
        assert isinstance(start, (numbers.Number, tuple, type(None))), repr(start)
        assert isinstance(stop, (numbers.Number, tuple, type(None))), repr(stop)
        if start is not None:
            start = durationtools.Offset(start)
        if stop is not None:
            stop = durationtools.Offset(stop)
        timespan_modification = 'self._adjust_timespan_offsets(start_offset, stop_offset, {!r}, {!r})'
        timespan_modification = timespan_modification.format(start, stop)
        result = copy.deepcopy(self)
        result.timespan_modifications.append(timespan_modification)
        return result

    def divide_timespan_by_ratio(self, ratio):
        result = []
        for part in range(len(ratio)):
            new_symbolic_timespan = copy.deepcopy(self)
            timespan_modification = 'self._divide_timespan_by_ratio(start_offset, stop_offset, {!r}, {!r})'
            timespan_modification = timespan_modification.format(ratio, part)
            new_symbolic_timespan.timespan_modifications.append(timespan_modification)
            result.append(new_symbolic_timespan)
        return tuple(result)

    def get_duration(self, score_specification, context_name):
        '''Evaluate duration of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return duration.
        '''
        start_offset, stop_offset = self.get_offsets(score_specification, context_name)
        return stop_offset - start_offset

    @abc.abstractmethod
    def get_offsets(self, score_specification, context_name):
        '''Get start offset and stop offset of symbolic timespan
        when applied to `context_name` in `score_specification`.

        Return pair.
        '''
        pass

    def select_background_measures(self, start=None, stop=None, time_relation=None):
        '''Select the first five background measures that start during segment 'red'::

            >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
            >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
            >>> red_segment = score_specification.append_segment(name='red')

        ::

            >>> timespan = red_segment.select_background_measures(stop=5)

        ::

            >>> z(timespan)
            symbolictimetools.BackgroundMeasureSelector(
                anchor='red',
                stop_identifier=5
                )

        Return background measure symbolic timespan.
        '''
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        from experimental import symbolictimetools
        timespan = symbolictimetools.BackgroundMeasureSelector(
            anchor=self.moniker,
            start_identifier=start, 
            stop_identifier=stop, 
            time_relation=time_relation)
        return timespan

    def select_divisions(self, voice, start=None, stop=None, time_relation=None):
        '''Select the first five divisions that start during segment 'red'::

            >>> timespan = red_segment.select_divisions('Voice 1', stop=5)

        ::
            
            >>> z(timespan)
            symbolictimetools.DivisionSelector(
                anchor='red',
                stop_identifier=5,
                voice_name='Voice 1'
                )

        Return timespan.
        '''
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        from experimental import symbolictimetools
        timespan = symbolictimetools.DivisionSelector(
            anchor=self.moniker,
            start_identifier=start, 
            stop_identifier=stop, 
            voice_name=voice,
            time_relation=time_relation)
        return timespan

    def select_leaves(self, voice, start=None, stop=None, time_relation=None):
        '''Select the first ``40`` voice ``1`` leaves that start during segment ``'red'``::

            >>> timespan = red_segment.select_leaves('Voice 1', stop=40)

        ::

            >>> z(timespan)
            symbolictimetools.CounttimeComponentSelector(
                anchor='red',
                klass=leaftools.Leaf,
                stop_identifier=40,
                voice_name='Voice 1'
                )

        Return timespan.
        '''
        assert isinstance(voice, (str, type(None)))
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        from experimental import symbolictimetools
        timespan = symbolictimetools.CounttimeComponentSelector(
            anchor=self.moniker,
            time_relation=time_relation, 
            klass=leaftools.Leaf, 
            start_identifier=start, 
            stop_identifier=stop, 
            voice_name=voice)
        return timespan

    def select_notes_and_chords(self, voice, start=None, stop=None, time_relation=None):
        '''Select the first ``40`` voice ``1`` notes and chords 
        that start during segment ``'red'``::

            >>> timespan = red_segment.select_notes_and_chords('Voice 1', stop=40)

        ::

            >>> z(timespan)
            symbolictimetools.CounttimeComponentSelector(
                anchor='red',
                klass=helpertools.KlassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                stop_identifier=40,
                voice_name='Voice 1'
                )

        Return timespan.
        '''
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        from experimental import symbolictimetools
        timespan = symbolictimetools.CounttimeComponentSelector(
            anchor=self.moniker,
            time_relation=time_relation, 
            klass=(notetools.Note, chordtools.Chord),
            start_identifier=start, 
            stop_identifier=stop, 
            voice_name=voice)
        return timespan
