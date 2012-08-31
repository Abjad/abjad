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

    def _store_multiple_context_setting(self, attribute, source,
        callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        source = requesttools.source_to_request(source, 
            callback=callback, count=count, offset=offset, reverse=reverse)
        contexts = self._context_token_to_context_names(contexts)
        selector = selector or self.select_segment()
        multiple_context_setting = settingtools.MultipleContextSetting(
            attribute, 
            source, 
            selector,
            context_names=contexts, 
            persist=persist, 
            truncate=truncate
            )
        self.multiple_context_settings.append(multiple_context_setting)
        return multiple_context_setting

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def abbreviated_context_names(self):
        r'''Segment specification abbreviated context names::

            >>> segment.abbreviated_context_names
            ['Voice 1', 'Voice 2', 'Voice 3', 'Voice 4']

        Return list of strings.
        '''
        return Specification.abbreviated_context_names.fget(self)

    @property
    def context_names(self):
        r'''Segment specification context names::

            >>> for x in segment.context_names:
            ...     x
            ... 
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Voice 1'
            'Staff 2'
            'Voice 2'
            'Staff 3'
            'Voice 3'
            'Staff 4'
            'Voice 4'

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
            Timepoint(anchor=SingleSegmentSelector(identifier='red'), edge=Left)

        Return timepoint.
        '''
        selector = self.select_segment()
        return timespantools.Timepoint(anchor=selector, edge=Left)

    @property
    def stop_timepoint(self):
        '''Segment specification stop timepoint.

            >>> segment.stop_timepoint
            Timepoint(anchor=SingleSegmentSelector(identifier='red'), edge=Right)

        Return timepoint.
        '''
        selector = self.select_segment()
        return timespantools.Timepoint(anchor=selector, edge=Right)

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
            SingleSourceTimespan(selector=SingleSegmentSelector(identifier='red'))

        Return timespan.
        '''
        selector = self.select_segment()
        return timespantools.SingleSourceTimespan(selector=selector)

    ### PUBLIC METHODS ###

    def request_divisions(self,  
        context_name=None, callback=None, count=None, offset=None, reverse=None):
        selector = self.select_segment()
        return requesttools.AttributeRequest('divisions', selector,
            context_name=context_name, callback=callback, count=count, offset=offset, reverse=reverse)

    def request_time_signatures(self, 
        context_name=None, callback=None, count=None, offset=None, reverse=None):
        r'''Request segment time signatures in `context_name`::

            >>> request = segment.request_time_signatures()

        ::

            >>> z(request)
            requesttools.AttributeRequest(
                'time_signatures',
                selectortools.SingleSegmentSelector(
                    identifier='red'
                    )
                )

        Return attribute request.
        '''
        selector = self.select_segment()
        return requesttools.AttributeRequest('time_signatures', selector,
            context_name=context_name, callback=callback, count=count, offset=offset, reverse=reverse)

    def select_background_measure(self, n):
        '''Select segment background measure ``0``::

            >>> selector = segment.select_background_measure(0)

        ::

            >>> z(selector)
            selectortools.BackgroundMeasureSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SingleSegmentSelector(
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
        selector = selectortools.BackgroundMeasureSelector(
            inequality=inequality, start_identifier=start, stop_identifier=stop)
        return selector

    def select_background_measures(self, start=None, stop=None):
        '''Select the first five segment background measures::

            >>> selector = segment.select_background_measures(stop=5)

        ::

            >>> z(selector)
            selectortools.BackgroundMeasureSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SingleSegmentSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=5
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.BackgroundMeasureSelector(
            inequality=inequality, start_identifier=start, stop_identifier=stop)
        return selector
    
    def select_background_measures_ratio_part(self, ratio, part, is_count=True):
        r'''Select the first third of segment background measures 
        calculated according to count of segment background measures::

            >>> selector = segment.select_background_measures_ratio_part((1, 1, 1), 0, is_count=True)

        ::

            >>> z(selector)
            selectortools.CountRatioPartSelector(
                selectortools.BackgroundMeasureSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SingleSegmentSelector(
                                identifier='red'
                                )
                            )
                        )
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Select the first third of segment background measures calculcated
        according to duration of segment background measures::

            >>> selector = segment.select_background_measures_ratio_part((1, 1, 1), 0, is_count=False)

        ::

            >>> z(selector)
            selectortools.TimeRatioPartSelector(
                selectortools.BackgroundMeasureSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SingleSegmentSelector(
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
        return self._wrap_selector_with_ratio_part_selector(selector, ratio, part, is_count=is_count)

    def select_division(self, n):
        '''Select segment division ``0``::

            >>> selector = segment.select_division(0)

        ::
            
            >>> z(selector)
            selectortools.DivisionSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SingleSegmentSelector(
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
        selector = selectortools.DivisionSelector(
            inequality=inequality, start_identifier=start, stop_identifier=stop)
        return selector

    def select_divisions(self, start=None, stop=None):
        '''Select the first five segment divisions::

            >>> selector = segment.select_divisions(stop=5)

        ::
            
            >>> z(selector)
            selectortools.DivisionSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SingleSegmentSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=5
                )

        Return selector.
        '''
        inequality = timespantools.expr_starts_during_timespan(self.timespan)
        selector = selectortools.DivisionSelector(
            inequality=inequality, start_identifier=start, stop_identifier=stop)
        return selector

    def select_divisions_ratio_part(self, ratio, part, is_count=True):
        r'''Select the first third of segment divisions::

            >>> selector = segment.select_divisions_ratio_part((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.CountRatioPartSelector(
                selectortools.DivisionSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SingleSegmentSelector(
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
        selector = self.select_divisions()
        return self._wrap_selector_with_ratio_part_selector(selector, ratio, part, is_count=is_count)

    def select_leaves(self, start=None, stop=None):
        '''Select the first ``40`` segment leaves::

            >>> selector = segment.select_leaves(stop=40)

        ::

            >>> z(selector)
            selectortools.CounttimeComponentSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SingleSegmentSelector(
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
        selector = selectortools.CounttimeComponentSelector(
            inequality=inequality, klass=leaftools.Leaf, 
            start_identifier=start, stop_identifier=stop)
        return selector

    def select_leaves_ratio_part(self, ratio, part, is_count=True):
        r'''Select the first third of segment leaves::

            >>> selector = segment.select_leaves_ratio_part((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.CountRatioPartSelector(
                selectortools.CounttimeComponentSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SingleSegmentSelector(
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
        return self._wrap_selector_with_ratio_part_selector(selector, ratio, part, is_count=is_count)

    def select_notes_and_chords(self, start=None, stop=None):
        '''Select the first ``40`` segment notes and chords::

            >>> selector = segment.select_notes_and_chords(stop=40)

        ::

            >>> z(selector)
            selectortools.CounttimeComponentSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SingleSegmentSelector(
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
        selector = selectortools.CounttimeComponentSelector(
            inequality=inequality, klass=(notetools.Note, chordtools.Chord),
            start_identifier=start, stop_identifier=stop)
        return selector

    def select_notes_and_chords_ratio_part(self, ratio, part, is_count=True):
        r'''Select the first third of segment notes and chords::

            >>> selector = segment.select_notes_and_chords_ratio_part((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.CountRatioPartSelector(
                selectortools.CounttimeComponentSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SingleSegmentSelector(
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
        return self._wrap_selector_with_ratio_part_selector(selector, ratio, part, is_count=is_count)

    def select_segment(self):
        '''Select segment::

            >>> selector = segment.select_segment()

        ::

            >>> z(selector)
            selectortools.SingleSegmentSelector(
                identifier='red'
                )

        Return selector.
        '''
        return selectortools.SingleSegmentSelector(identifier=self.segment_name)

    def select_segment_offsets(self, start=None, stop=None):
        r'''Select segment from ``1/8`` to ``3/8``::

            >>> selector = segment.select_segment_offsets(start=(1, 8), stop=(3, 8))

        ::

            >>> z(selector)
            selectortools.OffsetSelector(
                selectortools.SingleSegmentSelector(
                    identifier='red'
                    ),
                start_offset=durationtools.Offset(1, 8),
                stop_offset=durationtools.Offset(3, 8)
                )

        Return selector.
        '''
        selector = self.select_segment()
        return selectortools.OffsetSelector(selector, start_offset=start, stop_offset=stop)

    def select_segment_ratio_part(self, ratio, part):
        r'''Select the first third of segment::

            >>> selector = segment.select_segment_ratio_part((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.TimeRatioPartSelector(
                selectortools.SingleSegmentSelector(
                    identifier='red'
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        selector = self.select_segment()
        return selectortools.TimeRatioPartSelector(selector, ratio, part)

    def set_aggregate(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set aggregate of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'aggregate'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_articulations(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set articulations of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'articulations'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_chord_treatment(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set chord treatment of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'chord_treatment'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_divisions(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set divisions of segment `contexts` to `source`::

            >>> setting = segment.set_divisions([(3, 16)], contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                'divisions',
                [(3, 16)],
                selectortools.SingleSegmentSelector(
                    identifier='red'
                    ),
                context_names=['Voice 1', 'Voice 3'],
                persist=True,
                truncate=False
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'divisions'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_dynamics(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set dynamics of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'dynamics'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_marks(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set marks of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'marks'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_markup(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set markup of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'markup'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_pitch_classes(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set pitch-classes of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_classes'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_pitch_class_application(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set pitch-class application of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_application'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_pitch_class_transform(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set pitch-class transform of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_transform'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_registration(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set registration of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'registration'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_rhythm(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set rhythm of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'rhythm'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_retrograde_divisions(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=True):
        r'''Set divisions of segment `contexts` to retrograde `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        string = 'sequencetools.reverse_sequence'
        callback = helpertools.Callback(eval(string), string)
        return self.set_divisions(source, contexts=contexts,
            callback=callback, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_rotated_divisions(self, source, n, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=True):
        r'''Set divisions of segment `contexts` to `source` rotated by integer `n`.

        Create, store and return ``MultipleContextSetting``.
        '''
        assert isinstance(n, int), repr(n)
        string = 'lambda x: sequencetools.rotate_sequence(x, {})'.format(n)
        callback = helpertools.Callback(eval(string), string)
        return self.set_divisions(source, contexts=contexts,
            callback=callback, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_tempo(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set tempo of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'tempo'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset, 
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)

    def set_time_signatures(self, source, callback=None, contexts=None, count=None, 
        offset=None, persist=True, reverse=None, selector=None, truncate=False):
        r'''Set time signatures according to `source` for segment `contexts`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'time_signatures'
        return self._store_multiple_context_setting(attribute, source,
            callback=callback, contexts=contexts, count=count, offset=offset,
            persist=persist, reverse=reverse, selector=selector, truncate=truncate)
