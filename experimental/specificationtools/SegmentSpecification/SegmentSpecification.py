from abjad.tools import *
from experimental import helpertools
from experimental import interpretertools
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental import timespantools
from experimental.specificationtools.exceptions import *
from experimental.specificationtools.Specification import Specification
from experimental.statalservertools.StatalServer import StatalServer
import copy


class SegmentSpecification(Specification):
    r'''.. versionadded:: 1.0

    ::

        >>> from abjad.tools import scoretemplatetools
        >>> from experimental import specificationtools

    The examples below reference the following segment specification::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=template)
        
    ::
    
        >>> segment = score_specification.append_segment('red')

    ::
            
        >>> segment
        SegmentSpecification('red')

    ``SegmentSpecification`` properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template, segment_name):
        assert isinstance(segment_name, str), segment_name
        Specification.__init__(self, score_template)
        self._score_model = self.score_template()
        self._segment_name = segment_name
        self._multiple_context_settings = settingtools.MultipleContextSettingInventory()

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if isinstance(expr, int):
            return self.multiple_context_settings.__getitem__(expr)
        else:
            return self.contexts.__getitem__(expr) 
        
    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.segment_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def context_names(self):
        r'''Segment specification context names::

            >>> segment.context_names
            ['Voice 1']

        Only names for which context abbreviations exist are included.

        Return list of strings.
        '''
        return Specification.context_names.fget(self)

    @property
    def contexts(self):
        r'''Segment specification context proxy dictionary::

            >>> for key in segment.contexts:
            ...     key
            ... 
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Voice 1'

        Return context proxy dictionary.
        '''
        return Specification.contexts.fget(self)

    @property
    def duration(self):
        '''Segment specification duration.

            >>> segment.duration
            Duration(0, 1)

        Return duration.
        '''
        return durationtools.Duration(sum([durationtools.Duration(x) for x in self.time_signatures]))

    @property
    def multiple_context_settings(self):
        '''Segment specification multiple-context settings.

            >>> segment.multiple_context_settings
            MultipleContextSettingInventory([])

        Return multiple-context setting inventory.
        '''
        return self._multiple_context_settings

    @property
    def resolved_single_context_settings(self):
        r'''Segment specification resolved single-context settings::

            >>> for key in segment.resolved_single_context_settings:
            ...     key
            ... 
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Voice 1'

        Return context proxy dictionary.
        '''
        return Specification.resolved_single_context_settings.fget(self)

    @property
    def score_model(self):
        '''Segment score model::

            >>> segment.score_model
            Score-"Grouped Rhythmic Staves Score"<<1>>

        Return Abjad score object.
        '''
        return self._score_model

    @property
    def score_name(self):
        r'''Segment specification score name::

            >>> segment.score_name
            'Grouped Rhythmic Staves Score'

        Return string.
        '''
        return Specification.score_name.fget(self)

    @property
    def score_template(self):
        r'''Segment specification score template::

            >>> segment.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=1)

        Return score template.
        '''
        return Specification.score_template.fget(self)

    @property
    def segment_name(self):
        '''Segment specification name.

            >>> segment.segment_name
            'red'

        Return string.
        '''
        return self._segment_name

    @property
    def selector(self):
        '''Segment specification selector::

            >>> segment.selector
            SegmentSelector(index='red')

        Return segment selector.
        '''
        return selectortools.SegmentSelector(index=self.segment_name)

    @property
    def single_context_settings(self):
        r'''Segment specification single-context settings::

            >>> segment.single_context_settings
            SingleContextSettingInventory([])

        Return single-context setting inventory.
        '''
        return Specification.single_context_settings.fget(self)

    @property
    def start(self):
        '''Segment specification start timepoint.

            >>> segment.start
            Timepoint(anchor=SegmentSelector(index='red'), edge=Left)

        Return timepoint.
        '''
        return timespantools.Timepoint(anchor=self.selector, edge=Left)

    @property
    def stop(self):
        '''Segment specification stop timepoint.

            >>> segment.stop
            Timepoint(anchor=SegmentSelector(index='red'), edge=Right)

        Return timepoint.
        '''
        return timespantools.Timepoint(anchor=self.selector, edge=Right)

    @property
    def storage_format(self):
        r'''Segment specification storage format::

            >>> z(segment)
            specificationtools.SegmentSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=1
                    ),
                'red'
                )
        
        Return string.
        '''
        return Specification.storage_format.fget(self)

    @property
    def time_signatures(self):
        '''Segment specification time signatures::

            >>> segment.time_signatures
            []

        Return list of zero or more time signatures.
        '''
        try:
            resolved_single_context_setting = \
                self.resolved_single_context_settings.score_context_proxy.get_setting(
                attribute='time_signatures')
        except MissingContextSettingError:
            return []
        assert isinstance(resolved_single_context_setting.value, list), resolved_single_context_setting.value
        return resolved_single_context_setting.value

    @property
    def timespan(self):
        '''Segment specification timespan.

            >>> segment.timespan
            SingleSourceTimespan(selector=SegmentSelector(index='red'))

        Return timespan.
        '''
        return timespantools.SingleSourceTimespan(selector=self.selector)

    ### PUBLIC METHODS ###

    def count_ratio_item_selector_to_uninterpreted_division_command(self, resolved_single_context_setting):
        assert isinstance(resolved_single_context_setting.target, selectortools.CountRatioItemSelector)
        assert isinstance(resolved_single_context_setting.target.reference, 
            selectortools.BackgroundMeasureSliceSelector)
        assert resolved_single_context_setting.target.reference.inequality.timespan.selector.index == \
            self.segment_name
        ratio = resolved_single_context_setting.target.ratio
        index = resolved_single_context_setting.target.index
        time_signatures = self.time_signatures[:]
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(time_signatures, ratio)
        part = parts[index]
        durations = [durationtools.Duration(x) for x in part]
        duration = sum(durations)
        args = (resolved_single_context_setting.value, 
            duration, 
            resolved_single_context_setting.fresh, 
            resolved_single_context_setting.truncate)
        command = interpretertools.UninterpretedDivisionCommand(*args)
        return command

    def single_context_timespan_selector_to_uninterpreted_division_command(self, resolved_single_context_setting):
        #print 'here!'
        #print resolved_single_context_setting.storage_format
        assert isinstance(resolved_single_context_setting.target, selectortools.SingleContextTimespanSelector)
        assert isinstance(resolved_single_context_setting.target.timespan.selector, selectortools.SegmentSelector)
        assert resolved_single_context_setting.target.timespan.selector.index == self.segment_name
        args = (
            resolved_single_context_setting.value, 
            self.duration, 
            resolved_single_context_setting.fresh, 
            resolved_single_context_setting.truncate) 
        command = interpretertools.UninterpretedDivisionCommand(*args)
        #print command
        #print ''
        return command

    def get_multiple_context_settings(self, target=None, attribute=None):
        result = []
        for multiple_context_setting in self.multiple_context_settings:
            if target is None or multiple_context_setting.target == target:
                if attribute is None or multiple_context_setting.attribute == attribute:
                    result.append(multiple_context_setting)
        return result

    def get_uninterpreted_division_commands_that_start_during_segment(self, context_name):
        resolved_single_context_settings = self.get_resolved_single_context_settings('divisions', context_name)
        uninterpreted_division_commands = []
        for resolved_single_context_setting in resolved_single_context_settings:
            if isinstance(resolved_single_context_setting.target, selectortools.CountRatioItemSelector):
                uninterpreted_division_command = \
                    self.count_ratio_item_selector_to_uninterpreted_division_command(
                    resolved_single_context_setting)
            else:
                uninterpreted_division_command = \
                    self.single_context_timespan_selector_to_uninterpreted_division_command(
                    resolved_single_context_setting)
            uninterpreted_division_commands.append(uninterpreted_division_command)
        return uninterpreted_division_commands

    def get_resolved_single_context_settings(self, attribute, context_name):
        context = componenttools.get_first_component_in_expr_with_name(self.score_model, context_name)
        for component in componenttools.get_improper_parentage_of_component(context):
            context_proxy = self.resolved_single_context_settings[component.name]
            resolved_single_context_settings = context_proxy.get_settings(attribute=attribute)
            if resolved_single_context_settings:
                return resolved_single_context_settings
        return []

    def get_rhythm_commands_that_start_during_segment(self, voice_name):
        from experimental.specificationtools import library
        resolved_single_context_settings = self.get_resolved_single_context_settings('rhythm', voice_name)
        if resolved_single_context_settings is None:
            return []
        rhythm_commands = []
        for resolved_single_context_setting in resolved_single_context_settings:
            if isinstance(resolved_single_context_setting.target, selectortools.CountRatioItemSelector):
                raise Exception('implement me when it comes time.')
            else:
                rhythm_command = interpretertools.RhythmCommand(
                    resolved_single_context_setting.value, self.duration, resolved_single_context_setting.fresh)
            rhythm_commands.append(rhythm_command)
        return rhythm_commands

    def preprocess_setting_target(self, target):
        if isinstance(target, (str, list, type(self))):
            target = self.select_timespan(contexts=target)
        return target

    def retrieve_attribute(self, attribute, context_name=None):
        return requesttools.AttributeIndicator(attribute, self.segment_name, context_name=context_name)

    def select_background_measures(self, start=None, stop=None):
        '''Select the first five background measures that start during segment::

            >>> selector = segment.select_background_measures(stop=5)

        ::

            >>> z(selector)
            selectortools.BackgroundMeasureSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    ),
                stop=5
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality, start=start, stop=stop)
        return selector
    
    def select_divisions(self, contexts=None, start=None, stop=None):
        '''Select the first five divisions that start during segment::

            >>> contexts = ['Voice 1', 'Voice 3']
            >>> selector = segment.select_divisions(contexts=contexts, stop=5)

        ::
            
            >>> z(selector)
            selectortools.MultipleContextDivisionSliceSelector(
                contexts=['Voice 1', 'Voice 3'],
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    ),
                stop=5
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.MultipleContextDivisionSliceSelector(
            contexts=contexts, inequality=inequality, start=start, stop=stop)
        return selector

    def select_duration_ratio(self, ratio, index, contexts=None):
        '''Select the last third of the timespan of segment::

            >>> selector = segment.select_duration_ratio((1, 1, 1), -1, contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(selector)
            selectortools.DurationRatioItemSelector(
                selectortools.MultipleContextTimespanSelector(
                    contexts=['Voice 1', 'Voice 3'],
                    timespan=timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    ),
                mathtools.Ratio(1, 1, 1),
                index=-1
                )

        Return selector.
        '''
        selector = selectortools.MultipleContextTimespanSelector(contexts=contexts, timespan=self.timespan)
        selector = selectortools.DurationRatioItemSelector(selector, ratio, index)
        return selector

    def select_leaves(self, contexts=None, start=None, stop=None):
        '''Select the first ``40`` leaves that start during segment::

            >>> contexts = ['Voice 1', 'Voice 3']
            >>> selector = segment.select_leaves(contexts=contexts, stop=40)

        ::

            >>> z(selector)
            selectortools.MultipleContextCounttimeComponentSliceSelector(
                contexts=['Voice 1', 'Voice 3'],
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    ),
                klass=leaftools.Leaf,
                stop=40
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.MultipleContextCounttimeComponentSliceSelector(
            contexts=contexts, inequality=inequality, klass=leaftools.Leaf, 
            start=start, stop=stop)
        return selector

    def select_notes_and_chords(self, contexts=None, start=None, stop=None):
        '''Select the first ``40`` notes and chords that start during segment.
        Do this for ``'Voice 1'`` and ``'Voice 3'``::

            >>> contexts = ['Voice 1', 'Voice 3']
            >>> selector = segment.select_notes_and_chords(contexts=contexts, stop=40)

        ::

            >>> z(selector)
            selectortools.MultipleContextCounttimeComponentSliceSelector(
                contexts=['Voice 1', 'Voice 3'],
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    ),
                klass=helpertools.KlassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                stop=40
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.MultipleContextCounttimeComponentSliceSelector(
            contexts=contexts, inequality=inequality, klass=(notetools.Note, chordtools.Chord),
            start=start, stop=stop)
        return selector

    def select_ratio_of_background_measures(self, ratio, index=0, count=True):
        r'''Select the first third of background measures starting during segment::

            >>> selector = segment.select_ratio_of_background_measures((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.CountRatioItemSelector(
                selectortools.BackgroundMeasureSliceSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        )
                    ),
                mathtools.Ratio(1, 1, 1),
                index=0
                )

        Return selector.
        '''
        selector = self.select_background_measures()
        if count:
            selector = selectortools.CountRatioItemSelector(selector, ratio, index=index)
        else:
            selector = selectortools.DurationRatioItemSelector(selector, ratio, index=index)
        return selector

    def select_ratio_of_divisions(self, ratio, index, contexts=None, count=True):
        r'''Select the first third of divisions starting during segment::

            >>> selector = segment.select_ratio_of_divisions((1, 1, 1), 0, contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(selector)
            selectortools.CountRatioItemSelector(
                selectortools.MultipleContextDivisionSliceSelector(
                    contexts=['Voice 1', 'Voice 3'],
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        )
                    ),
                mathtools.Ratio(1, 1, 1),
                index=0
                )

        Return selector.
        '''
        selector = self.select_divisions(contexts=contexts)
        if count:
            selector = selectortools.CountRatioItemSelector(selector, ratio, index=index)
        else:
            selector = selectortools.DurationRatioItemSelector(selector, ratio, index=index)
        return selector

    def select_ratio_of_leaves(self, ratio, index, contexts=None, count=True):
        r'''Select the first third of leaves starting during segment::

            >>> selector = segment.select_ratio_of_leaves((1, 1, 1), 0, contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(selector)
            selectortools.CountRatioItemSelector(
                selectortools.MultipleContextCounttimeComponentSliceSelector(
                    contexts=['Voice 1', 'Voice 3'],
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    klass=leaftools.Leaf
                    ),
                mathtools.Ratio(1, 1, 1),
                index=0
                )

        Return selector.
        '''
        selector = self.select_leaves(contexts=contexts)
        if count:
            selector = selectortools.CountRatioItemSelector(selector, ratio, index=index)
        else:
            selector = selectortools.DurationRatioItemSelector(selector, ratio, index=index)
        return selector

    def select_ratio_of_notes_and_chords(self, ratio, index, contexts=None, count=True):
        r'''Select the first third of notes and chords starting during segment::

            >>> selector = segment.select_ratio_of_notes_and_chords((1, 1, 1), 0, contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(selector)
            selectortools.CountRatioItemSelector(
                selectortools.MultipleContextCounttimeComponentSliceSelector(
                    contexts=['Voice 1', 'Voice 3'],
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    klass=helpertools.KlassInventory([
                        notetools.Note,
                        chordtools.Chord
                        ])
                    ),
                mathtools.Ratio(1, 1, 1),
                index=0
                )

        Return selector.
        '''
        selector = self.select_notes_and_chords(contexts=contexts)
        if count:
            selector = selectortools.CountRatioItemSelector(selector, ratio, index=index)
        else:
            selector = selectortools.DurationRatioItemSelector(selector, ratio, index=index)
        return selector

    def select_timespan(self, contexts=None):
        '''Select contexts::

            >>> selector = segment.select_timespan()

        ::

            >>> z(selector)
            selectortools.MultipleContextTimespanSelector(
                contexts=['Grouped Rhythmic Staves Score'],
                timespan=timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                )

        Return selector.
        '''
        contexts = self._context_token_to_context_names(contexts)
        return selectortools.MultipleContextTimespanSelector(contexts=contexts, timespan=self.timespan)

    def set_aggregate(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'aggregate'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_articulations(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'articulations'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_attribute(self, attribute, target, source, 
        callback=None, count=None, offset=None, persistent=True, truncate=False):
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(persistent, type(True)), repr(persistent)
        assert isinstance(truncate, type(True)), repr(truncate)
        target = self.preprocess_setting_target(target)
        source = requesttools.request_source_to_request(source, callback=callback, count=count, offset=offset)
        multiple_context_setting = settingtools.MultipleContextSetting(target, attribute, source, 
            persistent=persistent, truncate=truncate)
        self.multiple_context_settings.append(multiple_context_setting)
        return multiple_context_setting

    def set_chord_treatment(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'chord_treatment'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_divisions(self, contexts, source, 
        callback=None, count=None, offset=None, persistent=True, truncate=False):
        attribute = 'divisions'
        return self.set_attribute(attribute, contexts, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, truncate=truncate)

    def set_duration_in_seconds(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'duration_in_seconds'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_dynamics(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'dynamics'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_marks(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'marks'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_markup(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'markup'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_pitch_classes(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'pitch_classes'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_pitch_class_application(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'pitch_class_application'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_pitch_class_transform(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'pitch_class_transform'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_register(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'register'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_rhythm(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'rhythm'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_retrograde_divisions(self, contexts, source,
        count=None, offset=None, persistent=True, truncate=True):
        r'''.. versionadded:: 1.0

        Set `contexts` divisions from `source` taken in retrograde.
        '''
        string = 'sequencetools.reverse_sequence'
        callback = helpertools.Callback(eval(string), string)
        return self.set_divisions(contexts, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, truncate=truncate)

    def set_rotated_divisions(self, contexts, source, n, 
        count=None, offset=None, persistent=True, truncate=True):
        r'''.. versionadded:: 1.0

        Set `contexts` divisions from `source` rotated by integer `n`.
        '''
        assert isinstance(n, int), repr(n)
        string = 'lambda x: sequencetools.rotate_sequence(x, {})'.format(n)
        callback = helpertools.Callback(eval(string), string)
        return self.set_divisions(contexts, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, truncate=truncate)

    def set_tempo(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'tempo'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_time_signatures(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'time_signatures'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_written_duration(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'written_duration'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)
