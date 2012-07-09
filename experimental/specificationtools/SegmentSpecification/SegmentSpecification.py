from abjad.tools import *
from experimental.specificationtools.exceptions import *
from experimental.specificationtools.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from experimental.specificationtools.AttributeRetrievalRequest import AttributeRetrievalRequest
from experimental.specificationtools.Callback import Callback
from experimental.specificationtools.DivisionSelector import DivisionSelector
from experimental.specificationtools.HandlerRequest import HandlerRequest
from experimental.specificationtools.ResolvedContextSetting import ResolvedContextSetting
from experimental.specificationtools.Specification import Specification
from experimental.specificationtools.StatalServer import StatalServer
from experimental.specificationtools.StatalServerRequest import StatalServerRequest
from experimental.handlertools.Handler import Handler
import copy


class SegmentSpecification(Specification):
    r'''.. versionadded:: 1.0

    Segment specification.

    Examples::

        >>> from abjad.tools import scoretemplatetools
        >>> from experimental import specificationtools

    The examples below reference the following segment specification::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1)
        >>> specification = specificationtools.ScoreSpecification(score_template=template)
        
    ::
    
        >>> segment = specification.append_segment()

    ::
            
        >>> segment
        SegmentSpecification('1')

    More description goes here.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template, name):
        from experimental import specificationtools
        assert isinstance(name, str), name
        Specification.__init__(self, score_template)
        self._score_model = self.score_template()
        self._name = name
        self._directives = specificationtools.SettingInventory()

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if isinstance(expr, int):
            return self.directives.__getitem__(expr)
        else:
            return self.payload_context_dictionary.__getitem__(expr) 
        
    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def directives(self):
        '''Segment specification directives.

            >>> segment.directives
            SettingInventory([])

        Return directive inventory.
        '''
        return self._directives

    @property
    def duration(self):
        '''Segment specification duration.

            >>> segment.duration is None
            True

        Derived during interpretation.

        Return rational or none.
        '''
        if self.time_signatures is not None:
            return sum([durationtools.Duration(x) for x in self.time_signatures])        

    # TODO: change name to 'selector'
    @property
    def indicator(self):
        '''Segment specification indicator::

            >>> segment.indicator
            SegmentSelector(index='1')

        Return segment selector.
        '''
        from experimental import selectortools
        return selectortools.SegmentSelector(index=self.name)
        
    @property
    def name(self):
        '''Segment name.

            >>> segment.name
            '1'

        Return string.
        '''
        return self._name

    @property
    def score_model(self):
        '''Segment score model specified by user.

            >>> segment.score_model
            Score-"Grouped Rhythmic Staves Score"<<1>>

        Return Abjad score object.
        '''
        return self._score_model

    @property
    def selector(self):
        '''Segment specification selector.

        Return segment selector.

        .. note:: this should replace the ``indicator`` property.
        '''
        return self.indicator

    @property
    def start(self):
        '''Segment start.

            >>> segment.start
            Timepoint(anchor=SegmentSelector(index='1'), edge=Left)

        Return timepoint.
        '''
        from experimental import timespantools
        return timespantools.Timepoint(anchor=self.indicator, edge=Left)

    @property
    def stop(self):
        '''Segment stop.

            >>> segment.stop
            Timepoint(anchor=SegmentSelector(index='1'), edge=Right)

        Return timepoint.
        '''
        from experimental import timespantools
        return timespantools.Timepoint(anchor=self.indicator, edge=Right)

    @property
    def time_signatures(self):
        '''Segment time signatures::

            >>> segment.time_signatures is None
            True

        Derived during interpretation.

        Return list or none.
        '''
        try:
            setting = self.resolved_settings_context_dictionary.score_context_proxy.get_setting(
                attribute='time_signatures')
        except MissingContextSettingError:
            return None
        assert isinstance(setting.value, list), setting.value
        return setting.value

    @property
    def timespan(self):
        '''Segment timespan.

            >>> segment.timespan
            Timespan(selector=SegmentSelector(index='1'))

        Return timespan.
        '''
        from experimental import timespantools
        return timespantools.Timespan(selector=self.selector)

    ### PUBLIC METHODS ###

    def add_time_signatures(self, score):
        time_signatures = self.time_signatures
        if self.time_signatures is not None:
            measures = measuretools.make_measures_with_full_measure_spacer_skips(time_signatures)
            context = componenttools.get_first_component_in_expr_with_name(score, 'TimeSignatureContext')
            context.extend(measures)

    def annotate_source(self, source, callback=None, count=None, offset=None):
        assert isinstance(callback, (Callback, type(None))), callback
        assert isinstance(count, (int, type(None))), count
        assert isinstance(offset, (int, type(None))), offset
        if isinstance(source, StatalServer):
            if count is not None or offset is not None:
                source = StatalServerRequest(source, count=count, offset=offset)
        elif isinstance(source, Handler):
            if offset is not None:
                assert count is None
                source = HandlerRequest(source, offset=offset)
        elif isinstance(source, AttributeRetrievalIndicator):
            if any([x is not None for x in (callback, count, offset)]):
                source = AttributeRetrievalRequest(source, callback=callback, count=count, offset=offset)
        elif isinstance(source, DivisionSelector):
            if any([x is not None for x in (callback, count, offset)]):
                source = copy.copy(source)
                source.callback = callback
                source.count = count
                source.offset = offset
        elif any([x is not None for x in (callback, count, offset)]):
            raise ValueError("'callback', 'count' or 'offset' set on nonstatal source: {!r}.".format(source))
        return source

    def get_directives(self, target=None, attribute=None):
        result = []
        for directive in self.directives:
            if target is None or directive.target == target:
                if attribute is None or directive.attribute == attribute:
                    result.append(directive)
        return result

    def get_divisions_value_with_fresh_and_truncate(self, context_name, timespan=None):
        '''Return value found in context tree or else default to segment time signatures.
        '''
        value, fresh, truncate = self.get_resolved_value_with_fresh('divisions', context_name, 
            include_truncate=True, timespan=timespan)
        if value is None:
            value, fresh = self.get_resolved_value_with_fresh('time_signatures', context_name, 
            timespan=timespan)
            truncate = False
        return value, fresh, truncate

    def get_resolved_value_with_fresh(self, attribute, context_name, include_truncate=False, timespan=None):
        '''Return value from resolved setting because context proxy stores resolved settings.
        '''
        #self._debug((attribute, context_name))
        context = componenttools.get_first_component_in_expr_with_name(self.score_model, context_name)
        for component in componenttools.get_improper_parentage_of_component(context):
            #self._debug(component)
            context_proxy = self.resolved_settings_context_dictionary[component.name]
            settings = context_proxy.get_settings(attribute=attribute, timespan=timespan)
            #self._debug(settings, 'settings')
            if not settings:
                continue
            elif len(settings) == 1:
                setting = settings[0]
                assert isinstance(setting, ResolvedContextSetting)
                if include_truncate:
                    return setting.value, setting.fresh, setting.truncate
                else:
                    return setting.value, setting.fresh
            else:
                raise Exception('multiple {!r} settings found.'.format(attribute))
        if include_truncate:
            return None, None, False
        else:
            return None, None
    
    def get_rhythm_value(self, context_name, timespan=None):
        '''Default to rest-filled tokens if explicit rhythm not found.
        '''
        from experimental.specificationtools import library
        value, fresh = self.get_resolved_value_with_fresh('rhythm', context_name, timespan=timespan)
        if value is not None:
            return value, fresh
        return library.rest_filled_tokens, True

    def retrieve_attribute(self, attribute, **kwargs):
        return Specification.retrieve_attribute(self, attribute, self.name, **kwargs)

    def retrieve_resolved_value(self, attribute, **kwargs):
        return Specification.retrieve_resolved_value(self, attribute, self.name, **kwargs)

    def select(self):
        '''Select all segment contexts over timespan of segment.
        '''
        from experimental import specificationtools
        return specificationtools.Selection()
        
    def select_contexts(self, contexts=None):
        from experimental import specificationtools
        contexts = self.context_token_to_context_names(contexts)
        return specificationtools.Selection(contexts=contexts, timespan=self.timespan)

    # NEXT: rename specificationtools.Selection to specificationtools.MulticontextSelection
    # NEXT: move specificationtools.MulticontextSelection to selectortools
    # NEXT: implement selectortools.MulticontextSelector to complement this
    # NEXT: reimplement the next three methods to return multicontext selectors
    def select_divisions(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        from experimental import specificationtools
        from experimental import timespantools
        criterion = 'divisions'
        contexts = self.context_token_to_context_names(context_token)
        timespan = timespantools.Timespan(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(contexts=contexts, segment_name=segment_name, timespan=timespan)
        return selection

#    def select_measures(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
#        from experimental import specificationtools
#        criterion = 'measures'
#        contexts = self.context_token_to_context_names(context_token)
#        timespan = timespantools.Timespan(criterion=criterion, part=part, start=start, stop=stop)
#        selection = self.select(contexts=contexts, segment_name=segment_name, timespan=timespan)
#        return selection
#    
#    def select_notes_and_chords(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
#        from experimental import specificationtools
#        criterion = (chordtools.Chord, notetools.Note)
#        contexts = self.context_token_to_context_names(context_token)
#        timespan = timespantools.Timespan(criterion=criterion, part=part, start=start, stop=stop)
#        selection = self.select(contexts=contexts, timespan=timespan)
#        return selection

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

    def set_attribute(self, attribute, contexts, source, 
        callback=None, count=None, offset=None, persistent=True, timespan=None, truncate=False):
        from experimental import specificationtools
        from experimental import timespantools
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(persistent, type(True)), repr(persistent)
        assert isinstance(timespan, (timespantools.Timespan, type(None))), repr(timespan)
        assert isinstance(truncate, type(True)), repr(truncate)
        target = self.select_contexts(contexts=contexts)
        source = self.annotate_source(source, callback=callback, count=count, offset=offset)
        directive = specificationtools.Setting(target, attribute, source, 
            persistent=persistent, truncate=truncate)
        self.directives.append(directive)
        return directive

    def set_chord_treatment(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute = 'chord_treatment'
        return self.set_attribute(attribute, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_divisions(self, contexts, source, 
        callback=None, count=None, offset=None, persistent=True, timespan=None, truncate=False):
        attribute = 'divisions'
        return self.set_attribute(attribute, contexts, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, timespan=timespan, truncate=truncate)

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
        callback = Callback(eval(string), string)
        return self.set_divisions(contexts, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, truncate=truncate)

    def set_rotated_divisions(self, contexts, source, n, 
        count=None, offset=None, persistent=True, truncate=True):
        r'''.. versionadded:: 1.0

        Set `contexts` divisions from `source` rotated by integer `n`.
        '''
        assert isinstance(n, int), repr(n)
        string = 'lambda x: sequencetools.rotate_sequence(x, {})'.format(n)
        callback = Callback(eval(string), string)
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

    def unpack_directives(self):
        for directive in self.directives:
            self.settings.extend(directive.unpack())
        return self.settings
