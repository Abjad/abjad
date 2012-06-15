from abjad.tools import *
from experimental.specificationtools.exceptions import *
from experimental.specificationtools.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from experimental.specificationtools.AttributeRetrievalRequest import AttributeRetrievalRequest
from experimental.specificationtools.Callback import Callback
from experimental.specificationtools.DivisionRetrievalRequest import DivisionRetrievalRequest
from experimental.specificationtools.HandlerRequest import HandlerRequest
from experimental.specificationtools.ResolvedSetting import ResolvedSetting
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
        self._directives = specificationtools.DirectiveInventory()

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
            DirectiveInventory([])

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

    @property
    def indicator(self):
        '''Segment score object indicator.

            >>> segment.indicator
            ScoreObjectIndicator(segment='1')

        Return score object indicator.
        '''
        from experimental import specificationtools
        return specificationtools.ScoreObjectIndicator(segment=self)
        
    @property
    def name(self):
        '''Segment name.

            >>> segment.name
            '1'

        Return string.
        '''
        return self._name

    @property
    def scope(self):
        '''Segment temporal scope.

            >>> segment.scope
            TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Left), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Right))

        Return temporal scope.
        '''
        from experimental import specificationtools
        return specificationtools.TemporalScope(start=self.start, stop=self.stop)

    @property
    def score_model(self):
        '''Segment score model specified by user.

            >>> segment.score_model
            Score-"Grouped Rhythmic Staves Score"<<1>>

        Return Abjad score object.
        '''
        return self._score_model

    @property
    def start(self):
        '''Segment start cursor.

            >>> segment.start
            TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Left)

        Return temporal cursor.
        '''
        from experimental import specificationtools
        return specificationtools.TemporalCursor(anchor=self.indicator, edge=Left)

    @property
    def stop(self):
        '''Segment stop cursor.

            >>> segment.stop
            TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Right)

        Return temporal cursor.
        '''
        from experimental import specificationtools
        return specificationtools.TemporalCursor(anchor=self.indicator, edge=Right)

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
                attribute_name='time_signatures')
        except MissingSettingError:
            return None
        assert isinstance(setting.value, list), setting.value
        return setting.value

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
        elif isinstance(source, DivisionRetrievalRequest):
            if any([x is not None for x in (callback, count, offset)]):
                source = copy.copy(source)
                source.callback = callback
                source.count = count
                source.offset = offset
        elif any([x is not None for x in (callback, count, offset)]):
            raise ValueError("'callback', 'count' or 'offset' set on nonstatal source: {!r}.".format(source))
        return source

    def get_directives(self, target=None, attribute_name=None):
        result = []
        for directive in self.directives:
            if target is None or directive.target == target:
                if attribute_name is None or directive.attribute_name == attribute_name:
                    result.append(directive)
        return result

    def get_divisions_value_with_fresh_and_truncate(self, context_name, scope=None):
        '''Return value found in context tree or else default to segment time signatures.
        '''
        value, fresh, truncate = self.get_resolved_value_with_fresh('divisions', context_name, 
            include_truncate=True, scope=scope)
        if value is None:
            value, fresh = self.get_resolved_value_with_fresh('time_signatures', context_name, 
            scope=scope)
            truncate = False
        return value, fresh, truncate

    def get_resolved_value_with_fresh(self, attribute_name, context_name, include_truncate=False, scope=None):
        '''Return value from resolved setting because context proxy stores resolved settings.
        '''
        #self._debug((attribute_name, context_name))
        context = componenttools.get_first_component_in_expr_with_name(self.score_model, context_name)
        for component in componenttools.get_improper_parentage_of_component(context):
            #self._debug(component)
            context_proxy = self.resolved_settings_context_dictionary[component.name]
            settings = context_proxy.get_settings(attribute_name=attribute_name, scope=scope)
            #self._debug(settings, 'settings')
            if not settings:
                continue
            elif len(settings) == 1:
                setting = settings[0]
                assert isinstance(setting, ResolvedSetting)
                if include_truncate:
                    return setting.value, setting.fresh, setting.truncate
                else:
                    return setting.value, setting.fresh
            else:
                raise Exception('multiple {!r} settings found.'.format(attribute_name))
        if include_truncate:
            return None, None, False
        else:
            return None, None
    
    def get_rhythm_value(self, context_name, scope=None):
        '''Default to rest-filled tokens if explicit rhythm not found.
        '''
        from experimental.specificationtools import library
        value, fresh = self.get_resolved_value_with_fresh('rhythm', context_name, scope=scope)
        if value is not None:
            return value, fresh
        return library.rest_filled_tokens, True

    # TODO: rename to something more explicit
    def retrieve(self, attribute_name, **kwargs):
        return Specification.retrieve(self, attribute_name, self.name, **kwargs)

    def retrieve_resolved_value(self, attribute_name, **kwargs):
        return Specification.retrieve_resolved_value(self, attribute_name, self.name, **kwargs)

    def select(self):
        '''Select all segment contexts over timespan of segment.
        '''
        from experimental import specificationtools
        return specificationtools.Selection()
        
    #def select_contexts(self, contexts=None, segment_name=None):
    def select_contexts(self, contexts=None):
        from experimental import specificationtools
        #assert contexts is None or self.resolved_settings_context_dictionary.all_are_context_names(contexts)
        #assert isinstance(segment_name, (str, type(None)))
        #segment_name = segment_name or self.name
        #selection = specificationtools.Selection(segment_name, contexts=contexts)
        contexts = self.context_token_to_context_names(contexts)
        return specificationtools.Selection(contexts=contexts, scope=self.scope)

    def select_divisions(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        from experimental import specificationtools
        criterion = 'divisions'
        contexts = self.context_token_to_context_names(context_token)
        scope = specificationtools.TemporalScope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(contexts=contexts, segment_name=segment_name, scope=scope)
        return selection

    def select_measures(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        from experimental import specificationtools
        criterion = 'measures'
        contexts = self.context_token_to_context_names(context_token)
        scope = specificationtools.TemporalScope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(contexts=contexts, segment_name=segment_name, scope=scope)
        return selection
    
    def select_notes_and_chords(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        from experimental import specificationtools
        criterion = (chordtools.Chord, notetools.Note)
        contexts = self.context_token_to_context_names(context_token)
        scope = specificationtools.TemporalScope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(contexts=contexts, scope=scope)
        return selection

    def set_aggregate(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'aggregate'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_articulations(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'articulations'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_attribute(self, attribute_name, contexts, source, 
        callback=None, count=None, offset=None, persistent=True, scope=None, truncate=False):
        from experimental import specificationtools
        assert attribute_name in self.attribute_names, repr(attribute_name)
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(persistent, type(True)), repr(persistent)
        assert isinstance(scope, (specificationtools.TemporalScope, type(None))), repr(scope)
        assert isinstance(truncate, type(True)), repr(truncate)
        # handle scope here and include in target selection?
        #target = self.parse_selection_token(contexts)
        target = self.select_contexts(contexts=contexts)
        source = self.annotate_source(source, callback=callback, count=count, offset=offset)
        directive = specificationtools.Directive(target, attribute_name, source, 
            persistent=persistent, truncate=truncate)
        self.directives.append(directive)
        return directive

    def set_chord_treatment(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'chord_treatment'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_divisions(self, contexts, source, 
        callback=None, count=None, offset=None, persistent=True, scope=None, truncate=False):
        attribute_name = 'divisions'
        return self.set_attribute(attribute_name, contexts, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, scope=scope, truncate=truncate)

    def set_duration_in_seconds(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'duration_in_seconds'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_dynamics(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'dynamics'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_marks(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'marks'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_markup(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'markup'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_pitch_classes(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_classes'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_pitch_class_application(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_class_application'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_pitch_class_transform(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_class_transform'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_register(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'register'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_rhythm(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'rhythm'
        return self.set_attribute(attribute_name, contexts, source, 
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
        attribute_name = 'tempo'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_time_signatures(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'time_signatures'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def set_written_duration(self, contexts, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'written_duration'
        return self.set_attribute(attribute_name, contexts, source, 
            count=count, offset=offset, persistent=persistent)

    def unpack_directives(self):
        for directive in self.directives:
            self.settings.extend(directive.unpack())
        return self.settings
