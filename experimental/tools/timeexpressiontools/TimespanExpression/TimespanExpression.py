import abc
import copy
import numbers
from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import timerelationtools
from abjad.tools.timespantools.Timespan import Timespan


class TimespanExpression(Timespan):
    r'''

    ::
        
        >>> from experimental.tools import *

    Abstract base class from which conrete symbolic timespans inherit.

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> setting = red_segment.set_time_signatures([(4, 8), (3, 8)])

    ::
        
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> setting = blue_segment.set_time_signatures([(9, 16), (3, 16)])

    The examples below refer to the score and segment specifications defined above.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

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

    def _apply_timespan_modifiers(self, start_offset, stop_offset):
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
        return start_offset, stop_offset
        
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

    @abc.abstractmethod
    def _get_offsets(self, score_specification, context_name):
        '''Get start offset and stop offset of symbolic timespan
        when applied to `context_name` in `score_specification`.

        Return pair.
        '''
        pass

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

    def _store_multiple_context_setting(self, attribute, source, contexts=None, persist=True, truncate=None):
        from experimental.tools import requesttools
        from experimental.tools import settingtools
        request = requesttools.expr_to_request(source)
        assert self.score_specification is not None
        context_names = self.score_specification._context_token_to_context_names(contexts)
        multiple_context_setting = settingtools.MultipleContextSetting(
            attribute, 
            request, 
            self._timespan_abbreviation,
            context_names=context_names,
            persist=persist, 
            truncate=truncate
            )
        self.score_specification.multiple_context_settings.append(multiple_context_setting)
        return multiple_context_setting

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

            >>> timespans = red_segment.select('Voice 1').divide_by_ratio((2, 3))

        ::
    
            >>> z(timespans[0])
            timeexpressiontools.SegmentSelector(
                anchor='red',
                voice_name='Voice 1',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, (2, 3), 0)'
                    ])
                )

        ::

            >>> z(timespans[1])
            timeexpressiontools.SegmentSelector(
                anchor='red',
                voice_name='Voice 1',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, (2, 3), 1)'
                    ])
                )

        Coerce integer `ratio` to ``Ratio(ratio*[1])``::

            >>> timespans = red_segment.select('Voice 1').divide_by_ratio(3)

        ::

            >>> z(timespans[0])
            timeexpressiontools.SegmentSelector(
                anchor='red',
                voice_name='Voice 1',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 0)'
                    ])
                )

        ::

            >>> z(timespans[1])
            timeexpressiontools.SegmentSelector(
                anchor='red',
                voice_name='Voice 1',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 1), None))"
                    ]),
                timespan_modifiers=settingtools.ModifierInventory([
                    'self._divide_by_ratio(original_start_offset, original_stop_offset, [1, 1, 1], 1)'
                    ])
                )

        ::

            >>> z(timespans[2])
            timeexpressiontools.SegmentSelector(
                anchor='red',
                voice_name='Voice 1',
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

            >>> z(red_segment.select('Voice 1').scale(Multiplier(4, 5)))
            timeexpressiontools.SegmentSelector(
                anchor='red',
                voice_name='Voice 1',
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

    def select_background_measures(self, voice_name, time_relation=None):
        '''Select voice ``1`` background measures 
        that start during segment ``'red'``::

            >>> selector = red_segment.select_background_measures('Voice 1')

        ::

            >>> z(selector)
            timeexpressiontools.BackgroundMeasureSelector(
                anchor='red',
                voice_name='Voice 1'
                )

        Return background measure selector.
        '''
        from experimental.tools import timeexpressiontools
        selector = timeexpressiontools.BackgroundMeasureSelector(
            anchor=self._timespan_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        selector._score_specification = self.score_specification
        return selector

    def select_beats(self, voice_name, time_relation=None):
        '''Select voice ``1`` beats that start during segment ``'red'``::

            >>> selector = red_segment.select_beats('Voice 1')

        ::

            >>> z(selector)
            timeexpressiontools.BeatSelector(
                anchor='red',
                voice_name='Voice 1'
                )

        Return beat selector.
        '''
        from experimental.tools import timeexpressiontools
        selector = timeexpressiontools.BeatSelector(
            anchor=self._timespan_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        selector._score_specification = self.score_specification
        return selector

    def select_divisions(self, voice_name, time_relation=None):
        '''Select voice ``1`` divisions that start during segment ``'red'``::

            >>> selector = red_segment.select_divisions('Voice 1')

        ::
            
            >>> z(selector)
            timeexpressiontools.DivisionSelector(
                anchor='red',
                voice_name='Voice 1'
                )

        Return division selector.
        '''
        from experimental.tools import timeexpressiontools
        selector = timeexpressiontools.DivisionSelector(
            anchor=self._timespan_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        selector._score_specification = self.score_specification
        return selector

    def select_leaves(self, voice_name, time_relation=None):
        '''Select voice ``1`` leaves that start during segment ``'red'``::

            >>> selector = red_segment.select_leaves('Voice 1')

        ::

            >>> z(selector)
            timeexpressiontools.CounttimeComponentSelector(
                anchor='red',
                klass=leaftools.Leaf,
                voice_name='Voice 1'
                )

        Return counttime component selector.
        '''
        from experimental.tools import timeexpressiontools
        selector = timeexpressiontools.CounttimeComponentSelector(
            anchor=self._timespan_abbreviation,
            time_relation=time_relation, 
            klass=leaftools.Leaf, 
            voice_name=voice_name
            )
        selector._score_specification = self.score_specification
        return selector

    def select_notes_and_chords(self, voice_name, time_relation=None):
        '''Select voice ``1`` notes and chords that start during segment ``'red'``::

            >>> selector = red_segment.select_notes_and_chords('Voice 1')

        ::

            >>> z(selector)
            timeexpressiontools.CounttimeComponentSelector(
                anchor='red',
                klass=helpertools.KlassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                voice_name='Voice 1'
                )

        Return counttime component selector.
        '''
        from experimental.tools import timeexpressiontools
        selector = timeexpressiontools.CounttimeComponentSelector(
            anchor=self._timespan_abbreviation,
            time_relation=time_relation, 
            klass=(notetools.Note, chordtools.Chord),
            voice_name=voice_name
            )
        selector._score_specification = self.score_specification
        return selector

    def set_aggregate(self, source, contexts=None, persist=True):
        r'''Set aggregate of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'aggregate'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_articulations(self, source, contexts=None, persist=True):
        r'''Set articulations of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'articulations'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_chord_treatment(self, source, contexts=None, persist=True):
        r'''Set chord treatment of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'chord_treatment'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_divisions(self, source, contexts=None, persist=True, truncate=None):
        r'''Set divisions `contexts` to `source`::

            >>> setting = red_segment.set_divisions([(3, 16)], contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                attribute='divisions',
                request=requesttools.AbsoluteRequest(
                    [(3, 16)]
                    ),
                anchor='red',
                context_names=['Voice 1', 'Voice 3'],
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'divisions'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, truncate=truncate, persist=persist)

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

    def set_dynamics(self, source, contexts=None, persist=True):
        r'''Set dynamics of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'dynamics'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_marks(self, source, contexts=None, persist=True):
        r'''Set marks of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'marks'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_markup(self, source, contexts=None, persist=True):
        r'''Set markup of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'markup'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

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

    def set_pitch_class_application(self, source, contexts=None, persist=True):
        r'''Set pitch-class application of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_application'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_pitch_class_transform(self, source, contexts=None, persist=True):
        r'''Set pitch-class transform of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_transform'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_pitch_classes(self, source, contexts=None, persist=True):
        r'''Set pitch-classes of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_classes'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_registration(self, source, contexts=None, persist=True):
        r'''Set registration of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'registration'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_rhythm(self, source, contexts=None, persist=True):
        r'''Set rhythm of `contexts` to `source`.

            >>> setting = red_segment.set_rhythm(library.sixteenths)

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                attribute='rhythm',
                request=requesttools.AbsoluteRequest(
                    rhythmmakertools.TaleaRhythmMaker(
                        [1],
                        16,
                        prolation_addenda=[],
                        secondary_divisions=[],
                        beam_each_cell=False,
                        beam_cells_together=True,
                        tie_split_notes=False
                        )
                    ),
                anchor='red',
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'rhythm'
        return self._store_multiple_context_setting(attribute, source, contexts=contexts, persist=persist)

    def set_tempo(self, source, contexts=None, persist=True):
        r'''Set tempo of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'tempo'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_time_signatures(self, source, contexts=None, persist=True):
        r'''Set time signatures of `contexts` to `source`.

            >>> setting = red_segment.set_time_signatures([(3, 8), (4, 8)])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                attribute='time_signatures',
                request=requesttools.AbsoluteRequest(
                    [(3, 8), (4, 8)]
                    ),
                anchor='red',
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'time_signatures'
        return self._store_multiple_context_setting(attribute, source, contexts=contexts, persist=persist)

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
