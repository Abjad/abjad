import abc
import numbers
from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import leaftools
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

    def __init__(self):
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

    def apply_offset_modifications(self, offsets):
        for offset_modification in self.offset_modifications:
            start_offset, stop_offset = offsets
            offset_modification = offset_modification.replace('start_offset', repr(start_offset))
            offset_modification = offset_modification.replace('stop_offset', repr(stop_offset))
            #self._debug(offset_modification, 'offset modification')
            offsets = eval(offset_modification, {'Offset': durationtools.Offset})
        return offsets
        
    def divide_by_ratio(self, ratio):
        ''''Divide self by `ratio`.

        Method is mirrors ``mathtools.divide_number_by_ratio()``.

        Return tuple of timespans.
        '''
        from experimental import symbolictimetools
        result = []
        for part in range(len(ratio)):
            # TODO: eventually create custom class different from TimeRatioOperator
            result.append(symbolictimetools.TimeRatioOperator(self.moniker, ratio, part))
        return tuple(result)

    def get_duration(self, score_specification, context_name):
        '''Evaluate duration of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return duration.
        '''
        start_offset, stop_offset = self.get_offsets(score_specification, context_name)
        return stop_offset - start_offset

    @abc.abstractmethod
    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        '''Get start offset and stop offset of symbolic timespan
        when applied to `context_name` in `score_specification`.

        Return pair.
        '''
        pass

    def select_background_measures(self, voice, start=None, stop=None, time_relation=None):
        '''Select the first five background measures that start during segment 'red'::

            >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
            >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
            >>> red_segment = score_specification.append_segment(name='red')

        ::

            >>> timespan = red_segment.select_background_measures('Voice 1', stop=5)

        ::

            >>> z(timespan)
            symbolictimetools.BackgroundMeasureSelector(
                anchor='red',
                stop_identifier=5,
                voice_name='Voice 1'
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
            time_relation=time_relation,
            voice_name=voice)
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

    def set_offsets(self, start=None, stop=None):
        '''Set offsets on self.
        '''
        from experimental import symbolictimetools
        assert isinstance(start, (numbers.Number, tuple, type(None))), repr(start)
        assert isinstance(stop, (numbers.Number, tuple, type(None))), repr(stop)
        #return symbolictimetools.OffsetOperator(self.moniker, start_offset=start, stop_offset=stop)
        if start is not None and durationtools.Offset(start) < 0:
            self.offset_modifications.append('(stop_offset + Offset({!r}), stop_offset)'.format(start))
        if stop is not None and durationtools.Offset(stop) < 0:
            self.offset_modifications.append('(start_offset, stop_offset + Offset({!r}))'.format(stop))
        if stop is not None and 0 <= durationtools.Offset(stop):
            self.offset_modifications.append('(start_offset, start_offset + Offset({!r}))'.format(stop))
        if start is not None and 0 <= durationtools.Offset(start):
            self.offset_modifications.append('(start_offset + Offset({!r}), stop_offset)'.format(start))
