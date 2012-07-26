from abjad.tools import *
from experimental import divisiontools
from experimental import interpretertools
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental.specificationtools.SegmentSpecification import SegmentSpecification
from experimental.specificationtools.SegmentSpecificationInventory import SegmentSpecificationInventory
from experimental.specificationtools.Specification import Specification


class ScoreSpecification(Specification):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    Score specification::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(template)

    With three named segments::

        >>> segment = score_specification.append_segment('red')
        >>> segment = score_specification.append_segment('orange')
        >>> segment = score_specification.append_segment('yellow')

    All score specification properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template):
        Specification.__init__(self, score_template)
        self._segment_specifications = SegmentSpecificationInventory()
        self._segment_specification_class = SegmentSpecification

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if isinstance(expr, int):
            return self.segment_specifications.__getitem__(expr)
        else:
            return self.contexts.__getitem__(expr)

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.segment_specifications)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        r'''Score specification context names::

            >>> score_specification.context_names
            ['Voice 1', 'Voice 2', 'Voice 3', 'Voice 4']

        Only names for which context abbreviations exist are included.

        Return list of strings.
        '''
        return Specification.context_names.fget(self)

    @property
    def contexts(self):
        r'''Score specification context proxy dictionary::

            >>> for key in score_specification.contexts:
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
        r'''Score specification duration::

            >>> score_specification.duration
            Duration(0, 1)

        Return duration.
        '''

        result = []
        for segment_specification in self.segment_specifications:
            duration = segment_specification.duration
            if duration is not None:
                result.append(duration)
        return durationtools.Duration(sum(result))

    @property
    def resolved_single_context_settings(self):
        r'''Score specification resolved single-context settings::

            >>> for key in score_specification.resolved_single_context_settings:
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
    def segment_names(self):
        r'''Score segment names::

            >>> score_specification.segment_names
            ['red', 'orange', 'yellow']

        Return list of zero or more strings.
        '''
        return [segment_specification.name for segment_specification in self.segment_specifications]

    @property
    def segment_specification_class(self):
        r'''Segment specification class of score specification::

            >>> score_specification.segment_specification_class
            <class 'experimental.specificationtools.SegmentSpecification.SegmentSpecification.SegmentSpecification'>
        
        Return segment specification class.
        '''
        return self._segment_specification_class

    @property
    def score_name(self):
        r'''Score specification score name::

            >>> score_specification.score_name
            'Grouped Rhythmic Staves Score'

        Return string.
        '''
        return Specification.score_name.fget(self)
        
    @property
    def score_template(self):
        r'''Score specification score template::

            >>> score_specification.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=4)

        Return score template.
        '''
        return Specification.score_template.fget(self)

    @property
    def segment_specifications(self):
        r'''Segment specifications defined against score specification::

            >>> for segment_specification in score_specification.segment_specifications:
            ...     segment_specification
            ... 
            SegmentSpecification('red')
            SegmentSpecification('orange')
            SegmentSpecification('yellow')

        Return segment specification inventory.
        '''
        return self._segment_specifications

    @property
    def single_context_settings(self):
        r'''Score specification single-context settings::

            >>> score_specification.single_context_settings
            SingleContextSettingInventory([])

        Return single-context setting inventory.
        '''
        return Specification.single_context_settings.fget(self)

    @property
    def storage_format(self):
        r'''Score specification storage format::

            >>> z(score_specification)
            specificationtools.ScoreSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                )

        Return string.
        '''
        return Specification.storage_format.fget(self)

    @property
    def time_signatures(self):
        r'''Score specification time signatures::

            >>> score_specification.time_signatures
            []

        Return list of zero or more time signatures.
        '''
        result = []
        for segment_specification in self.segment_specifications:
            time_signatures = segment_specification.time_signatures
            result.extend(segment_specification.time_signatures)
        return result

    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        name = name or str(self.find_first_unused_segment_number())
        assert name not in self.segment_names, repr(name)
        segment_specification = self.segment_specification_class(self.score_template, name)
        self.segment_specifications.append(segment_specification)
        return segment_specification

    def apply_offset_and_count_to_request(self, request, value):
        if request.offset is not None or request.count is not None:
            original_value_type = type(value)
            offset = request.offset or 0
            count = request.count or 0
            value = sequencetools.CyclicTuple(value)
            if offset < 0:
                offset = len(value) - -offset
            result = value[offset:offset+count]
            result = original_value_type(result)
            return result
        else:
            return value

    def calculate_segment_offset_pairs(self):
        segment_durations = [x.duration for x in self.segment_specifications]
        if sequencetools.all_are_numbers(segment_durations):
            self.segment_durations = segment_durations
            self.score_duration = sum(self.segment_durations)
            self.segment_offset_pairs = mathtools.cumulative_sums_zero_pairwise(self.segment_durations)
    
    def attribute_retrieval_indicator_to_resolved_single_context_setting(self, indicator):
        segment_specification = self.segment_specifications[indicator.segment_name]
        context_proxy = segment_specification.resolved_single_context_settings[indicator.context_name]
        resolved_single_context_setting = context_proxy.get_setting(attribute=indicator.attribute)
        return resolved_single_context_setting

    def clear_persistent_resolved_single_context_settings(self, context_name, attribute):
        if attribute in self.resolved_single_context_settings[context_name]:
            del(self.resolved_single_context_settings[context_name][attribute])

    def find_first_unused_segment_number(self):
        candidate_segment_number = 1
        while True:
            for segment_specification in self.segment_specifications:
                if segment_specification.name == str(candidate_segment_number):
                    candidate_segment_number += 1
                    break
            else:
                return candidate_segment_number

    def get_voice_division_list(self, voice):
        from experimental import specificationtools
        voice_division_list = self.contexts[voice.name].get('voice_division_list')
        if voice_division_list is None:
            time_signatures = self.time_signatures
            voice_division_list = divisiontools.VoiceDivisionList(time_signatures)
        return voice_division_list

    def index(self, segment_specification):
        return self.segment_specifications.index(segment_specification)

    def interpret(self):
        interpreter = interpretertools.ConcreteInterpreter()
        return interpreter(self)

    def process_divisions_value(self, divisions_value):
        if isinstance(divisions_value, selectortools.SingleContextDivisionSliceSelector):
            return self.handle_division_retrieval_request(divisions_value)
        else:
            return divisions_value
        
    def resolve_attribute_retrieval_request(self, request):
        resolved_single_context_setting = \
            self.attribute_retrieval_indicator_to_resolved_single_context_setting(request.indicator)
        value = resolved_single_context_setting.value
        assert value is not None, repr(value)
        if request.callback is not None:
            value = request.callback(value)
        result = self.apply_offset_and_count_to_request(request, value)
        return result

    def resolve_single_context_setting(self, single_context_setting):
        if isinstance(single_context_setting, settingtools.ResolvedSingleContextSetting):
            return single_context_setting
        value = self.resolve_single_context_setting_source(single_context_setting)
        arguments = single_context_setting._mandatory_argument_values + (value, )
        resolved_single_context_setting = settingtools.ResolvedSingleContextSetting(*arguments, 
            persistent=single_context_setting.persistent, 
            truncate=single_context_setting.truncate, 
            fresh=single_context_setting.fresh)
        return resolved_single_context_setting

    def resolve_single_context_setting_source(self, single_context_setting):
        if isinstance(single_context_setting.source, requesttools.AttributeRequest):
            return self.resolve_attribute_retrieval_request(single_context_setting.source)
        elif isinstance(single_context_setting.source, requesttools.StatalServerRequest):
            return single_context_setting.source()
        else:
            return single_context_setting.source

    def segment_name_to_index(self, segment_name):
        segment_specification = self.segment_specifications[segment_name]
        return self.index(segment_specification)

    def segment_name_to_offsets(self, segment_name, segment_count=1):
        start_segment_index = self.segment_name_to_index(segment_name)        
        stop_segment_index = start_segment_index + segment_count - 1
        start_offset_pair = self.segment_offset_pairs[start_segment_index]
        stop_offset_pair = self.segment_offset_pairs[stop_segment_index]
        return start_offset_pair[0], stop_offset_pair[1]

    def select(self, segment_name, context_names=None, timespan=None):
        return selectortools.MultipleContextTimespanSelector(
            segment_name, context_names=context_names, timespan=timespan)

    # TODO: the really long dot-chaning here has got to go.
    #       The way to fix this is to make all selectors be able to recursively check for segment index.
    def store_single_context_setting(self, single_context_setting, clear_persistent_first=False):
        '''Resolve single-context setting and find segment in which single-context setting starts.

        Store resolved single-context setting in segment resolved single-context settings.

        If setting persists then store setting in score resolved single-context settings, too.
        '''
        resolved_single_context_setting = self.resolve_single_context_setting(single_context_setting)
        if isinstance(resolved_single_context_setting.target, selectortools.RatioSelector):
            rsc_setting = resolved_single_context_setting
            segment_index = rsc_setting.target.reference.timespan.selector.inequality.timespan.selector.index
        else:
            segment_index = resolved_single_context_setting.target.timespan.selector.index
        segment_specification = self.segment_specifications[segment_index]
        context_name = resolved_single_context_setting.target.context or \
            segment_specification.resolved_single_context_settings.score_name
        attribute = resolved_single_context_setting.attribute
        self.store_resolved_single_context_setting(
            segment_specification, context_name, attribute, resolved_single_context_setting, 
            clear_persistent_first=clear_persistent_first)

    def store_single_context_settings(self, single_context_settings, clear_persistent_first=False):
        for single_context_setting in single_context_settings:
            self.store_single_context_setting(
                single_context_setting, clear_persistent_first=clear_persistent_first)

    def store_resolved_single_context_setting(self, 
        segment_specification, context_name, attribute, resolved_single_context_setting, 
        clear_persistent_first=False):
        if clear_persistent_first:
            self.clear_persistent_resolved_single_context_settings(context_name, attribute)
        if attribute in segment_specification.resolved_single_context_settings[context_name]:
            segment_specification.resolved_single_context_settings[context_name][attribute].append(
                resolved_single_context_setting)
        else:
            segment_specification.resolved_single_context_settings[context_name][attribute] = [
                resolved_single_context_setting]
        if resolved_single_context_setting.persistent:
            if attribute in self.resolved_single_context_settings[context_name]:
                self.resolved_single_context_settings[context_name][attribute].append(
                    resolved_single_context_setting)
            else:
                self.resolved_single_context_settings[context_name][attribute] = [
                    resolved_single_context_setting]
