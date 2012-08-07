from abjad.tools import *
from experimental import helpertools
from experimental import interpretertools
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental import timespantools
from experimental.exceptions import *
from experimental.specificationtools.Specification import Specification


class SegmentSpecification(Specification):
    r'''.. versionadded:: 1.0

    ::

        >>> from abjad.tools import *
        >>> from experimental import *

    The examples below reference the following segment specification::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        
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

    ### PRIVATE METHODS ###

    # DEPRECATED: pass timespan and contexts separately everywhere in system
    def _expr_to_selector(self, expr):
        if isinstance(expr, selectortools.Selector):
            return expr
        else:
            return self.select_segment_timespan()

    # DEPRECATED: eliminate multiple-context selectors.
    # DEPRECATED: then pass selectors and contexts separately everywhere in system.
    def _set_attribute(self, attribute, selector, source, 
        callback=None, contexts=None, count=None, offset=None, persist=True, truncate=False):
        contexts = self._context_token_to_context_names(contexts)
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(persist, type(True)), repr(persist)
        assert isinstance(truncate, type(True)), repr(truncate)
        selector = self._expr_to_selector(selector)
        assert isinstance(selector, (selectortools.Selector, type(None))), repr(selector)
        #self._debug(source, 'set_attribute')
        source = requesttools.source_to_request(source, callback=callback, count=count, offset=offset)
        #self._debug(source, 'request')
        multiple_context_setting = settingtools.MultipleContextSetting(attribute, source, selector,
            context_names=contexts, persist=persist, truncate=truncate)
        #self._debug(multiple_context_setting, 'mcs')
        #print ''
        self.multiple_context_settings.append(multiple_context_setting)
        return multiple_context_setting

    def _set_attribute_new(self, attribute, source, selector=None, contexts=None,
        callback=None, count=None, offset=None, persist=True, truncate=False):
        contexts = self._context_token_to_context_names(contexts)
        selector = selectortools.TimespanSelector(selector)
        return self._set_attribute(attribute, selector, source,
            callback=callback, contexts=contexts, count=count, 
            offset=offset, persist=persist, truncate=truncate)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def context_names(self):
        r'''Segment specification context names::

            >>> segment.context_names
            ['Voice 1', 'Voice 2', 'Voice 3', 'Voice 4']

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
            'Staff 2'
            'Staff 3'
            'Staff 4'
            'Voice 1'
            'Voice 2'
            'Voice 3'
            'Voice 4'

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
            'Staff 2'
            'Staff 3'
            'Staff 4'
            'Voice 1'
            'Voice 2'
            'Voice 3'
            'Voice 4'

        Return context proxy dictionary.
        '''
        return Specification.resolved_single_context_settings.fget(self)

    @property
    def score_model(self):
        '''Segment specification score model::

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
            GroupedRhythmicStavesScoreTemplate(staff_count=4)

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
            SegmentItemSelector(identifier='red')

        Return selector.
        '''
        return selectortools.SegmentItemSelector(identifier=self.segment_name)

    @property
    def single_context_settings(self):
        r'''Segment specification single-context settings::

            >>> segment.single_context_settings
            SingleContextSettingInventory([])

        Return single-context setting inventory.
        '''
        return Specification.single_context_settings.fget(self)

    @property
    def start_timepoint(self):
        '''Segment specification start timepoint.

            >>> segment.start_timepoint
            Timepoint(anchor=SegmentItemSelector(identifier='red'), edge=Left)

        Return timepoint.
        '''
        return timespantools.Timepoint(anchor=self.selector, edge=Left)

    @property
    def stop_timepoint(self):
        '''Segment specification stop timepoint.

            >>> segment.stop_timepoint
            Timepoint(anchor=SegmentItemSelector(identifier='red'), edge=Right)

        Return timepoint.
        '''
        return timespantools.Timepoint(anchor=self.selector, edge=Right)

    @property
    def storage_format(self):
        r'''Segment specification storage format::

            >>> z(segment)
            specificationtools.SegmentSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
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
        assert isinstance(resolved_single_context_setting.resolved_value, list), repr(
            resolved_single_context_setting.resolved_value)
        return resolved_single_context_setting.resolved_value

    @property
    def timespan(self):
        '''Segment specification timespan.

            >>> segment.timespan
            SingleSourceTimespan(selector=SegmentItemSelector(identifier='red'))

        Return timespan.
        '''
        return timespantools.SingleSourceTimespan(selector=self.selector)

    ### PUBLIC METHODS ###

    def request_time_signatures(self, context_name=None, callback=None, count=None, offset=None):
        r'''Select time signatures in `context_name` that start during segment::

            >>> request = segment.request_time_signatures()

        ::

            >>> z(request)
            requesttools.AttributeRequest(
                'time_signatures',
                selectortools.SegmentItemSelector(
                    identifier='red'
                    )
                )

        Return attribute request.
        '''
        selector = self.select_segment()
        return requesttools.AttributeRequest('time_signatures', selector,
            context_name=context_name, callback=callback, count=count, offset=offset)

    def select_background_measure(self, n):
        '''Select background measure `n` that starts during segment::

            >>> selector = segment.select_background_measure(0)

        ::

            >>> z(selector)
            selectortools.BackgroundMeasureSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                start_identifier=0,
                stop_identifier=1
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        start, stop = n, n + 1
        selector = selectortools.BackgroundMeasureSliceSelector(
            inequality=inequality, start_identifier=start, stop_identifier=stop)
        return selector

    def select_background_measures(self, start=None, stop=None):
        '''Select the first five background measures that start during segment::

            >>> selector = segment.select_background_measures(stop=5)

        ::

            >>> z(selector)
            selectortools.BackgroundMeasureSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=5
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.BackgroundMeasureSliceSelector(
            inequality=inequality, start_identifier=start, stop_identifier=stop)
        return selector
    
    def select_background_measures_ratio_part(self, ratio, part, is_count=True):
        r'''Select the first third of background measures starting during segment::

            >>> selector = segment.select_background_measures_ratio_part((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.CountRatioPartSelector(
                selectortools.BackgroundMeasureSliceSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentItemSelector(
                                identifier='red'
                                )
                            )
                        )
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        selector = self.select_background_measures()
        if is_count:
            selector = selectortools.CountRatioPartSelector(selector, ratio, part)
        else:
            selector = selectortools.TimeRatioPartSelector(selector, ratio, part)
        return selector

    def select_division(self, voice, n):
        '''Select `voice` division `n` that starts during segment::

            >>> selector = segment.select_division('Voice 1', 0)

        ::
            
            >>> z(selector)
            selectortools.DivisionSliceSelector(
                'Voice 1',
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                start_identifier=0,
                stop_identifier=1
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        start, stop = n, n + 1
        selector = selectortools.DivisionSliceSelector(
            voice, inequality=inequality, start_identifier=start, stop_identifier=stop)
        return selector

    def select_divisions(self, voice, start=None, stop=None):
        '''Select the first five ``'Voice 1'`` divisions that start during segment::

            >>> selector = segment.select_divisions('Voice 1', stop=5)

        ::
            
            >>> z(selector)
            selectortools.DivisionSliceSelector(
                'Voice 1',
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=5
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.DivisionSliceSelector(voice,
            inequality=inequality, start_identifier=start, stop_identifier=stop)
        return selector

    def select_divisions_ratio_part(self, voice, ratio, part, is_count=True):
        r'''Select the first third of ``'Voice 1'`` divisions starting during segment::

            >>> selector = segment.select_divisions_ratio_part('Voice 1', (1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.CountRatioPartSelector(
                selectortools.DivisionSliceSelector(
                    'Voice 1',
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentItemSelector(
                                identifier='red'
                                )
                            )
                        )
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        selector = self.select_divisions(voice)
        if is_count:
            selector = selectortools.CountRatioPartSelector(selector, ratio, part)
        else:
            selector = selectortools.TimeRatioPartSelector(selector, ratio, part)
        return selector

    def select_leaves(self, start=None, stop=None):
        '''Select the first ``40`` leaves that start during segment::

            >>> selector = segment.select_leaves(stop=40)

        ::

            >>> z(selector)
            selectortools.CounttimeComponentSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                klass=leaftools.Leaf,
                stop_identifier=40
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.CounttimeComponentSliceSelector(
            inequality=inequality, klass=leaftools.Leaf, 
            start_identifier=start, stop_identifier=stop)
        return selector

    def select_leaves_ratio_part(self, ratio, part, is_count=True):
        r'''Select the first third of leaves starting during segment::

            >>> selector = segment.select_leaves_ratio_part((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.CountRatioPartSelector(
                selectortools.CounttimeComponentSliceSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentItemSelector(
                                identifier='red'
                                )
                            )
                        ),
                    klass=leaftools.Leaf
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        selector = self.select_leaves()
        if is_count:
            selector = selectortools.CountRatioPartSelector(selector, ratio, part)
        else:
            selector = selectortools.TimeRatioPartSelector(selector, ratio, part)
        return selector

    def select_notes_and_chords(self, start=None, stop=None):
        '''Select the first ``40`` notes and chords that start during segment.

            >>> selector = segment.select_notes_and_chords(stop=40)

        ::

            >>> z(selector)
            selectortools.CounttimeComponentSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                klass=helpertools.KlassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                stop_identifier=40
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.CounttimeComponentSliceSelector(
            inequality=inequality, klass=(notetools.Note, chordtools.Chord),
            start_identifier=start, stop_identifier=stop)
        return selector

    def select_notes_and_chords_ratio_part(self, ratio, part, is_count=True):
        r'''Select the first third of notes and chords starting during segment::

            >>> selector = segment.select_notes_and_chords_ratio_part((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.CountRatioPartSelector(
                selectortools.CounttimeComponentSliceSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentItemSelector(
                                identifier='red'
                                )
                            )
                        ),
                    klass=helpertools.KlassInventory([
                        notetools.Note,
                        chordtools.Chord
                        ])
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        selector = self.select_notes_and_chords()
        if is_count:
            selector = selectortools.CountRatioPartSelector(selector, ratio, part)
        else:
            selector = selectortools.TimeRatioPartSelector(selector, ratio, part)
        return selector

    def select_segment(self):
        return selectortools.SegmentItemSelector(identifier=self.segment_name)

    def select_segment_timespan(self):
        '''Select contexts::

            >>> selector = segment.select_segment_timespan()

        ::

            >>> z(selector)
            selectortools.TimespanSelector(
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    )
                )

        Return timespan selector.
        '''
        return selectortools.TimespanSelector(self.timespan)

    def select_segment_timespan_ratio_part(self, ratio, part):
        r'''Select the first third of segment ``'red'``::

            >>> selector = segment.select_segment_timespan_ratio_part((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.TimeRatioPartSelector(
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        identifier='red'
                        )
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return duration-ratio part selector.
        '''
        return selectortools.TimeRatioPartSelector(self.timespan, ratio, part)

    def set_aggregate(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set aggregate of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'aggregate'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_articulations(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set articulations of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'articulations'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_chord_treatment(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set chord treatment of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'chord_treatment'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_divisions(self, source, selector=None, contexts=None,
        callback=None, count=None, offset=None, persist=True, truncate=False):
        r'''Set divisions of segment `contexts` to `source`::

            >>> setting = segment.set_divisions([(3, 16)], contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                'divisions',
                [(3, 16)],
                selectortools.TimespanSelector(
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                context_names=['Voice 1', 'Voice 3'],
                persist=True,
                truncate=False
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        selector = selector or self.select_segment_timespan()
        contexts = contexts or [self.score_name]
        return self._set_attribute_new(
            'divisions',
            source, selector=selector, contexts=contexts,
            callback=callback, count=count, offset=offset,
            persist=persist, truncate=truncate,
            )

    def set_dynamics(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set dynamics of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'dynamics'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_marks(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set marks of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'marks'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_markup(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set markup of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'markup'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_pitch_classes(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set pitch-classes of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_classes'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_pitch_class_application(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set pitch-class application of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_application'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_pitch_class_transform(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set pitch-class transform of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_transform'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_registration(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set registration of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'registration'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_rhythm(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set rhythm of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        contexts = contexts or self
        attribute = 'rhythm'
        return self._set_attribute(attribute, contexts, source, 
            contexts=contexts, count=count, offset=offset, persist=persist)

    def set_retrograde_divisions(self, source, contexts=None,
        count=None, offset=None, persist=True, truncate=True):
        r'''Set divisions of segment `contexts` to retrograde `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        string = 'sequencetools.reverse_sequence'
        contexts = contexts or self
        callback = helpertools.Callback(eval(string), string)
        return self.set_divisions(source, contexts=contexts,
            callback=callback, count=count, offset=offset, persist=persist, truncate=truncate)

    def set_rotated_divisions(self, source, n, contexts=None,
        count=None, offset=None, persist=True, truncate=True):
        r'''Set divisions of segment `contexts` to `source` rotated by integer `n`.

        Create, store and return ``MultipleContextSetting``.
        '''
        assert isinstance(n, int), repr(n)
        contexts = contexts or self
        string = 'lambda x: sequencetools.rotate_sequence(x, {})'.format(n)
        callback = helpertools.Callback(eval(string), string)
        return self.set_divisions(source, contexts=contexts,
            callback=callback, count=count, offset=offset, persist=persist, truncate=truncate)

    def set_tempo(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set tempo of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'tempo'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_time_signatures(self, source, contexts=None,
        count=None, persist=True, offset=None):
        r'''Set time signatures according to `source` for segment `contexts`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'time_signatures'
        contexts = contexts or self
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)
