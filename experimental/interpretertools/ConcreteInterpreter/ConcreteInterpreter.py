import copy
from abjad.tools import *
from experimental import divisiontools
from experimental import helpertools
from experimental import library
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespaninequalitytools
from experimental.interpretertools.Interpreter import Interpreter


class ConcreteInterpreter(Interpreter):
    r'''.. versionadded:: 1.0

    Concrete interpreter.

    Currently the only interpreter implemented.

    The ``'concrete'`` designation is provisional.
    '''

    ### INITIALIZER ###

    def __call__(self, score_specification):
        '''Top-level interpretation entry point::

            * interpret time signatures
            * interpret divisions
            * interpret rhythms
            * interpret pitch-classes
            * interpret registration
            * interpret additional parameters

        Return Abjad score object.
        '''
        self.score_specification = score_specification
        self.score = self.instantiate_score()
        self.unpack_multiple_context_settings_for_score()
        self.store_single_context_time_signature_settings()
        self.add_time_signatures_to_score()
        self.calculate_segment_offset_pairs()
        self.store_single_context_division_settings()
        self.add_division_lists_to_score()
        self.store_single_context_rhythm_settings()
        self.add_rhythms_to_score()
        self.store_single_context_pitch_class_settings()
        self.apply_pitch_classes()
        self.store_single_context_registration_settings()
        self.apply_registration()
        self.store_additional_single_context_settings()
        self.apply_additional_parameters()
        return self.score

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def add_division_lists_to_score(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_division_lists_to_voice(voice)

    def add_division_lists_to_voice(self, voice):
        #self._debug(voice)
        self.make_division_region_division_lists_for_voice(voice)
        #self._debug_values(
        #    self.score_specification.contexts[voice.name]['division_region_division_lists'], 'drdl')
        if self.score_specification.contexts[voice.name]['division_region_division_lists']:
            voice_division_list = self.make_voice_division_list_for_voice(voice)
            self.score_specification.contexts[voice.name]['voice_division_list'] = voice_division_list
            #self._debug(voice_division_list, 'vdl')
            segment_division_lists = self.make_segment_division_lists_for_voice(voice)
            self.score_specification.contexts[voice.name]['segment_division_lists'] = segment_division_lists
            #self._debug(segment_division_lists, 'sdl')
            self.add_segment_division_lists_to_voice(voice, segment_division_lists)

    def add_rhythm_to_voice(self, voice, rhythm_maker, rhythm_region_division_list):
#        self._debug(rhythm_maker)
#        self._debug(rhythm_region_division_list)
        assert isinstance(rhythm_maker, timetokentools.TimeTokenMaker), repr(rhythm_maker)
        assert isinstance(rhythm_region_division_list, divisiontools.RhythmRegionDivisionList)
        leaf_lists = rhythm_maker(rhythm_region_division_list.pairs)
        rhythm_containers = [containertools.Container(x) for x in leaf_lists]
        voice.extend(rhythm_containers)
        self.conditionally_beam_rhythm_containers(rhythm_maker, rhythm_containers)

    def add_rhythms_to_score(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_rhythms_to_voice(voice)

    def add_rhythms_to_voice(self, voice):
        voice_division_list = self.get_voice_division_list(voice)
        if len(voice_division_list) == 0:
            return
        #self._debug(voice_division_list, 'vdl')
        voice_divisions = voice_division_list.divisions
        voice_division_durations = [durationtools.Duration(x) for x in voice_divisions]
        #self._debug(voice_division_durations, 'vdd')

        rhythm_commands = self.get_rhythm_commands_for_voice(voice)
        #self._debug_values(rhythm_commands, 'rc')
        rhythm_commands = self.fuse_like_rhythm_commands(rhythm_commands)
        #self._debug_values(rhythm_commands, 'rc')
        rhythm_command_durations = [x.duration for x in rhythm_commands]
        #self._debug(rhythm_command_durations, 'rcd')

        key = 'division_region_division_lists'
        division_region_division_lists = self.score_specification.contexts[voice.name][key]
        #self._debug_values(division_region_division_lists, 'drdl')
        division_region_durations = [x.duration for x in division_region_division_lists]
        #self._debug(division_region_durations, 'drd')
        rhythm_region_durations = sequencetools.merge_duration_sequences(
            division_region_durations, rhythm_command_durations)
        #self._debug(rhythm_region_durations, 'rrd')
        args = (voice_division_durations, rhythm_region_durations)
        rhythm_region_division_duration_lists = sequencetools.partition_sequence_by_backgrounded_weights(*args)
        assert len(rhythm_region_division_duration_lists) == len(rhythm_region_durations)
        rhythm_region_lengths = [len(l) for l in rhythm_region_division_duration_lists]
        rhythm_region_division_lists = sequencetools.partition_sequence_by_counts(
            voice_divisions, rhythm_region_lengths, cyclic=False, overhang=False)
        assert len(rhythm_region_division_lists) == len(rhythm_region_durations)
        input_pairs = [(command.resolved_value, command.duration) for command in rhythm_commands]
        output_pairs = sequencetools.pair_duration_sequence_elements_with_input_pair_values(
            rhythm_region_durations, input_pairs)
        rhythm_makers = [output_pair[-1] for output_pair in output_pairs]
        assert len(rhythm_makers) == len(rhythm_region_division_lists)
        self.make_rhythms_and_add_to_voice(voice, rhythm_makers, rhythm_region_division_lists)

    def add_segment_division_lists_to_voice(
        self, voice, segment_division_lists):
        assert len(self.score_specification.segment_specifications) == len(segment_division_lists)
        for segment_specification, segment_division_list in zip(
            self.score_specification.segment_specifications, segment_division_lists):
            segment_specification.contexts[voice.name]['segment_division_list'] = segment_division_list
            segment_specification.contexts[voice.name]['segment_pairs'] = [
                x.pair for x in segment_division_list]

    def add_time_signatures_for_segment(self, segment_specification):
        time_signatures = segment_specification.time_signatures
        if time_signatures is not None:
            measures = measuretools.make_measures_with_full_measure_spacer_skips(time_signatures)
            context = componenttools.get_first_component_in_expr_with_name(self.score, 'TimeSignatureContext')
            context.extend(measures)

    def add_time_signatures_to_score(self):
        for segment_specification in self.score_specification.segment_specifications:
            self.add_time_signatures_for_segment(segment_specification)

    def apply_additional_parameters(self):
        pass

    def apply_pitch_classes(self):
        pass

    def apply_registration(self):
        pass

    def calculate_segment_offset_pairs(self):
        '''Set ``'segment_durations'`` property on score specification.

        Set ``'score_duration'`` property on score specification.

        Set ``'start_offset'`` to ``Offset(0)`` on score specification.

        Set ``'stop_offset'`` on score specification.

        Set ``'segment_offset_pairs'`` property on score specification.
        '''
        segment_durations = [x.duration for x in self.score_specification.segment_specifications]
        #self._debug(segment_durations, 'sd')
        if sequencetools.all_are_numbers(segment_durations):
            self.score_specification.segment_durations = segment_durations
            self.score_specification.score_duration = sum(self.score_specification.segment_durations)
            self.score_specification.start_offset = durationtools.Offset(0)
            self.score_specification.stop_offset = durationtools.Offset(
                self.score_specification.score_duration)
            segment_offset_pairs = mathtools.cumulative_sums_zero_pairwise(
                self.score_specification.segment_durations)
            segment_offset_pairs = [
                (durationtools.Offset(x[0]), durationtools.Offset(x[1])) for x in segment_offset_pairs]
            self.score_specification.segment_offset_pairs = segment_offset_pairs

    def clear_persistent_resolved_single_context_settings(self, context_name, attribute):
        r'''Clear persistent resolved single-context settings.
        '''
        if attribute in self.score_specification.resolved_single_context_settings[context_name]:
            del(self.score_specification.resolved_single_context_settings[context_name][attribute])

    def conditionally_beam_rhythm_containers(self, rhythm_maker, rhythm_containers):
        if getattr(rhythm_maker, 'beam', False):
            durations = [x.preprolated_duration for x in rhythm_containers]
            beamtools.DuratedComplexBeamSpanner(rhythm_containers, durations=durations, span=1)

    def division_material_request_to_divisions(self, division_material_request):
        assert isinstance(division_material_request, requesttools.MaterialRequest)
        assert division_material_request.attribute == 'divisions'
        voice = componenttools.get_first_component_in_expr_with_name(
            self.score, division_material_request.context_name)
        assert isinstance(voice, voicetools.Voice), voice
        division_region_division_lists = self.score_specification.contexts[voice.name][
            'division_region_division_lists']
        divisions = []
        for division_region_division_list in division_region_division_lists:
            divisions.extend(division_region_division_list)
        assert isinstance(divisions, list), divisions
        start_segment_identifier = division_material_request.selector.start_identifier
        stop_segment_identifier = division_material_request.selector.stop_identifier
        start_segment_index = self.score_specification.segment_identifier_expression_to_segment_index(
            start_segment_identifier)
        stop_segment_index = self.score_specification.segment_identifier_expression_to_segment_index(
            stop_segment_identifier)
        segment_count =  stop_segment_index - start_segment_index
        start_offset, stop_offset = self.score_specification.segment_name_to_segment_offsets(
            start_segment_index, segment_count)
        total_amount = stop_offset - start_offset
        divisions = [mathtools.NonreducedFraction(x) for x in divisions]
        divisions = sequencetools.split_sequence_by_weights(
            divisions, [0, total_amount], cyclic=False, overhang=True)
        divisions = divisions[1]
        if division_material_request.callback is not None:
            divisions = division_material_request.callback(divisions)
        return divisions

    def fix_boundary_indicators_to_raw_segment_division_lists(self,
        voice_division_list, raw_segment_division_lists):
        #self._debug(voice_division_list, 'vdl')
        #self._debug(raw_segment_division_lists, 'rsdl')
        voice_divisions = voice_division_list.divisions
        voice_divisions = [mathtools.NonreducedFraction(x) for x in voice_divisions]
        parts = sequencetools.partition_sequence_by_backgrounded_weights(
            voice_divisions, self.score_specification.segment_durations)
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

    def fuse_like_rhythm_commands(self, rhythm_commands):
        if not rhythm_commands:
            return []
        result = [copy.deepcopy(rhythm_commands[0])]
        for rhythm_command in rhythm_commands[1:]:
            if rhythm_command.resolved_value == result[-1].resolved_value and not rhythm_command.fresh:
                result[-1]._duration += rhythm_command.duration
            else:
                result.append(copy.deepcopy(rhythm_command))
        return result

    def get_resolved_single_context_settings(self, segment_specification, attribute, context_name,
        include_improper_parentage=False):
        context = componenttools.get_first_component_in_expr_with_name(
            segment_specification.score_model, context_name)
        result = []
        if include_improper_parentage:
            parentage_to_search = componenttools.get_improper_parentage_of_component(context)
        else:
            parentage_to_search = [context]
        # ensure lower-level contexts appear before high-level contexts
        parentage_to_search = list(reversed(parentage_to_search))
        for component in parentage_to_search:
            context_proxy = segment_specification.resolved_single_context_settings[component.name]
            resolved_single_context_settings = context_proxy.get_settings(attribute=attribute)
            if resolved_single_context_settings:
                result.extend(resolved_single_context_settings)
        return result

    def get_rhythm_commands_for_voice(self, voice):
        rhythm_commands = []
        for segment_specification in self.score_specification.segment_specifications:
            raw_commands = self.get_rhythm_commands_that_start_during_segment(
                segment_specification, voice.name)
            #self._debug(raw_commands, 'raw')
            default_command = self.make_default_rhythm_command_for_segment(segment_specification)
            raw_commands.insert(0, default_command)
            #self._debug(raw_commands, 'raw')
            cooked_commands = self.sort_and_split_raw_commands(raw_commands)
            #self._debug(cooked_commands, 'cooked')
            rhythm_commands.extend(cooked_commands)
        return rhythm_commands

    def get_rhythm_commands_that_start_during_segment(self, segment_specification, context_name):
        #self._debug(segment_specification, 'segment')
        resolved_single_context_settings = self.get_resolved_single_context_settings(
            segment_specification, 'rhythm', context_name, include_improper_parentage=True)
        rhythm_commands = []
        for resolved_single_context_setting in resolved_single_context_settings:
            #self._debug(resolved_single_context_setting)
            rhythm_command = \
                self.resolved_single_context_setting_to_rhythm_command(
                resolved_single_context_setting, segment_specification)
            rhythm_commands.append(rhythm_command)
        #print ''
        return rhythm_commands

    def get_segment_specification(self, expr):
        return self.score_specification.get_segment_specification(expr)

    def get_time_signature_slice(self, start_offset, stop_offset):
        assert self.score_specification.time_signatures
        time_signatures = self.score_specification.time_signatures
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        slice_duration = stop_offset - start_offset
        weights = [start_offset, slice_duration]
        shards = sequencetools.split_sequence_by_weights(
            time_signatures, weights, cyclic=False, overhang=False)
        result = shards[1]
        result = [x.pair for x in result]
        return result

    def get_uninterpreted_division_commands_for_voice(self, voice):
        uninterpreted_division_commands = []
        for segment_specification in self.score_specification.segment_specifications:
            raw_commands = self.get_uninterpreted_division_commands_that_start_during_segment(
                segment_specification, voice.name)
            cooked_commands = self.sort_and_split_raw_commands(raw_commands)
            if cooked_commands:
                uninterpreted_division_commands.extend(cooked_commands)
            elif segment_specification.time_signatures:
                command = self.make_default_uninterpreted_division_command_for_segment(segment_specification)
                uninterpreted_division_commands.append(command)
        return uninterpreted_division_commands

    def get_uninterpreted_division_commands_that_start_during_segment(self, 
        segment_specification, context_name):
        #self._debug(segment_specification, 'segment')
        resolved_single_context_settings = self.get_resolved_single_context_settings(
            segment_specification, 'divisions', context_name, include_improper_parentage=True)
        uninterpreted_division_commands = []
        for resolved_single_context_setting in resolved_single_context_settings:
            #self._debug(resolved_single_context_setting, 'rscs')
            uninterpreted_division_command = \
                self.resolved_single_context_setting_to_uninterpreted_division_command(
                resolved_single_context_setting, segment_specification)
            uninterpreted_division_commands.append(uninterpreted_division_command)
        #print ''
        return uninterpreted_division_commands

    def get_voice_division_list(self, voice):
        voice_division_list = self.score_specification.contexts[voice.name].get('voice_division_list')
        if voice_division_list is None:
            time_signatures = self.score_specification.time_signatures
            voice_division_list = divisiontools.VoiceDivisionList(time_signatures)
        return voice_division_list

    def instantiate_score(self):
        score = self.score_specification.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        score.insert(0, context)
        return score

    def make_default_rhythm_command_for_segment(self, segment_specification):
        from experimental import interpretertools
        return interpretertools.RhythmCommand(
            library.skip_filled_tokens, 
            segment_specification.segment_name,
            self.score_specification.score_name,
            0,
            segment_specification.duration,
            segment_specification.duration,
            True
            )

    def make_default_uninterpreted_division_command_for_segment(self, segment_specification):
        from experimental import interpretertools
        return interpretertools.UninterpretedDivisionCommand(
            segment_specification.time_signatures,
            segment_specification.segment_name,
            self.score_specification.score_name,
            0,
            segment_specification.duration,
            segment_specification.duration,
            True, 
            False
            )

    def make_division_region_division_lists_for_voice(self, voice):
        uninterpreted_division_commands = self.get_uninterpreted_division_commands_for_voice(voice)
        #self._debug_values(uninterpreted_division_commands, 'udc')
        region_division_commands = self.uninterpreted_division_commands_to_region_division_commands(
            uninterpreted_division_commands)
        #self._debug_values(region_division_commands, 'rdc')
        region_division_commands = self.supply_missing_region_division_commands(region_division_commands, voice)
        #self._debug_values(region_division_commands, 'srdc')
        self.region_division_commands_to_division_region_division_lists(region_division_commands, voice)
        #self._debug_values(
        #    self.score_specification.contexts[voice.name]['division_region_division_lists'], 'drdl')

    def make_rhythm_command(
        self, resolved_single_context_setting, segment_name, duration, start_offset, stop_offset):
        from experimental import interpretertools
        rhythm_command = interpretertools.RhythmCommand(
            resolved_single_context_setting.resolved_value, 
            segment_name,
            resolved_single_context_setting.context_name,
            start_offset,
            stop_offset,
            duration,
            resolved_single_context_setting.fresh
            )
        return rhythm_command

    def make_rhythms_and_add_to_voice(self, voice, rhythm_makers, rhythm_region_division_lists):
        for rhythm_maker, rhythm_region_division_list in zip(rhythm_makers, rhythm_region_division_lists):
            if rhythm_region_division_list:
                rhythm_region_division_list = divisiontools.RhythmRegionDivisionList(
                    rhythm_region_division_list)
                self.add_rhythm_to_voice(voice, rhythm_maker, rhythm_region_division_list)

    def make_segment_division_lists_for_voice(self, voice):
        #self._debug(voice, 'voice')
        voice_division_list = self.score_specification.contexts[voice.name]['voice_division_list']
        voice_divisions = [mathtools.NonreducedFraction(x) for x in voice_division_list.divisions]
        #self._debug(voice_divisions, 'vd')
        segment_durations = self.score_specification.segment_durations
        #self._debug(segment_durations, 'sd')
        shards = sequencetools.split_sequence_by_weights(
            voice_divisions, segment_durations, cyclic=False, overhang=True)
        raw_segment_division_lists = []
        for i, shard in enumerate(shards[:]):
            raw_segment_division_list = divisiontools.SegmentDivisionList(shard)
            raw_segment_division_lists.append(raw_segment_division_list)
        #self._debug(voice_division_list, 'vdl')
        #self._debug(raw_segment_division_lists, 'rsdl')
        segment_division_lists = self.fix_boundary_indicators_to_raw_segment_division_lists(
            voice_division_list, raw_segment_division_lists)
        return segment_division_lists

    def make_time_signature_region_division_command(self, voice, start_offset, stop_offset):
        from experimental import interpretertools
        divisions = self.get_time_signature_slice(start_offset, stop_offset)
        start_segment_name = self.score_specification.score_offset_to_segment_identifier(start_offset)
        fresh, truncate = True, True
        duration = stop_offset - start_offset
        region_division_command = interpretertools.RegionDivisionCommand(
            divisions,
            start_segment_name,
            voice.name, 
            start_offset,
            stop_offset,
            duration, 
            fresh,
            truncate
            )
        #self._debug(region_division_command, 'rdc')
        return region_division_command

    def make_uninterpreted_division_command(
        self, resolved_single_context_setting, segment_name, duration, start_offset, stop_offset):
        from experimental import interpretertools
        uninterpreted_division_command = interpretertools.UninterpretedDivisionCommand(
            resolved_single_context_setting.resolved_value,
            segment_name,
            resolved_single_context_setting.context_name,
            start_offset,
            stop_offset,
            duration,
            resolved_single_context_setting.fresh,
            resolved_single_context_setting.truncate
            )
        return uninterpreted_division_command

    def make_voice_division_list_for_voice(self, voice):
        division_region_division_lists = self.score_specification.contexts[voice.name][
            'division_region_division_lists']
        voice_divisions = []
        for division_region_division_list in division_region_division_lists:
            voice_divisions.extend(division_region_division_list.divisions)
        voice_division_list = divisiontools.VoiceDivisionList(voice_divisions)
        return voice_division_list

    def material_request_to_resolved_single_context_setting(self, material_request):
        #self._debug(material_request, 'mr')
        segment_specification = self.get_segment_specification(material_request.segment_identifier)
        context_proxy = segment_specification.resolved_single_context_settings[material_request.context_name]
        resolved_single_context_setting = context_proxy.get_setting(attribute=material_request.attribute)
        #self._debug(resolved_single_context_setting, 'rscs')
        return resolved_single_context_setting

    def region_division_command_to_division_region_division_list(self, region_division_command):
        #self._debug(region_division_command, 'rdc')
        resolved_value = region_division_command.resolved_value
        if isinstance(resolved_value, list):
            divisions = [mathtools.NonreducedFraction(x) for x in resolved_value]
            region_duration = region_division_command.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
            divisions = [x.pair for x in divisions]
            divisions = [divisiontools.Division(x) for x in divisions]
        elif isinstance(resolved_value, requesttools.MaterialRequest):
            assert resolved_value.attribute == 'divisions'
            division_material_request = resolved_value
            divisions = self.division_material_request_to_divisions(division_material_request)
        else:
            raise NotImplementedError('implement for {!r}.'.format(resolved_value))
        segment_specification = self.get_segment_specification(region_division_command.start_segment_name)
        segment_selector = segment_specification.selector
        start_offset, stop_offset = region_division_command.start_offset, region_division_command.stop_offset
        start_timepoint = timespaninequalitytools.Timepoint(anchor=segment_selector, addendum=start_offset)
        stop_timepoint = timespaninequalitytools.Timepoint(anchor=segment_selector, addendum=stop_offset)
        division_region_division_list = divisiontools.DivisionRegionDivisionList(divisions)
        division_region_division_list._start_timepoint = start_timepoint    
        division_region_division_list._stop_timepoint = stop_timepoint
        division_region_division_list._fresh = region_division_command.fresh
        division_region_division_list._truncate = region_division_command.truncate
        return division_region_division_list

    # NEXT TODO: Extend the loop in this function to save intermediate values as they are produced.
    #            This will enable later division commands to refer to the materials produced by earlier commands.
    def region_division_commands_to_division_region_division_lists(self, region_division_commands, voice):
        self.score_specification.contexts[voice.name]['division_region_division_lists'] = []
        for region_division_command in region_division_commands:
            #self._debug(region_division_command, 'rdc')
            division_region_division_list = self.region_division_command_to_division_region_division_list(
                region_division_command)
            self.score_specification.contexts[voice.name]['division_region_division_lists'].append(
                division_region_division_list)
            #self._debug(division_region_division_list, 'drdl')
            #print ''

    def resolve_material_request(self, material_request):
        assert isinstance(material_request, requesttools.MaterialRequest), repr(material_request)
        resolved_single_context_setting = self.material_request_to_resolved_single_context_setting(
            material_request)
        resolved_value = resolved_single_context_setting.resolved_value
        #self._debug(resolved_value, 'rv')
        assert resolved_value is not None, repr(resolved_value)
        if material_request.callback is not None:
            resolved_value = material_request.callback(resolved_value)
        resolved_value = requesttools.apply_request_transforms(material_request, resolved_value)
        #self._debug(resolved_value, 'rv')
        return resolved_value

    def resolve_single_context_setting(self, single_context_setting):
        if isinstance(single_context_setting, settingtools.ResolvedSingleContextSetting):
            return single_context_setting
        value = self.resolve_single_context_setting_source(single_context_setting.source)
        #self._debug(value, 'value')
        args = (
            single_context_setting.attribute,
            single_context_setting.source,
            value,
            single_context_setting.selector,
            )
        resolved_single_context_setting = settingtools.ResolvedSingleContextSetting(
            *args,
            context_name=single_context_setting.context_name,
            persist=single_context_setting.persist,
            truncate=single_context_setting.truncate,
            fresh=single_context_setting.fresh
            )
        return resolved_single_context_setting

    def resolve_single_context_setting_source(self, source):
        if isinstance(source, requesttools.MaterialRequest) and source.attribute == 'time_signatures':
            return self.resolve_material_request(source)
        # the following line should be resolvable
        elif isinstance(source, requesttools.MaterialRequest) and source.attribute == 'divisions':
            return source
        elif isinstance(source, requesttools.StatalServerRequest):
            return source()
        else:
            return source

    def resolved_single_context_setting_to_rhythm_command(
        self, resolved_single_context_setting, segment_specification):
        selector = resolved_single_context_setting.selector
        assert selector.segment_identifier == segment_specification.segment_name
        context_name = resolved_single_context_setting.context_name
        duration = selector.get_duration(self.score_specification, context_name)
        start_offset, stop_offset = selector.get_segment_offsets(self.score_specification, context_name)
        segment_name = segment_specification.segment_name
        rhythm_command = self.make_rhythm_command(
            resolved_single_context_setting, segment_name, duration, start_offset, stop_offset)
        #self._debug(rhythm_command, 'rc')
        return rhythm_command

    def resolved_single_context_setting_to_uninterpreted_division_command(
        self, resolved_single_context_setting, segment_specification):
        selector = resolved_single_context_setting.selector
        assert selector.segment_identifier == segment_specification.segment_name
        context_name = resolved_single_context_setting.context_name
        duration = selector.get_duration(self.score_specification, context_name)
        start_offset, stop_offset = selector.get_segment_offsets(self.score_specification, context_name)
        segment_name = segment_specification.segment_name
        uninterpreted_division_command = self.make_uninterpreted_division_command(
            resolved_single_context_setting, segment_name, duration, start_offset, stop_offset)
        #self._debug(uninterpreted_division_command, 'udc')
        return uninterpreted_division_command

    def sort_and_split_raw_commands(self, raw_commands):
        cooked_commands = []
        start_segment_names = [x.start_segment_name for x in raw_commands]
        assert sequencetools.all_are_equal(start_segment_names)
        #self._debug_values(raw_commands, 'raw')
        for raw_command in raw_commands:
            command_was_delayed, command_was_split = False, False
            commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split = [], [], [], []
            for cooked_command in cooked_commands:
                if raw_command.improperly_contains(cooked_command):
                    commands_to_remove.append(cooked_command)
                elif raw_command.delays(cooked_command):
                    commands_to_delay.append(cooked_command)
                elif raw_command.curtails(cooked_command):
                    commands_to_curtail.append(cooked_command)
                elif cooked_command.properly_contains(raw_command):
                    commands_to_split.append(cooked_command)
            #print commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split
            for command_to_remove in commands_to_remove:
                cooked_commands.remove(command_to_remove)
            for command_to_curtail in commands_to_curtail:
                command_to_curtail._stop_offset = raw_command.start_offset
                duration = command_to_curtail.stop_offset - command_to_curtail.start_offset
                command_to_curtail._duration = duration
            for command_to_delay in commands_to_delay:
                command_to_delay._start_offset = raw_command.stop_offset
                duration = command_to_delay.stop_offset - command_to_delay.start_offset
                command_to_delay._duration = duration
                command_was_delayed = True
            for command_to_split in commands_to_split:
                left_command = command_to_split
                middle_command = raw_command
                right_command = copy.deepcopy(left_command)
                left_command._stop_offset = middle_command.start_offset
                left_duration = left_command.stop_offset - left_command.start_offset
                left_command._duration = left_duration
                right_command._start_offset = middle_command.stop_offset
                right_duration = right_command.stop_offset - right_command.start_offset
                right_command._duration = right_duration
                command_was_split = True
            if command_was_delayed:
                index = cooked_commands.index(cooked_command)
                cooked_commands.insert(index, raw_command)
            elif command_was_split:
                cooked_commands.append(middle_command)
                cooked_commands.append(right_command)
            else:
                cooked_commands.append(raw_command)
            cooked_commands.sort()
            #self._debug_values(cooked_commands, 'cooked')
        #self._debug_values(cooked_commands, 'cooked')
        return cooked_commands

    def store_additional_single_context_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_resolved_single_context_setting(self,
        segment_specification, resolved_single_context_setting, clear_persistent_first=False):
        context_name = resolved_single_context_setting.context_name
        if context_name is None:
            context_name = segment_specification.resolved_single_context_settings.score_name
        attribute = resolved_single_context_setting.attribute
        if clear_persistent_first:
            self.clear_persistent_resolved_single_context_settings(context_name, attribute)
        if attribute in segment_specification.resolved_single_context_settings[context_name]:
            segment_specification.resolved_single_context_settings[context_name][attribute].append(
                resolved_single_context_setting)
        else:
            segment_specification.resolved_single_context_settings[context_name][attribute] = [
                resolved_single_context_setting]
        if resolved_single_context_setting.persist:
            if attribute in self.score_specification.resolved_single_context_settings[context_name]:
                self.score_specification.resolved_single_context_settings[context_name][attribute].append(
                    resolved_single_context_setting)
            else:
                self.score_specification.resolved_single_context_settings[context_name][attribute] = [
                    resolved_single_context_setting]

    def store_single_context_division_settings(self):
        '''For every segment specification:

        Get new single-context division settings for segment.

        If no new single-context division settings exist, then copy existing
        resolved single-context division settings from global score context.

        Then store single-context division settings in global score context.
        '''
        for segment_specification in self.score_specification.segment_specifications:
            new_settings = segment_specification.single_context_settings.get_settings(attribute='divisions')
            #self._debug(segment_specification, 'segment')
            #self._debug_values(new_settings, 'ns')
            if not new_settings:
                new_settings = []
                existing_settings = self.score_specification.resolved_single_context_settings.get_settings(
                    attribute='divisions')
                for existing_setting in existing_settings:
                    #self._debug(existing_setting, 'es')
                    new_setting = existing_setting.copy_setting_to_segment(segment_specification)
                    new_settings.append(new_setting)
            #self._debug_values(new_settings, 'NS')
            self.store_single_context_settings(new_settings, clear_persistent_first=True)

    def store_single_context_pitch_class_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_single_context_registration_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_single_context_rhythm_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            settings = segment_specification.single_context_settings.get_settings(attribute='rhythm')
            if not settings:
                settings = []
                existing_settings = self.score_specification.resolved_single_context_settings.get_settings(
                    attribute='rhythm')
                for existing_setting in existing_settings:
                    setting = existing_setting.copy_setting_to_segment(segment_specification)
                    settings.append(setting)
            self.store_single_context_settings(settings, clear_persistent_first=True)

    def store_single_context_setting(self, single_context_setting, clear_persistent_first=False):
        '''Resolve single-context setting and find segment in which single-context setting starts.

        Store resolved single-context setting in segment resolved single-context settings.

        If setting persists then store setting in score resolved single-context settings, too.
        '''
        resolved_single_context_setting = self.resolve_single_context_setting(single_context_setting)
        #self._debug(resolved_single_context_setting, 'rscs')
        selector = resolved_single_context_setting.selector
        segment_specification = self.get_segment_specification(selector)
        self.store_resolved_single_context_setting(
            segment_specification, resolved_single_context_setting,
            clear_persistent_first=clear_persistent_first)

    def store_single_context_settings(self, single_context_settings, clear_persistent_first=False):
        if single_context_settings:
            self.store_single_context_setting(
                single_context_settings[0], clear_persistent_first=clear_persistent_first)
            for single_context_setting in single_context_settings[1:]:
                #self.store_single_context_setting(
                #    single_context_setting, clear_persistent_first=clear_persistent_first)
                self.store_single_context_setting(single_context_setting, clear_persistent_first=False)

    def store_single_context_time_signature_settings(self):
        '''For each segment:

        Check segment for an explicit time signature setting.

        If none, check score resolved settings context dictionary for current time signature setting.

        Halt interpretation if no time signature setting is found.

        Otherwise store time signature setting.
        '''
        for segment_specification in self.score_specification.segment_specifications:
            settings = segment_specification.single_context_settings.get_settings(attribute='time_signatures')
            if settings:
                assert len(settings) == 1, repr(settings)
                setting = settings[0]
            else:
                settings = self.score_specification.resolved_single_context_settings.get_settings(
                    attribute='time_signatures')
                if not settings:
                    return
                assert len(settings) == 1, repr(settings)
                setting = settings[0]
                setting = setting.copy_setting_to_segment(segment_specification.segment_name)
            assert setting.selector.timespan == segment_specification.timespan, [
                repr(setting), '\n', repr(segment_specification.timespan)]
            self.store_single_context_setting(setting, clear_persistent_first=True)

    def supply_missing_region_division_commands(self, region_division_commands, voice):
        from experimental import interpretertools
        #self._debug_values(region_division_commands, 'rdc')
        if not region_division_commands:
            return region_division_commands
        first_start_offset_in_score = self.score_specification.segment_name_and_segment_offset_to_score_offset(
            region_division_commands[0].start_segment_name,
            region_division_commands[0].start_offset)
        if not first_start_offset_in_score == self.score_specification.start_offset:
            region_division_command = self.make_time_signature_region_division_command(
                voice, self.score_specification.start_offset, first_start_offset_in_score)
            region_division_commands.insert(0, region_division_command)
        last_stop_offset_in_score = self.score_specification.segment_name_and_segment_offset_to_score_offset(
            region_division_commands[-1].start_segment_name,
            region_division_commands[-1].stop_offset)
        if not last_stop_offset_in_score == self.score_specification.stop_offset:
            region_division_command = self.make_time_signature_region_division_command(
                voice, last_stop_offset_in_score, self.score_specification.stop_offset)
            region_division_commands.append(region_division_command)
        if len(region_division_commands) == 1:
            return region_division_commands
        #self._debug_values(region_division_commands, 'midway rdc')
        result = []
        for left_region_division_command, right_region_division_command in \
            sequencetools.iterate_sequence_pairwise_strict(region_division_commands):
            left_stop_offset_in_score = self.score_specification.segment_name_and_segment_offset_to_score_offset(
                left_region_division_command.start_segment_name,
                left_region_division_command.stop_offset)
            right_start_offset_in_score = self.score_specification.segment_name_and_segment_offset_to_score_offset(
                right_region_division_command.start_segment_name,
                right_region_division_command.start_offset)
            #self._debug((left_stop_offset_in_score, right_start_offset_in_score), 'offsets')
            assert left_stop_offset_in_score <= right_start_offset_in_score
            result.append(left_region_division_command)
            if left_stop_offset_in_score < right_start_offset_in_score:
                region_division_command = self.make_time_signature_region_division_command(
                    voice, left_stop_offset_in_score, right_start_offset_in_score)
                result.append(region_division_command)
        result.append(right_region_division_command)
        #self._debug_values(result, 'result')
        return result

    def uninterpreted_division_commands_to_region_division_commands(self, uninterpreted_division_commands):
        #self._debug(len(uninterpreted_division_commands), 'total')
        from experimental import interpretertools
        region_division_commands = []
        if not uninterpreted_division_commands:
            return []
        if any([x.resolved_value is None for x in uninterpreted_division_commands]):
            return []
        assert uninterpreted_division_commands[0].fresh, repr(uninterpreted_division_commands[0])
        for uninterpreted_division_command in uninterpreted_division_commands:
            #self._debug(uninterpreted_division_command, 'udc')
            if uninterpreted_division_command.fresh or uninterpreted_division_command.truncate:
                region_division_command = interpretertools.RegionDivisionCommand(
                    *uninterpreted_division_command.vector)
                region_division_commands.append(region_division_command)
            else:
                last_region_division_command = region_division_commands[-1]
                if uninterpreted_division_command.resolved_value != last_region_division_command.resolved_value:
                    region_division_command = interpretertools.RegionDivisionCommand(
                        *uninterpreted_division_command.vector)
                    region_division_commands.append(region_division_command)
                elif last_region_division_command.truncate:
                    region_division_command = interpretertools.RegionDivisionCommand(
                        *uninterpreted_division_command.vector)
                    region_division_commands.append(region_division_command)
                else:
                    duration = last_region_division_command.duration + uninterpreted_division_command.duration
                    start_offset = last_region_division_command.start_offset
                    stop_offset = last_region_division_command.stop_offset + \
                        uninterpreted_division_command.duration
                    region_division_command = interpretertools.RegionDivisionCommand(
                        last_region_division_command.resolved_value,
                        last_region_division_command.start_segment_name,
                        uninterpreted_division_command.context_name,
                        start_offset,
                        stop_offset,
                        duration,
                        last_region_division_command.fresh,
                        uninterpreted_division_command.truncate
                        )
                    region_division_commands[-1] = region_division_command
        #self._debug(region_division_commands)
        return region_division_commands

    def unpack_multiple_context_settings_for_score(self):
        for segment_specification in self.score_specification.segment_specifications:
            settings = self.unpack_multiple_context_settings_for_segment(segment_specification)
            self.score_specification.single_context_settings.extend(settings)

    def unpack_multiple_context_settings_for_segment(self, segment_specification):
        for multiple_context_setting in segment_specification.multiple_context_settings:
            segment_specification.single_context_settings.extend(multiple_context_setting.unpack())
        return segment_specification.single_context_settings
