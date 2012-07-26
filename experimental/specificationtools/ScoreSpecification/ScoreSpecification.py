from abjad.tools import *
from experimental import divisiontools
from experimental import helpertools
from experimental import interpretertools
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental import timespantools
from experimental.specificationtools.SegmentSpecification import SegmentSpecification
from experimental.specificationtools.SegmentSpecificationInventory import SegmentSpecificationInventory
from experimental.specificationtools.Specification import Specification
import copy
import re


class ScoreSpecification(Specification):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import helpertools
        >>> from experimental import selectortools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

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
    def duration(self):
        result = []
        for segment_specification in self.segment_specifications:
            duration = segment_specification.duration
            if duration is not None:
                result.append(duration)
        return sum(result)

    @property
    def segment_names(self):
        return [segment_specification.name for segment_specification in self.segment_specifications]

    @property
    def segment_specification_class(self):
        return self._segment_specification_class

    @property
    def segment_specifications(self):
        return self._segment_specifications

    @property
    def time_signatures(self):
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

    def apply_offset_and_count(self, request, value):
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
    
    def change_attribute_retrieval_indicator_to_setting(self, indicator):
        segment_specification = self.segment_specifications[indicator.segment_name]
        context_proxy = segment_specification.resolved_single_context_settings[indicator.context_name]
        setting = context_proxy.get_setting(attribute=indicator.attribute)
        return setting

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
        from experimental import interpretertools
        interpreter = interpretertools.ConcreteInterpreter()
        return interpreter(self)

    def make_resolved_single_context_setting(self, setting):
        if isinstance(setting, settingtools.ResolvedSingleContextSetting):
            return setting
        value = self.resolve_setting_source(setting)
        arguments = setting._mandatory_argument_values + (value, )
        resolved_setting = settingtools.ResolvedSingleContextSetting(*arguments, 
            persistent=setting.persistent, truncate=setting.truncate, fresh=setting.fresh)
        return resolved_setting

    def process_divisions_value(self, divisions_value):
        if isinstance(divisions_value, selectortools.SingleContextDivisionSliceSelector):
            return self.handle_division_retrieval_request(divisions_value)
        else:
            return divisions_value
        
    def resolve_attribute_retrieval_request(self, request):
        setting = self.change_attribute_retrieval_indicator_to_setting(request.indicator)
        value = setting.value
        assert value is not None, repr(value)
        if request.callback is not None:
            value = request.callback(value)
        result = self.apply_offset_and_count(request, value)
        return result

    def resolve_setting_source(self, setting):
        from experimental import specificationtools
        if isinstance(setting.source, requesttools.AttributeRequest):
            return self.resolve_attribute_retrieval_request(setting.source)
        elif isinstance(setting.source, requesttools.StatalServerRequest):
            return setting.source()
        else:
            return setting.source

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

    def store_resolved_single_context_settings(self, 
        segment_specification, context_name, attribute, resolved_setting, clear_persistent_first=False):
        if clear_persistent_first:
            self.clear_persistent_resolved_single_context_settings(context_name, attribute)
        if attribute in segment_specification.resolved_single_context_settings[context_name]:
            segment_specification.resolved_single_context_settings[context_name][attribute].append(
                resolved_setting)
        else:
            segment_specification.resolved_single_context_settings[context_name][attribute] = [resolved_setting]
        if resolved_setting.persistent:
            if attribute in self.resolved_single_context_settings[context_name]:
                self.resolved_single_context_settings[context_name][attribute].append(resolved_setting)
            else:
                self.resolved_single_context_settings[context_name][attribute] = [resolved_setting]

    # TODO: change name to self.store_single_context_setting()
    # TODO: the really long dot-chaning here has got to go.
    #       The way to fix this is to make all selectors be able to recursively check for segment index.
    def store_setting(self, setting, clear_persistent_first=False):
        '''Resolve setting and find segment in which setting starts.

        Store setting in segment context tree.

        If setting persists then store setting in score context tree, too.
        '''
        resolved_single_context_setting = self.make_resolved_single_context_setting(setting)
        if isinstance(resolved_single_context_setting.target, selectortools.RatioSelector):
            segment_index = resolved_single_context_setting.target.reference.timespan.selector.inequality.timespan.selector.index
        else:
            segment_index = resolved_single_context_setting.target.timespan.selector.index
        segment_specification = self.segment_specifications[segment_index]
        context_name = resolved_single_context_setting.target.context or \
            segment_specification.resolved_single_context_settings.score_name
        attribute = resolved_single_context_setting.attribute
        self.store_resolved_single_context_settings(
            segment_specification, context_name, attribute, resolved_single_context_setting, 
            clear_persistent_first=clear_persistent_first)

    # TODO: change name to self.store_single_context_settings()
    def store_settings(self, settings, clear_persistent_first=False):
        for setting in settings:
            self.store_setting(setting, clear_persistent_first=clear_persistent_first)
