from abjad.tools import *
from specificationtools.exceptions import *
from specificationtools.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from specificationtools.AttributeRetrievalRequest import AttributeRetrievalRequest
from specificationtools.Callback import Callback
from specificationtools.Directive import Directive
from specificationtools.DirectiveInventory import DirectiveInventory
from specificationtools.DivisionRetrievalRequest import DivisionRetrievalRequest
from specificationtools.HandlerRequest import HandlerRequest
from specificationtools.ResolvedSetting import ResolvedSetting
from specificationtools.Scope import Scope
from specificationtools.Specification import Specification
from specificationtools.Selection import Selection
from specificationtools.StatalServer import StatalServer
from specificationtools.StatalServerRequest import StatalServerRequest
from handlers.Handler import Handler
import copy


class SegmentSpecification(Specification):

    ### INITIALIZER ###

    def __init__(self, score_template, name):
        assert isinstance(name, str), name
        Specification.__init__(self, score_template)
        self._score_model = self.score_template()
        self._name = name
        self._directives = DirectiveInventory()

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
        return self._directives

    @property
    def duration(self):
        if self.time_signatures is not None:
            return sum([durationtools.Duration(x) for x in self.time_signatures])        

    @property
    def name(self):
        return self._name

    @property
    def score_model(self):
        return self._score_model

    @property
    def time_signatures(self):
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

    def get_directives(self, target_selection=None, attribute_name=None):
        result = []
        for directive in self.directives:
            if target_selection is None or directive.target_selection == target_selection:
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
        import specificationtools.library as library
        value, fresh = self.get_resolved_value_with_fresh('rhythm', context_name, scope=scope)
        if value is not None:
            return value, fresh
        return library.rest_filled_tokens, True

    # TODO: remove this and just call self.settings.get_setting() directly
    def get_setting(self, **kwargs):
        '''Return unresolved setting.
        '''
        return self.settings.get_setting(segment_name=self.name, **kwargs)

    # TODO: remove this and just call self.settings.get_settings() directly
    def get_settings(self, **kwargs):
        '''Return unresolved setting.
        '''
        return self.settings.get_settings(segment_name=self.name, **kwargs)

    def parse_context_token(self, context_token):
        if context_token in self.context_names:
            context_names = [context_token]
        elif self.resolved_settings_context_dictionary.all_are_context_names(context_token):
            context_names = context_token
        elif isinstance(context_token, type(self)):
            context_names = None
        else:
            raise ValueError('invalid context token: {!r}'.format(context_token))
        return context_names
            
    def parse_selection_token(self, selection_token):
        if isinstance(selection_token, Selection):
            selection = selection_token
        elif isinstance(selection_token, type(self)):
            selection = self.select()
        elif isinstance(selection_token, str) and selection_token in self.resolved_settings_context_dictionary:
            selection = self.select(context_names=[selection_token])
        elif self.resolved_settings_context_dictionary.all_are_context_names(selection_token):
            selection = self.select(context_names=selection_token)
        else:
            raise ValueError('invalid selection token: {!r}.'.format(selection_token))
        return selection

    # TODO: rename to something more explicit
    def retrieve(self, attribute_name, **kwargs):
        return Specification.retrieve(self, attribute_name, self.name, **kwargs)

    def retrieve_resolved_value(self, attribute_name, **kwargs):
        return Specification.retrieve_resolved_value(self, attribute_name, self.name, **kwargs)

    def select(self, context_names=None, segment_name=None, scope=None):
        assert context_names is None or self.resolved_settings_context_dictionary.all_are_context_names(
            context_names)
        assert isinstance(segment_name, (str, type(None)))
        assert isinstance(scope, (Scope, type(None)))
        segment_name = segment_name or self.name
        selection = Selection(segment_name, context_names=context_names, scope=scope)
        return selection

    def select_divisions(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = 'divisions'
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, segment_name=segment_name, scope=scope)
        return selection

    def select_measures(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = 'measures'
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, segment_name=segment_name, scope=scope)
        return selection
    
    def select_notes_and_chords(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = (chordtools.Chord, notetools.Note)
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, scope=scope)
        return selection

    def set_aggregate(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'aggregate'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_articulations(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'articulations'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_attribute(self, attribute_name, target_token, source, 
        callback=None, count=None, offset=None, persistent=True, truncate=False):
        assert attribute_name in self.attribute_names, attribute_name
        assert isinstance(count, (int, type(None))), count
        assert isinstance(persistent, type(True)), persistent
        assert isinstance(truncate, type(True)), truncate
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, callback=callback, count=count, offset=offset)
        directive = Directive(target_selection, attribute_name, source, 
            persistent=persistent, truncate=truncate)
        self.directives.append(directive)
        return directive

    def set_chord_treatment(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'chord_treatment'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_divisions(self, target_token, source, 
        callback=None, count=None, offset=None, persistent=True, truncate=False):
        attribute_name = 'divisions'
        return self.set_attribute(attribute_name, target_token, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, truncate=truncate)

    def set_divisions_rotated_by_count(self, target_token, source, n, 
        count=None, offset=None, persistent=True, truncate=True):
        assert isinstance(n, int)
        string = 'lambda x: sequencetools.rotate_sequence(x, {})'.format(n)
        callback = Callback(eval(string), string)
        return self.set_divisions(target_token, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, truncate=truncate)

    def set_duration_in_seconds(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'duration_in_seconds'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_dynamics(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'dynamics'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_marks(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'marks'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_markup(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'markup'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_pitch_classes(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_classes'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_pitch_class_application(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_class_application'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_pitch_class_transform(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_class_transform'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_register(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'register'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_rhythm(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'rhythm'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_tempo(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'tempo'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_time_signatures(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'time_signatures'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_written_duration(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'written_duration'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def unpack_directives(self):
        for directive in self.directives:
            self.settings.extend(directive.unpack())
        return self.settings
