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

    ::

        >>> from experimental import *

    Abstract base class from which conrete symbolic timespans inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, offset_modifications=None):
        self._offset_modifications = []

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

    ### PRIVAVET READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'offset_modifications=[]' in result:
            result = list(result)
            result.remove('offset_modifications=[]')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _evaluate_adjust_offsets(self, offsets, start_adjustment, stop_adjustment):
        original_start_offset, original_stop_offset = offsets
        new_start_offset, new_stop_offset = offsets
        if start_adjustment is not None and 0 <= start_adjustment:
            new_start_offset = original_start_offset + start_adjustment
        elif start_adjustment is not None and start_adjustment < 0:
            new_start_offset = original_stop_offset + start_adjustment
        if stop_adjustment is not None and 0 <= stop_adjustment:
            new_stop_offset = original_start_offset + stop_adjustment
        elif stop_adjustment is not None and stop_adjustment < 0:
            new_stop_offset = original_stop_offset + stop_adjustment
        return new_start_offset, new_stop_offset

    def _evaluate_divide_by_ratio(self, offsets, ratio, the_part):
        original_start_offset, original_stop_offset = offsets
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
            if not 'offset_modifications=[]' in string:
                filtered_result.append(string)
        return filtered_result
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def moniker(self):
        '''Form of symbolic timespan suitable for writing to disk.
        '''
        return self

    @property
    def offset_modifications(self):
        '''Read-only list of offset_modifications to be applied 
        to symbolic timespan during evaluation.

        Return list.
        '''
        return self._offset_modifications

    ### PUBLIC METHODS ###

    def adjust_offsets(self, start=None, stop=None):
        '''Add delayed evaluation offset setting command to symbolic timespan.
        
        Return symbolic timespan copy with offset modification.
        '''
        assert isinstance(start, (numbers.Number, tuple, type(None))), repr(start)
        assert isinstance(stop, (numbers.Number, tuple, type(None))), repr(stop)
        if start is not None:
            start = durationtools.Offset(start)
        if stop is not None:
            stop = durationtools.Offset(stop)
        offset_modification = 'self._evaluate_adjust_offsets(original_offsets, {!r}, {!r})'
        offset_modification = offset_modification.format(start, stop)
        result = copy.deepcopy(self)
        result.offset_modifications.append(offset_modification)
        return result

    def apply_offset_modifications(self, offsets):
        for offset_modification in self.offset_modifications:
            offset_modification = offset_modification.replace('original_offsets', repr(offsets))
            offsets = eval(offset_modification, {'Offset': durationtools.Offset, 'self': self})
        return offsets
        
    def divide_by_ratio(self, ratio):
        result = []
        for part in range(len(ratio)):
            new_symbolic_timespan = copy.deepcopy(self)
            offset_modification = 'self._evaluate_divide_by_ratio(original_offsets, {!r}, {!r})'
            offset_modification = offset_modification.format(ratio, part)
            new_symbolic_timespan.offset_modifications.append(offset_modification)
            result.append(new_symbolic_timespan)
        return result

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
