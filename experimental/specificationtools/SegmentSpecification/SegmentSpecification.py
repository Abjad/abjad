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

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
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

    ### PRIVATE METHODS ###

    def _expr_to_selector(self, expr):
        r'''Return `expr` when `expr` is already a selector.
        Otherwise assume `expr` to be contexts and create and 
        return a multiple-context timespan selector.
        '''
        if isinstance(expr, selectortools.Selector):
            return expr
        elif isinstance(expr, (str, list, type(self))):
            return self.select_timespan(contexts=expr)

    def _set_attribute(self, attribute, target, source, 
        callback=None, count=None, offset=None, persist=True, truncate=False):
        r'''Generalized method to create ``MultipleContextSetting`` objects.
        Select `attribute` from `source` and set on `target`.
        All other set methods call this method.
        Create, store and return ``MultipleContextSetting``.
        '''
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(persist, type(True)), repr(persist)
        assert isinstance(truncate, type(True)), repr(truncate)
        target = self._expr_to_selector(target)
        source = requesttools.source_to_request(source, callback=callback, count=count, offset=offset)
        multiple_context_setting = settingtools.MultipleContextSetting(attribute, source, target,
            persist=persist, truncate=truncate)
        self.multiple_context_settings.append(multiple_context_setting)
        return multiple_context_setting

    def _set_attribute_new(self, attribute, source, timespan=None, contexts=None,
        callback=None, count=None, offset=None, persist=True, truncate=False):
        target = selectortools.MultipleContextTimespanSelector(contexts=contexts, timespan=timespan)
        return self._set_attribute(attribute, target, source,
            callback=callback, count=count, offset=offset, persist=persist, truncate=truncate)

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

    def request_time_signatures(self, context_name=None, callback=None, count=None, offset=None):
        r'''Select time signatures in `context_name` that start during segment::

            >>> segment.request_time_signatures()
            AttributeRequest('time_signatures', 'red')

        Return attribute request.
        '''
        return requesttools.AttributeRequest('time_signatures', self.segment_name, 
            context_name=context_name, callback=callback, count=count, offset=offset)

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

    def select_ratio_of_background_measures(self, ratio, index=0, is_count=True):
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
        if is_count:
            selector = selectortools.CountRatioItemSelector(selector, ratio, index=index)
        else:
            selector = selectortools.DurationRatioItemSelector(selector, ratio, index=index)
        return selector

    def select_ratio_of_divisions(self, ratio, index, contexts=None, is_count=True):
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
        if is_count:
            selector = selectortools.CountRatioItemSelector(selector, ratio, index=index)
        else:
            selector = selectortools.DurationRatioItemSelector(selector, ratio, index=index)
        return selector

    def select_ratio_of_leaves(self, ratio, index, contexts=None, is_count=True):
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
        if is_count:
            selector = selectortools.CountRatioItemSelector(selector, ratio, index=index)
        else:
            selector = selectortools.DurationRatioItemSelector(selector, ratio, index=index)
        return selector

    def select_ratio_of_notes_and_chords(self, ratio, index, contexts=None, is_count=True):
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
        if is_count:
            selector = selectortools.CountRatioItemSelector(selector, ratio, index=index)
        else:
            selector = selectortools.DurationRatioItemSelector(selector, ratio, index=index)
        return selector

    def select_segment_duration_ratio_item(self, ratio, item):
        r'''Select the first third of segment ``'red'``::

            >>> selector = segment.select_segment_duration_ratio_item((1, 1, 1), 0)

        ::

            >>> z(selector)
            selectortools.DurationRatioItemSelector(
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    ),
                mathtools.Ratio(1, 1, 1),
                index=0
                )

        Return duration-ratio item selector.
        '''
        return selectortools.DurationRatioItemSelector(self.timespan, ratio, index=item)

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

        Return multiple-context timespan selector.
        '''
        contexts = self._context_token_to_context_names(contexts)
        return selectortools.MultipleContextTimespanSelector(contexts=contexts, timespan=self.timespan)

    def set_aggregate(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set aggregate of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'aggregate'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_articulations(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set articulations of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'articulations'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_chord_treatment(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set chord treatment of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'chord_treatment'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_divisions(self, contexts, source, 
        callback=None, count=None, offset=None, persist=True, truncate=False):
        r'''Set divisions of segment `contexts` to `source`::

            >>> setting = segment.set_divisions(['Voice 1', 'Voice 3'], [(3, 16)])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                'divisions',
                [(3, 16)],
                selectortools.MultipleContextTimespanSelector(
                    contexts=['Voice 1', 'Voice 3'],
                    timespan=timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    ),
                persist=True,
                truncate=False
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'divisions'
        return self._set_attribute(attribute, contexts, source, 
            callback=callback, count=count, offset=offset, persist=persist, truncate=truncate)

    def set_divisions_new(self, source, timespan=None, contexts=None,
        callback=None, count=None, offset=None, persist=True, truncate=False):
        r'''New and improved division-setting method.

        Create, store and return ``MultipleContextSetting``.
        '''
        return self._set_attribute_new(
            'divisions',
            source, timespan=timespan, contexts=contexts,
            callback=callback, count=count, offset=offset,
            persist=persist, truncate=truncate,
            )

    def set_dynamics(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set dynamics of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'dynamics'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_marks(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set marks of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'marks'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_markup(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set markup of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'markup'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_pitch_classes(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set pitch-classes of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_classes'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_pitch_class_application(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set pitch-class application of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_application'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_pitch_class_transform(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set pitch-class transform of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_transform'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_registration(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set registration of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'registration'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_rhythm(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set rhythm of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'rhythm'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_retrograde_divisions(self, contexts, source,
        count=None, offset=None, persist=True, truncate=True):
        r'''Set divisions of segment `contexts` to retrograde `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        string = 'sequencetools.reverse_sequence'
        callback = helpertools.Callback(eval(string), string)
        return self.set_divisions(contexts, source, 
            callback=callback, count=count, offset=offset, persist=persist, truncate=truncate)

    def set_rotated_divisions(self, contexts, source, n, 
        count=None, offset=None, persist=True, truncate=True):
        r'''Set divisions of segment `contexts` to `source` rotated by integer `n`.

        Create, store and return ``MultipleContextSetting``.
        '''
        assert isinstance(n, int), repr(n)
        string = 'lambda x: sequencetools.rotate_sequence(x, {})'.format(n)
        callback = helpertools.Callback(eval(string), string)
        return self.set_divisions(contexts, source, 
            callback=callback, count=count, offset=offset, persist=persist, truncate=truncate)

    def set_tempo(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set tempo of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'tempo'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)

    def set_time_signatures(self, contexts, source, 
        count=None, persist=True, offset=None):
        r'''Set time signatures of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'time_signatures'
        return self._set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persist=persist)
