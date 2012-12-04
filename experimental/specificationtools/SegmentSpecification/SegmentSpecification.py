import numbers
from abjad.tools import *
from experimental.exceptions import *
from experimental import helpertools
from experimental import requesttools
from experimental import settingtools
from experimental import symbolictimetools
from experimental.specificationtools.Specification import Specification


class SegmentSpecification(Specification):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    The examples below reference the following segment specification::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        
    ::
    
        >>> red_segment = score_specification.append_segment(name='red')

    ::
            
        >>> red_segment
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
        self._time_signatures = []

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
        contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True, truncate=None):
        request = requesttools.expr_to_request(source)
        context_names = self._context_token_to_context_names(contexts)
        selector = selector or self.select_timespan()
        multiple_context_setting = settingtools.MultipleContextSetting(
            attribute, 
            request, 
            selector,
            start_segment_name=self.segment_name,
            context_names=context_names, 
            index=index,
            count=count,
            reverse=reverse,
            rotation=rotation,
            callback=callback,
            persist=persist, 
            truncate=truncate
            )
        self.multiple_context_settings.append(multiple_context_setting)
        return multiple_context_setting

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def abbreviated_context_names(self):
        r'''Segment specification abbreviated context names::

            >>> red_segment.abbreviated_context_names
            ['Voice 1', 'Voice 2', 'Voice 3', 'Voice 4']

        Return list of strings.
        '''
        return Specification.abbreviated_context_names.fget(self)

    @property
    def context_names(self):
        r'''Segment specification context names::

            >>> for x in red_segment.context_names:
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

            >>> for key in red_segment.contexts:
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

            >>> red_segment.duration
            Duration(0, 1)

        Return duration.
        '''
        return durationtools.Duration(sum([durationtools.Duration(x) for x in self.time_signatures]))

    @property
    def multiple_context_settings(self):
        '''Segment specification multiple-context settings.

            >>> red_segment.multiple_context_settings
            MultipleContextSettingInventory([])

        Return multiple-context setting inventory.
        '''
        return self._multiple_context_settings

    @property
    def score_model(self):
        '''Segment specification score model::

            >>> red_segment.score_model
            Score-"Grouped Rhythmic Staves Score"<<1>>

        Return Abjad score object.
        '''
        return self._score_model

    @property
    def score_name(self):
        r'''Segment specification score name::

            >>> red_segment.score_name
            'Grouped Rhythmic Staves Score'

        Return string.
        '''
        return Specification.score_name.fget(self)

    @property
    def score_template(self):
        r'''Segment specification score template::

            >>> red_segment.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=4)

        Return score template.
        '''
        return Specification.score_template.fget(self)

    @property
    def segment_name(self):
        '''Segment specification name::

            >>> red_segment.segment_name
            'red'

        Return string.
        '''
        return self._segment_name

    @property
    def selector(self):
        '''Segment specification selector::

            >>> red_segment.selector
            SingleSegmentSymbolicTimespan(identifier='red')

        Return single-segment selector.
        '''
        return self.select_timespan()

    @property
    def single_context_settings(self):
        r'''Segment specification single-context settings::

            >>> red_segment.single_context_settings
            SingleContextSettingInventory([])

        Return single-context setting inventory.
        '''
        return Specification.single_context_settings.fget(self)

    @property
    def single_context_settings_by_context(self):
        r'''Segment specification single-context settings by context::

            >>> for key in red_segment.single_context_settings_by_context:
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
        return Specification.single_context_settings_by_context.fget(self)

    @property
    def symbolic_start_offset(self):
        '''Segment specification symbolic start offset::

            >>> red_segment.symbolic_start_offset
            SymbolicOffset(selector=SingleSegmentSymbolicTimespan(identifier='red'), edge=Left)

        Return symbolic offset.
        '''
        selector = self.select_timespan()
        return symbolictimetools.SymbolicOffset(selector=selector, edge=Left)

    @property
    def symbolic_stop_offset(self):
        '''Segment specification symbolic stop offset::

            >>> red_segment.symbolic_stop_offset
            SymbolicOffset(selector=SingleSegmentSymbolicTimespan(identifier='red'), edge=Right)

        Return symbolic offset.
        '''
        selector = self.select_timespan()
        return symbolictimetools.SymbolicOffset(selector=selector, edge=Right)

    @property
    def storage_format(self):
        r'''Segment specification storage format::

            >>> z(red_segment)
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
        '''Time signatures set on segment during time signature interpretation.

                >>> red_segment.time_signatures
                []

        Return list of zero or more nonreduced fractions.
        '''
        return [mathtools.NonreducedFraction(x) for x in self._time_signatures]

    @property
    def timespan(self):
        '''Segment specification timespan.

            >>> red_segment.timespan
            SingleSourceSymbolicTimespan(selector=SingleSegmentSymbolicTimespan(identifier='red'))

        Return timespan.
        '''
        selector = self.select_timespan()
        return symbolictimetools.SingleSourceSymbolicTimespan(selector=selector)

    ### PUBLIC METHODS ###

    # TODO: replace 'selector', 'edge', 'multiplier' keywords and with (symbolic) 'offset' keyword.
    # TODO: simplify by inheriting from Specification. 
    def request_division_command(self, voice, selector=None, 
        edge=None, multiplier=None, addendum=None, 
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment division command active at offset
        in `voice`.

        Example 1. Request division command active at start of segment::

            >>> request = red_segment.request_division_command('Voice 1')

        ::

            >>> z(request)
            requesttools.CommandRequest(
                'divisions',
                symbolictimetools.SymbolicOffset(
                    selector=symbolictimetools.SingleSegmentSymbolicTimespan(
                        identifier='red'
                        )
                    ),
                context_name='Voice 1'
                )

        Example 2. Request division command active halfway through segment::

            >>> request = red_segment.request_division_command('Voice 1', multiplier=Multiplier(1, 2))

        ::

            >>> z(request)
            requesttools.CommandRequest(
                'divisions',
                symbolictimetools.SymbolicOffset(
                    selector=symbolictimetools.SingleSegmentSymbolicTimespan(
                        identifier='red'
                        ),
                    multiplier=durationtools.Multiplier(1, 2)
                    ),
                context_name='Voice 1' 
                )

        Example 3. Request division command active at ``1/4`` 
        after start of measure ``8``::

            >>> selector = red_segment.select_background_measure_timespan(8, 9)
            >>> offset = durationtools.Offset(1, 4)

        ::

            >>> request = red_segment.request_division_command('Voice 1', selector=selector, addendum=offset)

        ::

            >>> z(request)
            requesttools.CommandRequest(
                'divisions',
                symbolictimetools.SymbolicOffset(
                    selector=symbolictimetools.BackgroundMeasureSymbolicTimespan(
                        time_relation=timerelationtools.TimespanTimespanTimeRelation(
                            'timespan_1.start <= timespan_2.start < timespan_1.stop',
                            timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                                selector=symbolictimetools.SingleSegmentSymbolicTimespan(
                                    identifier='red'
                                    )
                                )
                            ),
                        start_identifier=8,
                        stop_identifier=9
                        ),
                    addendum=durationtools.Offset(1, 4)
                    ),
                context_name='Voice 1'
                )

        Specify symbolic offset with `selector`, `edge`, `multiplier`, `offset`.

        Postprocess command with any of `index`, `count`, `reverse`, `callback`.

        Return command request.        
        '''
        selector = selector or self.select_timespan()
        symbolic_offset = symbolictimetools.SymbolicOffset(
            selector=selector, edge=edge, multiplier=multiplier, addendum=addendum)
        return requesttools.CommandRequest(
            'divisions', context_name=voice, symbolic_offset=symbolic_offset,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    # TODO: replace 'selector', 'edge', 'multiplier' keywords and with (symbolic) 'offset' keyword
    def request_rhythm_command(self, voice, 
        selector=None, edge=None, multiplier=None, addendum=None, 
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment rhythm command active at offset in `voice`.

        Example. Request rhythm command active at start of segment::

            >>> request = red_segment.request_rhythm_command('Voice 1')

        ::

            >>> z(request)
            requesttools.CommandRequest(
                'rhythm',
                symbolictimetools.SymbolicOffset(
                    selector=symbolictimetools.SingleSegmentSymbolicTimespan(
                        identifier='red'
                        )
                    ),
                context_name='Voice 1'
                )

        Specify symbolic offset with segment-relative `edge`, `multiplier`, `offset`.

        Postprocess command with any of `index`, `count`, `reverse`, `callback`.

        Return command request.        
        '''
        selector = selector or self.select_timespan()
        symbolic_offset = symbolictimetools.SymbolicOffset(
            selector=selector, edge=edge, multiplier=multiplier, addendum=addendum)
        return requesttools.CommandRequest(
            'rhythm', context_name=voice, symbolic_offset=symbolic_offset,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    # TODO: add voice=None keyword?
    # TODO: replace 'selector', 'edge', 'multiplier' keywords with (symbolic) 'offset' keyword
    # TODO: simplify by inheriting from Specification.
    def request_time_signature_command(self, 
        selector=None, edge=None, multiplier=None, addendum=None, 
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment time signature command active at offset
        in `context`.

        Example. Request time signature command active at start of segment::

            >>> request = red_segment.request_time_signature_command()

        ::

            >>> z(request)
            requesttools.CommandRequest(
                'time_signatures',
                symbolictimetools.SymbolicOffset(
                    selector=symbolictimetools.SingleSegmentSymbolicTimespan(
                        identifier='red'
                        )
                    )
                )

        Specify symbolic offset with segment-relative `edge`, `multiplier`, `offset`.

        Postprocess command with any of `index`, `count`, `reverse`, `callback`.

        Return command request.
        '''
        selector = selector or self.select_timespan()
        symbolic_offset = symbolictimetools.SymbolicOffset(
            selector=selector, edge=edge, multiplier=multiplier, addendum=addendum)
        return requesttools.CommandRequest(
            'time_signatures', context_name=None, symbolic_offset=symbolic_offset,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    def select_timespan(self):
        '''Select segment::

            >>> selector = red_segment.select_timespan()

        ::

            >>> z(selector)
            symbolictimetools.SingleSegmentSymbolicTimespan(
                identifier='red'
                )

        Return selector.
        '''
        return symbolictimetools.SingleSegmentSymbolicTimespan(identifier=self.segment_name)

    def set_aggregate(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set aggregate of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'aggregate'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_articulations(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set articulations of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'articulations'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_chord_treatment(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set chord treatment of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'chord_treatment'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_divisions(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True, truncate=None):
        r'''Set divisions of segment `contexts` to `source`::

            >>> setting = red_segment.set_divisions([(3, 16)], contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                'divisions',
                requesttools.AbsoluteRequest(
                    [(3, 16)]
                    ),
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                start_segment_name='red',
                context_names=['Voice 1', 'Voice 3'],
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'divisions'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            truncate=truncate, persist=persist)

    def set_dynamics(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set dynamics of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'dynamics'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_marks(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set marks of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'marks'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_markup(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set markup of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'markup'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_pitch_classes(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set pitch-classes of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_classes'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_pitch_class_application(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set pitch-class application of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_application'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_pitch_class_transform(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set pitch-class transform of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_transform'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_registration(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set registration of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'registration'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_rhythm(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set rhythm of segment `contexts` to `source`.

            >>> setting = red_segment.set_rhythm(library.sixteenths)

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                'rhythm',
                requesttools.AbsoluteRequest(
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
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                start_segment_name='red',
                context_names=['Grouped Rhythmic Staves Score'],
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'rhythm'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_tempo(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set tempo of segment `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'tempo'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)

    def set_time_signatures(self, source, contexts=None, selector=None,
        index=None, count=None, reverse=None, rotation=None, callback=None,
        persist=True):
        r'''Set time signatures according to `source` for segment `contexts`.

            >>> setting = red_segment.set_time_signatures([(3, 8), (4, 8)])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                'time_signatures',
                requesttools.AbsoluteRequest(
                    [(3, 8), (4, 8)]
                    ),
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                start_segment_name='red',
                context_names=['Grouped Rhythmic Staves Score'],
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'time_signatures'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, selector=selector,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback,
            persist=persist)
