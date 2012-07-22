from abjad.tools import *
from experimental import interpretertools
from experimental.specificationtools.AttributeRetrievalRequest import AttributeRetrievalRequest
from experimental.specificationtools.Division import Division
from experimental.specificationtools.DivisionList import DivisionList
from experimental.specificationtools.RegionDivisionList import RegionDivisionList
from experimental.specificationtools.ScopedValue import ScopedValue
from experimental.specificationtools.SegmentDivisionList import SegmentDivisionList
from experimental.specificationtools.SegmentInventory import SegmentInventory
from experimental.specificationtools.SegmentSpecification import SegmentSpecification
from experimental.selectortools.MultipleContextTimespanSelector import MultipleContextTimespanSelector
from experimental.specificationtools.Specification import Specification
from experimental.specificationtools.StatalServerRequest import StatalServerRequest
from experimental.specificationtools.VoiceDivisionList import VoiceDivisionList
import collections
import copy
import re


class ScoreSpecification(Specification):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    Score specification::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> specification = specificationtools.ScoreSpecification(template)

    With three named segments::

        >>> segment = specification.append_segment('red')
        >>> segment = specification.append_segment('orange')
        >>> segment = specification.append_segment('yellow')

    All score specification properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template):
        Specification.__init__(self, score_template)
        self._segments = SegmentInventory()
        self._segment_specification_class = SegmentSpecification

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if isinstance(expr, int):
            return self.segments.__getitem__(expr)
        else:
            return self.payload_context_dictionary.__getitem__(expr)

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.segments)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def segment_names(self):
        return [segment.name for segment in self.segments]

    @property
    def segment_specification_class(self):
        return self._segment_specification_class

    @property
    def segments(self):
        return self._segments

    ### PUBLIC METHODS ###

    def add_divisions(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_divisions_to_voice(voice)

    # NEXT: extend this method to handle ratio selector settings.
    #       These settings address themselves to the timespans of *incomplete* segments
    def add_divisions_to_voice(self, voice):
        region_division_lists = self.make_region_division_lists_for_voice(voice)
        #self._debug(region_division_lists)
        if region_division_lists:
            self.payload_context_dictionary[voice.name]['region_division_lists'] = region_division_lists 
            voice_divisions = []
            for region_division_list in region_division_lists:
                voice_divisions.extend(region_division_list.divisions)
            #self._debug(voice_divisions)
            voice_division_list = VoiceDivisionList(voice_divisions)
            self.payload_context_dictionary[voice.name]['voice_division_list'] = voice_division_list
            segment_division_lists = self.make_segment_division_lists_for_voice(voice)
            #self._debug(segment_division_lists, 'CORRECT!')
            self.payload_context_dictionary[voice.name]['segment_division_lists'] = segment_division_lists
            self.add_segment_division_list_to_segment_payload_context_dictionarys_for_voice(
                voice, segment_division_lists)

    def add_rhythm_to_voice_for_segment_region_divisions(self, voice, rhythm_command, region_division_list):
        maker = rhythm_command.value
        assert isinstance(maker, timetokentools.TimeTokenMaker), repr(maker)
        leaf_lists = maker(region_division_list.pairs)
        containers = [containertools.Container(x) for x in leaf_lists]
        voice.extend(containers)
        if getattr(maker, 'beam', False):
            durations = [x.preprolated_duration for x in containers]
            beamtools.DuratedComplexBeamSpanner(containers, durations=durations, span=1)

    def add_rhythms(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_rhythms_to_voice(voice)

    def add_rhythms_to_voice(self, voice):
        rhythm_commands = self.get_rhythm_commands_for_all_segments_in_voice(voice)
        region_division_lists = self.payload_context_dictionary[voice.name]['region_division_lists']
        for rhythm_command, region_division_list in zip(rhythm_commands, region_division_lists):
            self.add_rhythm_to_voice_for_segment_region_divisions(voice, rhythm_command, region_division_list)

    # TODO: Using segment_division_lists here is a hack.
    #       Implement self.get_rhythm_commands_for_all_regions_in_voice()
    #       Then reimplement this method using *region* division lists.
    def add_rhythms_to_voice_new(self, voice):
        rhythm_commands = self.get_rhythm_commands_for_all_segments_in_voice(voice)
        segment_division_lists = self.payload_context_dictionary[voice.name]['segment_division_lists']
        for rhythm_command, segment_division_list in zip(rhythm_commands, segment_division_lists):
            self.add_rhythm_to_voice_for_segment_region_divisions(voice, rhythm_command, segment_division_list)

    def add_segment_division_list_to_segment_payload_context_dictionarys_for_voice(
        self, voice, segment_division_lists):
        assert len(self.segments) == len(segment_division_lists)
        for segment, segment_division_list in zip(self.segments, segment_division_lists):
            segment.payload_context_dictionary[voice.name]['segment_division_list'] = segment_division_list
            segment.payload_context_dictionary[voice.name]['segment_pairs'] = [
                x.pair for x in segment_division_list]

    def add_time_signatures(self):
        for segment in self.segments:
            segment.add_time_signatures(self.score)

    def append_segment(self, name=None):
        name = name or str(self.find_first_unused_segment_number())
        assert name not in self.segment_names, repr(name)
        segment = self.segment_specification_class(self.score_template, name)
        self.segments.append(segment)
        return segment

    def apply_additional_segment_parameters(self):
        pass 

    def apply_boundary_indicators_to_raw_segment_division_lists(self, 
        voice_division_list, raw_segment_division_lists):
        voice_divisions = voice_division_list.divisions
        voice_divisions = [mathtools.NonreducedFraction(x) for x in voice_divisions] 
        parts = sequencetools.partition_sequence_by_backgrounded_weights(voice_divisions, self.segment_durations)
        overage_from_previous_segment = 0
        segment_division_lists = []
        for part, raw_segment_division_list in zip(parts, raw_segment_division_lists):
            segment_division_list = copy.copy(raw_segment_division_list)
            segment_division_list[0].is_left_open = bool(overage_from_previous_segment)
            segment_duration_plus_fringe = overage_from_previous_segment + sum(part)
            overage_from_current_segment = segment_duration_plus_fringe - raw_segment_division_list.duration
            segment_division_list[-1].is_right_open = bool(overage_from_current_segment)
            overage_from_previous_segment = overage_from_current_segment
            segment_division_lists.append(segment_division_list)
        return segment_division_lists

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

    def apply_segment_pitch_classes(self):
        pass

    def apply_segment_registration(self):
        pass

    def calculate_segment_offset_pairs(self):
        segment_durations = [segment.duration for segment in self.segments]
        if sequencetools.all_are_numbers(segment_durations):
            self.segment_durations = segment_durations
            self.score_duration = sum(self.segment_durations)
            self.segment_offset_pairs = mathtools.cumulative_sums_zero_pairwise(self.segment_durations)
    
    def change_attribute_retrieval_indicator_to_setting(self, indicator):
        segment = self.segments[indicator.segment_name]
        context_proxy = segment.resolved_settings_context_dictionary[indicator.context_name]
        setting = context_proxy.get_setting(attribute=indicator.attribute)
        return setting

    def change_uninterpreted_division_commands_to_region_division_commands(self, uninterpreted_division_commands):
        region_division_commands = []
        if not uninterpreted_division_commands:
            return []
        if any([x.value is None for x in uninterpreted_division_commands]):
            return []
        assert uninterpreted_division_commands[0].fresh, repr(uninterpreted_division_commands[0])
        for uninterpreted_division_command in uninterpreted_division_commands:
            if uninterpreted_division_command.fresh or uninterpreted_division_command.truncate:
                region_division_command = interpretertools.RegionDivisionCommand(
                    *uninterpreted_division_command.vector)
                region_division_commands.append(region_division_command)
            else:
                last_region_division_command = region_division_commands[-1]
                assert last_region_division_command.value == uninterpreted_division_command.value
                if last_region_division_command.truncate:
                    region_division_command = interpretertools.RegionDivisionCommand(
                        *uninterpreted_division_command.vector)
                    region_division_commands.append(region_division_command)
                else:
                    value = last_region_division_command.value
                    duration = last_region_division_command.duration + uninterpreted_division_command.duration
                    #fresh = 'FOO'
                    fresh = last_region_division_command.fresh
                    truncate = uninterpreted_division_command.truncate
                    args = (value, duration, fresh, truncate)
                    region_division_command = interpretertools.RegionDivisionCommand(*args)
                    region_division_commands[-1] = region_division_command
        return region_division_commands

    def evaluate_segment_index_expression(self, expression):
        r'''Evaluate segment index expression::

            >>> expression = selectortools.SegmentIndexExpression("'red'")
            >>> specification.evaluate_segment_index_expression(expression)
            0

        ::

            >>> expression = selectortools.SegmentIndexExpression("'orange'")
            >>> specification.evaluate_segment_index_expression(expression)
            1

        ::

            >>> expression = selectortools.SegmentIndexExpression("'yellow'")
            >>> specification.evaluate_segment_index_expression(expression)
            2

        ::

            >>> expression = selectortools.SegmentIndexExpression("'red' + 'orange' + 'yellow'")
            >>> specification.evaluate_segment_index_expression(expression)
            3

        Evaluate strings directlly::

            >>> specification.evaluate_segment_index_expression('yellow')
            2

        Return integers unchanged::

            >>> specification.evaluate_segment_index_expression(0)
            0

        Return integer.
        '''
        from experimental import selectortools
        if isinstance(expression, int):
            return expression
        if isinstance(expression, str):
            return self.segment_name_to_index(expression)
        quoted_string_pattern = re.compile(r"""(['"]{1}[a-zA-Z1-9 _]+['"]{1})""")
        quoted_segment_names = quoted_string_pattern.findall(expression.string)
        modified_string = str(expression.string)
        for quoted_segment_name in quoted_segment_names:
            segment_name = quoted_segment_name[1:-1]
            segment_index = self.segment_name_to_index(segment_name)
            modified_string = modified_string.replace(quoted_segment_name, str(segment_index))
        result = eval(modified_string)
        return result
        
    def find_first_unused_segment_number(self):
        candidate_segment_number = 1
        while True:
            for segment in self.segments:
                if segment.name == str(candidate_segment_number):
                    candidate_segment_number += 1
                    break
            else:
                return candidate_segment_number

    # new behavior
    def get_improved_uninterpreted_division_commands_for_voice(self, voice):
        improved_uninterpreted_division_commands = []
        for segment in self.segments:
            commands = segment.get_uninterpreted_division_commands_that_start_during_segment(voice.name)
            improved_uninterpreted_division_commands.extend(commands)
        return improved_uninterpreted_division_commands

    def get_rhythm_commands_for_all_segments_in_voice(self, voice):
        rhythm_commands = []
        for segment in self.segments:
            rhythm_command = segment.get_rhythm_command(voice.name)
            rhythm_commands.append(rhythm_command)
        return rhythm_commands

    # deprecated behavior
    def get_uninterpreted_division_commands_for_voice(self, voice):
        uninterpreted_division_commands = []
        for segment in self.segments:
            resolved_value = segment.get_division_resolved_value(voice.name)
            value = self.process_divisions_value(resolved_value.value)
            args = (value, segment.duration, resolved_value.fresh, resolved_value.truncate)
            command = interpretertools.UninterpretedDivisionCommand(*args)
            uninterpreted_division_commands.append(command)
        return uninterpreted_division_commands

    def get_start_division_lists_for_voice(self, voice):
        region_division_lists = self.payload_context_dictionary[voice.name]['region_division_lists']
        divisions = []
        for region_division_list in region_division_lists:
            divisions.extend(region_division_list)
        divisions = [mathtools.NonreducedFraction(x) for x in divisions] 
        assert sum(divisions) == self.score_duration
        start_division_lists = sequencetools.partition_sequence_by_backgrounded_weights(
            divisions, self.segment_durations)
        start_division_lists = [DivisionList(x) for x in start_division_lists]
        return start_division_lists

    def glue_rhythm_commands_and_start_division_lists(self, rhythm_commands, start_division_lists):
        assert len(rhythm_commands) == len(start_division_lists)
        assert rhythm_commands[0].fresh
        glued_rhythm_commands, new_parts = [rhythm_commands[0]], [start_division_lists[0][:]]
        for rhythm_command, start_division_list in zip(rhythm_commands[1:], start_division_lists[1:]):
            if rhythm_command.value == glued_rhythm_commands[-1].value and \
                not rhythm_command.fresh:
                new_parts[-1].extend(start_division_list)
            else:
                glued_rhythm_commands.append(rhythm_command)
                new_parts.append(start_division_list[:])
        return glued_rhythm_commands, new_parts

    def handle_divisions_retrieval_request(self, request):
        voice = componenttools.get_first_component_in_expr_with_name(self.score, request.voice)
        assert isinstance(voice, voicetools.Voice), voice
        region_division_lists = self.payload_context_dictionary[voice.name]['region_division_lists']
        divisions = []
        for region_division_list in region_division_lists:
            divisions.extend(region_division_list)
        assert isinstance(divisions, list), divisions
        start_segment_expr = request.inequality.timespan.selector.start
        stop_segment_expr = request.inequality.timespan.selector.stop
        start_segment_index = self.evaluate_segment_index_expression(start_segment_expr)
        stop_segment_index = self.evaluate_segment_index_expression(stop_segment_expr)
        segment_count =  stop_segment_index - start_segment_index
        start_offset, stop_offset = self.segment_name_to_offsets(start_segment_index, segment_count)
        total_amount = stop_offset - start_offset
        divisions = [mathtools.NonreducedFraction(x) for x in divisions]
        divisions = sequencetools.split_sequence_once_by_weights_with_overhang(divisions, [0, total_amount])
        divisions = divisions[1]
        if request.callback is not None:
            divisions = request.callback(divisions)
        return divisions

    def index(self, segment):
        return self.segments.index(segment)

    def instantiate_score(self):
        self.score = self.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        self.score.insert(0, context)
        
    def interpret(self):
        self.instantiate_score()
        self.unpack_directives()
        self.interpret_segment_time_signatures()
        self.add_time_signatures()
        self.calculate_segment_offset_pairs()
        self.interpret_segment_divisions()
        self.add_divisions()
        self.interpret_segment_rhythms()
        self.add_rhythms()
        self.interpret_segment_pitch_classes()
        self.apply_segment_pitch_classes()
        self.interpret_segment_registration()
        self.apply_segment_registration()
        self.interpret_additional_segment_parameters()
        self.apply_additional_segment_parameters()
        return self.score

    def interpret_additional_segment_parameters(self):
        for segment in self.segments:
            pass

    def interpret_segment_divisions(self):
        for segment in self.segments:
            settings = segment.settings.get_settings(attribute='divisions')
            if not settings:
                settings = []
                existing_settings = self.resolved_settings_context_dictionary.get_settings(
                    attribute='divisions')
                for existing_setting in existing_settings:
                    assert existing_setting.target.timespan.encompasses_one_segment_exactly, repr(existing_setting)
                    setting = existing_setting.copy_to_segment(segment)
                    settings.append(setting)
            self.store_settings(settings)

    def interpret_segment_pitch_classes(self):
        for segment in self.segments:
            pass

    def interpret_segment_registration(self):
        for segment in self.segments:
            pass

    def interpret_segment_rhythms(self):
        for segment in self.segments:
            settings = segment.settings.get_settings(attribute='rhythm')
            if not settings:
                settings = []
                existing_settings = self.resolved_settings_context_dictionary.get_settings(
                    attribute='rhythm')
                for existing_setting in existing_settings:
                    setting = existing_setting.copy_to_segment(segment)
                    settings.append(setting)
            self.store_settings(settings)

    def interpret_segment_time_signatures(self):
        '''For each segment:
        Check segment for a very explicit time signature setting.
        If none, check SCORE resolved settings context dictionary for current time signature setting.
        Halt interpretation if no time signature setting is found.
        Otherwise store time signature setting.
        '''
        for segment in self.segments:
            settings = segment.settings.get_settings(attribute='time_signatures')
            if settings:
                assert len(settings) == 1, repr(settings)
                setting = settings[0]
            else:
                settings = self.resolved_settings_context_dictionary.get_settings(attribute='time_signatures')
                if not settings:
                    return
                assert len(settings) == 1, repr(settings)
                setting = settings[0]
                setting = setting.copy_to_segment(segment.name)
            assert setting.target.context == segment.score_name, repr(setting)
            assert setting.target.timespan == segment.timespan, [repr(setting), '\n', repr(segment.timespan)]
            self.store_setting(setting)

    def make_region_division_lists_for_voice(self, voice):
        '''Called only once for each voice in score.
        Make one RegionDivisionList for each region in voice.
        Model of region is changing during count ratio selector integration.
        What is the relationship between segments, regions and divisions?
        A segment models a small-, medium- or large-sized section of score.
        A division is the smallest unit of input to some material-making process;
        A division is frequently analagous to a beat.
        A region is (finally) defined equal to zero or more consecutive divisions.
        The purpose of a region is yoke together divisions for input to some material-making process.
        So regions act as a type of container of divisions.
        Segments exhibit no necessary relationship with either regions or divisions.
        But in the usual case a segment will comprise one (or a few) regions.
        '''
        # CURRENT: toggle between these two values while implementing count ratio selectors
        #          First line is for last known good behavior.
        #          Second line is for newly improved behavior.
        #          Corresponding change must also be made in self.store_setting() for this to work.
        #          And also one change in ContextProxy.
        uninterpreted_division_commands = self.get_uninterpreted_division_commands_for_voice(voice)
        #uninterpreted_division_commands = self.get_improved_uninterpreted_division_commands_for_voice(voice)
        #self._debug(uninterpreted_division_commands)
        region_division_commands = self.change_uninterpreted_division_commands_to_region_division_commands(
            uninterpreted_division_commands)
        #self._debug(region_division_commands)
        region_division_lists = self.make_region_division_lists_from_region_division_commands(
            region_division_commands)
        self.payload_context_dictionary[voice.name]['region_division_lists'] = region_division_lists[:]
        self.payload_context_dictionary[voice.name]['region_division_lists'] = region_division_lists[:]
        #self._debug(region_division_lists)
        return region_division_lists

    def make_region_division_lists_from_region_division_commands(self, region_division_commands):
        '''Return list of division lists.
        '''
        region_division_lists = []
        for region_division_command in region_division_commands:
            divisions = [mathtools.NonreducedFraction(x) for x in region_division_command.value]
            divisions = sequencetools.repeat_sequence_to_weight_exactly(
                divisions, region_division_command.duration)
            divisions = [x.pair for x in divisions]
            divisions = [Division(x) for x in divisions]
            region_division_list = RegionDivisionList(divisions)
            #region_division_list.fresh = 'FOO'
            region_division_list.fresh = region_division_command.fresh
            region_division_list.truncate = region_division_command.truncate
            region_division_lists.append(region_division_list)
        return region_division_lists

    def make_resolved_setting(self, setting):
        from experimental import settingtools
        if isinstance(setting, settingtools.ResolvedSingleContextSetting):
            return setting
        value = self.resolve_setting_source(setting)
        arguments = setting._mandatory_argument_values + (value, )
        resolved_setting = settingtools.ResolvedSingleContextSetting(*arguments, 
            persistent=setting.persistent, truncate=setting.truncate, fresh=setting.fresh)
        return resolved_setting

    def make_segment_division_lists_for_voice(self, voice):
        voice_division_list = self.payload_context_dictionary[voice.name]['voice_division_list']
        voice_divisions = [mathtools.NonreducedFraction(x) for x in voice_division_list.divisions]
        segment_durations = self.segment_durations
        shards = sequencetools.split_sequence_once_by_weights_with_overhang(voice_divisions, segment_durations)
        raw_segment_division_lists = []
        for i, shard in enumerate(shards[:]):
            raw_segment_division_list = SegmentDivisionList(shard)
            raw_segment_division_lists.append(raw_segment_division_list)
        segment_division_lists = self.apply_boundary_indicators_to_raw_segment_division_lists(
            voice_division_list, raw_segment_division_lists)
        return segment_division_lists

    def process_divisions_value(self, divisions_value):
        from experimental import selectortools
        if isinstance(divisions_value, selectortools.SingleContextDivisionSliceSelector):
            return self.handle_divisions_retrieval_request(divisions_value)
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
        if isinstance(setting.source, AttributeRetrievalRequest):
            return self.resolve_attribute_retrieval_request(setting.source)
        elif isinstance(setting.source, StatalServerRequest):
            return setting.source()
        else:
            return setting.source

    def segment_name_to_index(self, segment_name):
        segment = self.segments[segment_name]
        return self.index(segment)

    def segment_name_to_offsets(self, segment_name, segment_count=1):
        start_segment_index = self.segment_name_to_index(segment_name)        
        stop_segment_index = start_segment_index + segment_count - 1
        start_offset_pair = self.segment_offset_pairs[start_segment_index]
        stop_offset_pair = self.segment_offset_pairs[stop_segment_index]
        return start_offset_pair[0], stop_offset_pair[1]

    def select(self, segment_name, context_names=None, timespan=None):
        return MultipleContextTimespanSelector(segment_name, context_names=context_names, timespan=timespan)

    # TODO: the really long dot-chaning here has got to go.
    #       The way to fix this is to make all selectors be able to recursively check for segment index.
    def store_setting(self, setting):
        '''Resolve setting and find segment specified by setting.
        Store setting in SEGMENT context tree and, if persistent, in SCORE context tree, too.
        '''
        from experimental import selectortools
        resolved_setting = self.make_resolved_setting(setting)
        if isinstance(resolved_setting.target, selectortools.RatioSelector):
            segment_index = resolved_setting.target.reference.timespan.selector.inequality.timespan.selector.index
        else:
            segment_index = resolved_setting.target.timespan.selector.index
        segment = self.segments[segment_index]
        context_name = resolved_setting.target.context or \
            segment.resolved_settings_context_dictionary.score_name
        attribute = resolved_setting.attribute
        # CURRENT: toggle between these two values while implementing count ratio selectors
        #          First line is for last known good behavior.
        #          Second line is for newly improved behavior.
        self.store_only_one_setting(segment, context_name, attribute, resolved_setting)
        #self.store_multiple_settings(segment, context_name, attribute, resolved_setting)

    # new behavior
    def store_multiple_settings(self, segment, context_name, attribute, resolved_setting):
        if attribute in segment.resolved_settings_context_dictionary[context_name]:
            segment.resolved_settings_context_dictionary[context_name][attribute].append(resolved_setting)
        else:
            segment.resolved_settings_context_dictionary[context_name][attribute] = [resolved_setting]
        if resolved_setting.persistent:
            if attribute in self.resolved_settings_context_dictionary[context_name]:
                self.resolved_settings_context_dictionary[context_name][attribute].append(resolved_setting)
            else:
                self.resolved_settings_context_dictionary[context_name] = [resolved_setting]

    # deprecated old behavior
    def store_only_one_setting(self, segment, context_name, attribute, resolved_setting):
        segment.resolved_settings_context_dictionary[context_name][attribute] = resolved_setting
        if resolved_setting.persistent:
            self.resolved_settings_context_dictionary[context_name][attribute] = resolved_setting

    def store_settings(self, settings):
        for setting in settings:
            self.store_setting(setting)

    def unpack_directives(self):
        for segment in self.segments:
            self.settings.extend(segment.unpack_directives())
