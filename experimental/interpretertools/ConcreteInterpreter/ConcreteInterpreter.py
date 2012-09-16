import copy
import fractions
from abjad.tools import *
from experimental import divisiontools
from experimental import helpertools
from experimental import library
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespaninequalitytools
from experimental import timespantools
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
        Interpreter.__call__(self, score_specification)
        self.add_time_signatures_to_score()
        self.calculate_score_and_segment_durations()
        self.add_division_lists_to_voices()
        self.add_rhythm_to_voices()
        self.apply_pitch_classes()
        self.apply_registration()
        self.apply_additional_parameters()
        return self.score

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

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

    def add_division_lists_to_voices(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_division_lists_to_voice(voice)

    # TODO: Might make more sense to iterate all rhythm command scorewide
    #       (Rather than voicewide).
    # TODO: Extend this method to handle rhythm commands one after the other.
    #       This will parallel the way that division commands are interpreted.
    #       This will also enable look-back behavior.
    #       Look-back behavior will enable rhythm request interpretation.
    def add_rhythm_to_voice(self, voice):
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
        #self._debug_values(rhythm_commands, 'lrc')
        rhythm_command_durations = [x.duration for x in rhythm_commands]
        #self._debug(rhythm_command_durations, 'rcd')
        key = 'division_region_division_lists'
        division_region_division_lists = self.score_specification.contexts[voice.name][key]
        #self._debug_values(division_region_division_lists, 'drdls')
        division_region_durations = [x.duration for x in division_region_division_lists]
        #self._debug(division_region_durations, 'drd')
        rhythm_region_durations = sequencetools.merge_duration_sequences(
            division_region_durations, rhythm_command_durations)
        #self._debug(rhythm_region_durations, 'rrd')
        args = (voice_division_durations, rhythm_region_durations)
        rhythm_region_division_duration_lists = \
            sequencetools.partition_sequence_by_backgrounded_weights(*args)
        #self._debug_values(rhythm_region_division_duration_lists, 'rrddls')
        assert len(rhythm_region_division_duration_lists) == len(rhythm_region_durations)
        rhythm_region_lengths = [len(l) for l in rhythm_region_division_duration_lists]
        rhythm_region_division_lists = sequencetools.partition_sequence_by_counts(
            voice_divisions, rhythm_region_lengths, cyclic=False, overhang=False)
        rhythm_region_division_lists = [
            divisiontools.RhythmRegionDivisionList(x) for x in rhythm_region_division_lists]
        assert len(rhythm_region_division_lists) == len(rhythm_region_durations)
        #self._debug_values(rhythm_region_division_lists, 'rrdls')
        input_pairs = []
        # might make more sense for this to be the main loop of this method
        for command in rhythm_commands:
            if isinstance(command.request, requesttools.AbsoluteRequest):
                input_pairs.append((command.request.payload, command.duration))
            elif isinstance(command.request, requesttools.MaterialRequest):
                assert command.attribute == 'rhythm'
                #print command.storage_format
                input_pairs.append((command.request, command.duration))
            else:
                raise TypeError('unknown request {!r}?'.format(command.request))
        output_pairs = sequencetools.pair_duration_sequence_elements_with_input_pair_values(
            rhythm_region_durations, input_pairs)
        rhythm_makers = [output_pair[-1] for output_pair in output_pairs]
        assert len(rhythm_makers) == len(rhythm_region_division_lists)
        #self._debug_values(rhythm_makers, 'makers')
        #self._debug_values(rhythm_region_division_lists, 'rrdls')
        self.make_rhythms(voice, rhythm_makers, rhythm_region_division_lists)

    def add_rhythm_to_voices(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_rhythm_to_voice(voice)

    def add_segment_division_lists_to_voice(
        self, voice, segment_division_lists):
        assert len(self.score_specification.segment_specifications) == len(segment_division_lists)
        for segment_specification, segment_division_list in zip(
            self.score_specification.segment_specifications, segment_division_lists):
            segment_specification.contexts[voice.name]['segment_division_list'] = segment_division_list
            segment_specification.contexts[voice.name]['segment_pairs'] = [
                x.pair for x in segment_division_list]

    def add_time_signatures_to_segment(self, segment_specification):
        time_signatures = self.make_time_signatures_for_segment_specification(segment_specification)
        if time_signatures is not None:
            measures = measuretools.make_measures_with_full_measure_spacer_skips(time_signatures)
            context = componenttools.get_first_component_in_expr_with_name(self.score, 'TimeSignatureContext')
            context.extend(measures)

    def add_time_signatures_to_score(self):
        for segment_specification in self.score_specification.segment_specifications:
            self.add_time_signatures_to_segment(segment_specification)

    def apply_additional_parameters(self):
        pass

    def apply_pitch_classes(self):
        pass

    def apply_registration(self):
        pass

    def calculate_score_and_segment_durations(self):
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

    def clear_persistent_single_context_settings_by_context(self, context_name, attribute):
        if attribute in self.score_specification.single_context_settings_by_context[context_name]:
            del(self.score_specification.single_context_settings_by_context[context_name][attribute])

    def conditionally_beam_rhythm_containers(self, rhythm_maker, rhythm_containers):
        if getattr(rhythm_maker, 'beam', False):
            durations = [x.preprolated_duration for x in rhythm_containers]
            beamtools.DuratedComplexBeamSpanner(rhythm_containers, durations=durations, span=1)

    def context_name_to_parentage_names(self, segment_specification, context_name, proper=True):
        context = componenttools.get_first_component_in_expr_with_name(
            segment_specification.score_model, context_name)
        if proper:
            parentage = componenttools.get_proper_parentage_of_component(context)
        else:
            parentage = componenttools.get_improper_parentage_of_component(context)
        context_names = [context.name for context in parentage]
        return context_names

    def division_command_request_to_divisions(
        self, division_command_request, region_division_commands, voice_name):
        assert isinstance(division_command_request, requesttools.CommandRequest)
        assert division_command_request.attribute == 'divisions'
        #self._debug(division_command_request, 'dcr')
        #self._debug_values(region_division_commands, 'rdcs')
        requested_segment_identifier = division_command_request.timepoint.start_segment_identifier
        requested_segment_offset = division_command_request.timepoint.get_segment_offset(
            self.score_specification, voice_name)
        timespan_inventory = timespantools.TimespanInventory()
        for region_division_command in region_division_commands:
            if region_division_command.start_segment_identifier == requested_segment_identifier:
                if not region_division_command.request == division_command_request:
                    timespan_inventory.append(region_division_command)
        timespan_inequality = timespaninequalitytools.timepoint_happens_during_timespan(
            timepoint=requested_segment_offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_inequality(timespan_inequality)
        #self._debug_values(candidate_commands, 'candidates')
        segment_specification = self.get_start_segment_specification(requested_segment_identifier)
        source_command = self.select_first_element_in_expr_by_parentage(
            candidate_commands, segment_specification, division_command_request.context_name, 
            include_improper_parentage=True)
        assert source_command is not None
        #self._debug(source_command, 'source_command')
        absolute_request = source_command.request
        assert isinstance(absolute_request, requesttools.AbsoluteRequest), repr(absolute_request)
        divisions = requesttools.apply_request_transforms(absolute_request, absolute_request.payload)
        return divisions

    def division_material_request_to_divisions(self, division_material_request):
        assert isinstance(division_material_request, requesttools.MaterialRequest)
        assert division_material_request.attribute == 'divisions'
        #self._debug(division_material_request, 'dmr')
        voice_name = division_material_request.context_name
        start_segment_identifier = division_material_request.start_segment_identifier
        stop_segment_identifier = division_material_request.stop_segment_identifier
        selection_start_offset = division_material_request.start_offset
        selection_stop_offset = division_material_request.stop_offset
        divisions = self.voice_name_to_divisions(voice_name)
        divisions = self.keep_divisions_between_segments(
            divisions, start_segment_identifier, stop_segment_identifier)
        divisions = self.keep_divisions_between_selection_offsets(
            divisions, selection_start_offset, selection_stop_offset)
        divisions = requesttools.apply_request_transforms(division_material_request, divisions)
        return divisions

    def divisions_to_division_region_division_list(self, divisions, region_division_command):
        segment_specification = self.get_start_segment_specification(
            region_division_command.start_segment_identifier)
        segment_selector = segment_specification.selector
        segment_start_offset = region_division_command.segment_start_offset
        segment_stop_offset = region_division_command.segment_stop_offset
        start_timepoint = timespantools.SymbolicTimepoint(
            selector=segment_selector, offset=segment_start_offset)
        stop_timepoint = timespantools.SymbolicTimepoint(
            selector=segment_selector, offset=segment_stop_offset)
        division_region_division_list = divisiontools.DivisionRegionDivisionList(divisions)
        division_region_division_list._start_timepoint = start_timepoint    
        division_region_division_list._stop_timepoint = stop_timepoint
        return division_region_division_list

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
            if rhythm_command.request == result[-1].request and not rhythm_command.fresh:
                result[-1]._duration += rhythm_command.duration
            else:
                result.append(copy.deepcopy(rhythm_command))
        return result

    def get_all_region_division_commands(self):
        all_division_commands = []
        if not self.score_specification.segment_specifications:
            return all_division_commands
        first_segment = self.get_start_segment_specification(0)
        for voice in voicetools.iterate_voices_forward_in_expr(first_segment.score_model):
            #self._debug(voice, 'voice')
            division_commands = self.get_uninterpreted_division_commands_for_voice(voice)
            division_commands = self.uninterpreted_division_commands_to_region_division_commands(
                division_commands)
            division_commands = self.supply_missing_region_division_commands(
                division_commands, voice)
            all_division_commands.extend(division_commands)
        #self._debug(all_division_commands, 'all #0')
        return all_division_commands

    def get_single_context_settings_by_context(self, segment_specification, attribute, context_name,
        include_improper_parentage=False):
        result = []
        context_names = [context_name]
        if include_improper_parentage:
            context_names.extend(self.context_name_to_parentage_names(segment_specification, context_name))
        for context_name in reversed(context_names):
            single_context_settings = segment_specification.single_context_settings_by_context[context_name]
            single_context_settings = single_context_settings.get_settings(attribute=attribute)
            result.extend(single_context_settings)
        return result

    def get_rhythm_commands_for_voice(self, voice):
        rhythm_commands = []
        for segment_specification in self.score_specification.segment_specifications:
            raw_commands = self.get_rhythm_commands_that_start_during_segment(
                segment_specification, voice.name)
            #self._debug(raw_commands, 'raw')
            default_command = self.make_default_rhythm_command_for_segment_specification(segment_specification)
            raw_commands.insert(0, default_command)
            #self._debug(raw_commands, 'raw')
            cooked_commands = self.sort_and_split_raw_commands(raw_commands)
            #self._debug(cooked_commands, 'cooked')
            rhythm_commands.extend(cooked_commands)
        return rhythm_commands

    def get_rhythm_commands_that_start_during_segment(self, segment_specification, context_name):
        #self._debug(segment_specification, 'segment')
        single_context_settings = self.get_single_context_settings_by_context(
            segment_specification, 'rhythm', context_name, include_improper_parentage=True)
        rhythm_commands = []
        for single_context_setting in single_context_settings:
            #self._debug(single_context_setting)
            rhythm_command = \
                self.single_context_setting_to_rhythm_command(
                single_context_setting, segment_specification)
            rhythm_commands.append(rhythm_command)
        #print ''
        return rhythm_commands

    def get_start_segment_specification(self, expr):
        return self.score_specification.get_start_segment_specification(expr)

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
                command = self.make_default_uninterpreted_division_command_for_segment_specification(segment_specification)
                uninterpreted_division_commands.append(command)
        return uninterpreted_division_commands

    def get_uninterpreted_division_commands_that_start_during_segment(self, 
        segment_specification, context_name):
        #self._debug(segment_specification, 'segment')
        single_context_settings = self.get_single_context_settings_by_context(
            segment_specification, 'divisions', context_name, include_improper_parentage=True)
        uninterpreted_division_commands = []
        for single_context_setting in single_context_settings:
            #self._debug(single_context_setting, 'rscs')
            uninterpreted_division_command = \
                self.single_context_setting_to_uninterpreted_division_command(
                single_context_setting, segment_specification)
            uninterpreted_division_commands.append(uninterpreted_division_command)
        #print ''
        return uninterpreted_division_commands

    def get_voice_division_list(self, voice):
        voice_division_list = self.score_specification.contexts[voice.name].get('voice_division_list')
        if voice_division_list is None:
            time_signatures = self.score_specification.time_signatures
            voice_division_list = divisiontools.VoiceDivisionList(time_signatures)
        return voice_division_list

    def keep_divisions_between_segments(self, divisions, start_segment_identifier, stop_segment_identifier):
        start_segment_index = self.score_specification.segment_identifier_expression_to_segment_index(
            start_segment_identifier)
        stop_segment_index = self.score_specification.segment_identifier_expression_to_segment_index(
            stop_segment_identifier)
        segment_count =  stop_segment_index - start_segment_index
        score_start_offset, score_stop_offset = self.score_specification.segment_name_to_segment_offsets(
            start_segment_index, segment_count)
        total_amount = score_stop_offset - score_start_offset
        divisions = sequencetools.split_sequence_by_weights(
            divisions, [0, total_amount], cyclic=False, overhang=True)
        divisions = divisions[1]
        #self._debug(divisions, 'divisions')
        return divisions

    def keep_divisions_between_selection_offsets(
        self, divisions, selection_start_offset, selection_stop_offset):
        total_divisions = sum(divisions)
        if selection_start_offset is None:
            selection_start_offset = durationtools.Offset(0)
        if selection_stop_offset is None:
            selection_stop_offset = total_divisions
        first_weight = fractions.Fraction(selection_start_offset)
        second_weight = selection_stop_offset - selection_start_offset
        second_weight = fractions.Fraction(second_weight)
        weights = [first_weight, second_weight]
        third_weight = total_divisions - selection_stop_offset
        third_weight = fractions.Fraction(third_weight)
        if third_weight:
            weights.append(third_weight)
        #self._debug(weights, 'weights')
        divisions = sequencetools.split_sequence_by_weights(
            divisions, weights, cyclic=False, overhang=True)
        divisions = divisions[1]
        return divisions

    def make_default_rhythm_command_for_segment_specification(self, segment_specification):
        from experimental import interpretertools
        return interpretertools.RhythmCommand(
            requesttools.AbsoluteRequest(library.skip_filled_tokens), 
            segment_specification.segment_name,
            self.score_specification.score_name,
            0,
            segment_specification.duration,
            segment_specification.duration,
            fresh=True
            )

    def make_default_uninterpreted_division_command_for_segment_specification(self, segment_specification):
        from experimental import interpretertools
        return interpretertools.DivisionCommand(
            requesttools.AbsoluteRequest(segment_specification.time_signatures),
            segment_specification.segment_name,
            self.score_specification.score_name,
            0,
            segment_specification.duration,
            segment_specification.duration,
            fresh=True, 
            truncate=False
            )

    def make_division_region_division_lists_for_voice(self, voice):
        uninterpreted_division_commands = self.get_uninterpreted_division_commands_for_voice(voice)
        #self._debug_values(uninterpreted_division_commands, 'udc')
        region_division_commands = self.uninterpreted_division_commands_to_region_division_commands(
            uninterpreted_division_commands)
        #self._debug_values(region_division_commands, 'rdc')
        region_division_commands = self.supply_missing_region_division_commands(
            region_division_commands, voice)
        #self._debug_values(region_division_commands, 'srdc')
        all_region_division_commands = self.get_all_region_division_commands()
        #self._debug(all_region_division_commands, 'all #1')
        self.region_division_commands_to_division_region_division_lists(
            region_division_commands, voice, all_region_division_commands)

    def make_rhythm(self, voice, rhythm_maker, rhythm_region_division_list):
#        self._debug(rhythm_maker)
#        self._debug(rhythm_region_division_list)
        assert isinstance(rhythm_maker, timetokentools.TimeTokenMaker), repr(rhythm_maker)
        assert isinstance(rhythm_region_division_list, divisiontools.RhythmRegionDivisionList)
        leaf_lists = rhythm_maker(rhythm_region_division_list.pairs)
        rhythm_containers = [containertools.Container(x) for x in leaf_lists]
        voice.extend(rhythm_containers)
        self.conditionally_beam_rhythm_containers(rhythm_maker, rhythm_containers)

    def make_rhythm_command(
        self, single_context_setting, segment_name, duration, start_offset, stop_offset):
        from experimental import interpretertools
        rhythm_command = interpretertools.RhythmCommand(
            single_context_setting.request, 
            segment_name,
            single_context_setting.context_name,
            start_offset,
            stop_offset,
            duration,
            index=single_context_setting.index,
            count=single_context_setting.count,
            reverse=single_context_setting.reverse,
            rotation=single_context_setting.rotation,
            callback=single_context_setting.callback,
            fresh=single_context_setting.fresh
            )
        return rhythm_command

    def make_rhythms(self, voice, rhythm_makers, rhythm_region_division_lists):
        for rhythm_maker, rhythm_region_division_list in zip(rhythm_makers, rhythm_region_division_lists):
            if rhythm_region_division_list:
                self.make_rhythm(voice, rhythm_maker, rhythm_region_division_list)

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

    def make_time_signature_division_command(self, voice, start_offset, stop_offset):
        from experimental import interpretertools
        divisions = self.get_time_signature_slice(start_offset, stop_offset)
        segment_identifier = self.score_specification.score_offset_to_segment_identifier(start_offset)
        duration = stop_offset - start_offset
        division_command = interpretertools.DivisionCommand(
            requesttools.AbsoluteRequest(divisions),
            segment_identifier,
            voice.name, 
            start_offset,
            stop_offset,
            duration, 
            fresh=True,
            truncate=True
            )
        #self._debug(division_command, 'rdc')
        return division_command

    def make_time_signatures_for_segment_specification(self, segment_specification):
        time_signature_settings = \
            segment_specification.single_context_settings_by_context.score_context_proxy.get_settings(
            attribute='time_signatures')
        if not len(time_signature_settings) == 1:
            return
        time_signature_setting = time_signature_settings[0]
        #self._debug(time_signature_setting, 'tss')
        if isinstance(time_signature_setting.request, requesttools.AbsoluteRequest):
            time_signatures = time_signature_setting.request.payload
            time_signatures = requesttools.apply_request_transforms(
                time_signature_setting.request, time_signatures)
        elif isinstance(time_signature_setting.request, requesttools.MaterialRequest):
            time_signatures = self.time_signature_material_request_to_time_signatures(
                time_signature_setting.request)
        else:
            raise NotImplementedError('implement time signature creation for {!r}'.format(
                time_signature_setting.request))
        time_signatures = requesttools.apply_request_transforms(time_signature_setting, time_signatures)
        segment_specification._time_signatures = time_signatures[:]
        return time_signatures

    def make_uninterpreted_division_command(
        self, single_context_setting, segment_name, duration, start_offset, stop_offset):
        from experimental import interpretertools
        uninterpreted_division_command = interpretertools.DivisionCommand(
            single_context_setting.request,
            segment_name,
            single_context_setting.context_name,
            start_offset,
            stop_offset,
            duration,
            index=single_context_setting.index,
            count=single_context_setting.count,
            reverse=single_context_setting.reverse,
            rotation=single_context_setting.rotation,
            callback=single_context_setting.callback,
            fresh=single_context_setting.fresh,
            truncate=single_context_setting.truncate
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

    def region_division_command_to_division_region_division_list(
        self, region_division_command, region_division_commands, voice_name):
        #self._debug(region_division_command, 'rdc')
        if isinstance(region_division_command.request, list):
            divisions = region_division_command.request
            divisions = [mathtools.NonreducedFraction(x) for x in divisions]
            region_duration = region_division_command.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
            divisions = [x.pair for x in divisions]
            divisions = [divisiontools.Division(x) for x in divisions]
        elif isinstance(region_division_command.request, requesttools.AbsoluteRequest):
            request = region_division_command.request
            divisions = requesttools.apply_request_transforms(request, request.payload)
            divisions = requesttools.apply_request_transforms(region_division_command, divisions) 
            divisions = [mathtools.NonreducedFraction(x) for x in divisions]
            region_duration = region_division_command.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
            divisions = [x.pair for x in divisions]
            divisions = [divisiontools.Division(x) for x in divisions]
        elif isinstance(region_division_command.request, requesttools.MaterialRequest):
            assert region_division_command.request.attribute == 'divisions'
            division_material_request = region_division_command.request
            divisions = self.division_material_request_to_divisions(division_material_request)
            divisions = requesttools.apply_request_transforms(region_division_command, divisions)
            region_division_command._request = divisions
            division_region_division_list = self.region_division_command_to_division_region_division_list(
                region_division_command, region_division_commands, voice_name)
            return division_region_division_list
        elif isinstance(region_division_command.request, requesttools.CommandRequest):
            assert region_division_command.request.attribute == 'divisions'
            division_command_request = region_division_command.request
            divisions = self.division_command_request_to_divisions(
                division_command_request, region_division_commands, voice_name)
            divisions = requesttools.apply_request_transforms(division_command_request, divisions)
            divisions = requesttools.apply_request_transforms(region_division_command, divisions) 
            region_division_command._request = divisions
            division_region_division_list = self.region_division_command_to_division_region_division_list(
                region_division_command, region_division_commands, voice_name)
            return division_region_division_list
        else:
            raise NotImplementedError('implement for {!r}.'.format(region_division_command.request))
        division_region_division_list = self.divisions_to_division_region_division_list(
            divisions, region_division_command)
        return division_region_division_list

    def region_division_commands_to_division_region_division_lists(self, 
        region_division_commands, voice, all_region_division_commands):
        #self._debug(all_region_division_commands, 'all #2')
        self.score_specification.contexts[voice.name]['division_region_division_lists'] = []
        for region_division_command in region_division_commands:
            #self._debug(region_division_command, 'rdc')
            division_region_division_list = self.region_division_command_to_division_region_division_list(
                region_division_command, all_region_division_commands, voice.name)
            self.score_specification.contexts[voice.name]['division_region_division_lists'].append(
                division_region_division_list)

    def sort_elements_in_expr_by_parentage(self, expr, segment_specification, context_name, 
        include_improper_parentage=False):
        result = []
        context_names = [context_name]
        if include_improper_parentage:
            context_names = self.context_name_to_parentage_names(
                segment_specification, context_name, proper=False)
        for context_name in context_names:
            for element in expr:
                if element.context_name == context_name:
                    result.append(element)
        return result

    def select_first_element_in_expr_by_parentage(self, expr, segment_specification, context_name, 
        include_improper_parentage=False):
        context_names = [context_name]
        if include_improper_parentage:
            context_names = self.context_name_to_parentage_names(
                segment_specification, context_name, proper=False)
        for context_name in context_names:
            for element in expr:
                if element.context_name == context_name:
                    return element

    def single_context_setting_to_rhythm_command(
        self, single_context_setting, segment_specification):
        selector = single_context_setting.selector
        assert selector.start_segment_identifier == segment_specification.segment_name
        context_name = single_context_setting.context_name
        duration = selector.get_duration(self.score_specification, context_name)
        start_offset, stop_offset = selector.get_segment_offsets(self.score_specification, context_name)
        segment_name = segment_specification.segment_name
        rhythm_command = self.make_rhythm_command(
            single_context_setting, segment_name, duration, start_offset, stop_offset)
        #self._debug(rhythm_command, 'rc')
        return rhythm_command

    def single_context_setting_to_uninterpreted_division_command(
        self, single_context_setting, segment_specification):
        selector = single_context_setting.selector
        assert selector.start_segment_identifier == segment_specification.segment_name
        context_name = single_context_setting.context_name
        duration = selector.get_duration(self.score_specification, context_name)
        start_offset, stop_offset = selector.get_segment_offsets(self.score_specification, context_name)
        segment_name = segment_specification.segment_name
        uninterpreted_division_command = self.make_uninterpreted_division_command(
            single_context_setting, segment_name, duration, start_offset, stop_offset)
        #self._debug(uninterpreted_division_command, 'udc')
        return uninterpreted_division_command

    def sort_and_split_raw_commands(self, raw_commands):
        cooked_commands = []
        segment_identifiers = [x.start_segment_identifier for x in raw_commands]
        assert sequencetools.all_are_equal(segment_identifiers)
        #self._debug_values(raw_commands, 'raw')
        for raw_command in raw_commands:
            command_was_delayed, command_was_split = False, False
            commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split = [], [], [], []
            for cooked_command in cooked_commands:
                if timespaninequalitytools.timespan_2_contains_timespan_1_improperly(
                    cooked_command, raw_command):
                    commands_to_remove.append(cooked_command)
                elif timespaninequalitytools.timespan_2_delays_timespan_1(cooked_command, raw_command):
                    commands_to_delay.append(cooked_command)
                elif timespaninequalitytools.timespan_2_curtails_timespan_1(cooked_command, raw_command):
                    commands_to_curtail.append(cooked_command)
                elif timespaninequalitytools.timespan_2_trisects_timespan_1(cooked_command, raw_command):
                    commands_to_split.append(cooked_command)
            #print commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split
            for command_to_remove in commands_to_remove:
                cooked_commands.remove(command_to_remove)
            for command_to_curtail in commands_to_curtail:
                command_to_curtail._segment_stop_offset = raw_command.segment_start_offset
                duration = command_to_curtail.segment_stop_offset - command_to_curtail.segment_start_offset
                command_to_curtail._duration = duration
            for command_to_delay in commands_to_delay:
                command_to_delay._segment_start_offset = raw_command.segment_stop_offset
                duration = command_to_delay.segment_stop_offset - command_to_delay.segment_start_offset
                command_to_delay._duration = duration
                command_was_delayed = True
            for command_to_split in commands_to_split:
                left_command = command_to_split
                middle_command = raw_command
                right_command = copy.deepcopy(left_command)
                left_command._segment_stop_offset = middle_command.segment_start_offset
                left_duration = left_command.segment_stop_offset - left_command.segment_start_offset
                left_command._duration = left_duration
                right_command._segment_start_offset = middle_command.segment_stop_offset
                right_duration = right_command.segment_stop_offset - right_command.segment_start_offset
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

    def store_additional_single_context_settings_by_context(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_interpreter_specific_single_context_settings_by_context(self):
        self.store_single_context_time_signature_settings_by_context()
        self.store_single_context_division_settings_by_context()
        self.store_single_context_rhythm_settings_by_context()
        self.store_single_context_pitch_class_settings_by_context()
        self.store_single_context_registration_settings_by_context()
        self.store_additional_single_context_settings_by_context()

    def store_single_context_division_settings_by_context(self):
        '''For every segment specification:

        Get new single-context division settings for segment.

        If no new single-context division settings exist, then copy existing
        single-context division settings from global score context.

        Then store single-context division settings in global score context.
        '''
        for segment_specification in self.score_specification.segment_specifications:
            new_settings = segment_specification.single_context_settings.get_settings(attribute='divisions')
            #self._debug(segment_specification, 'segment')
            #self._debug_values(new_settings, 'ns')
            if not new_settings:
                new_settings = []
                existing_settings = self.score_specification.single_context_settings_by_context.get_settings(
                    attribute='divisions')
                for existing_setting in existing_settings:
                    #self._debug(existing_setting, 'es')
                    new_setting = existing_setting.copy_setting_to_segment(segment_specification)
                    new_settings.append(new_setting)
            #self._debug_values(new_settings, 'NS')
            self.store_single_context_settings_by_context(new_settings, clear_persistent_first=True)

    def store_single_context_pitch_class_settings_by_context(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_single_context_registration_settings_by_context(self):
        for segment_specification in self.score_specification.segment_specifications:
            pass

    def store_single_context_rhythm_settings_by_context(self):
        for segment_specification in self.score_specification.segment_specifications:
            settings = segment_specification.single_context_settings.get_settings(attribute='rhythm')
            if not settings:
                settings = []
                existing_settings = self.score_specification.single_context_settings_by_context.get_settings(
                    attribute='rhythm')
                for existing_setting in existing_settings:
                    setting = existing_setting.copy_setting_to_segment(segment_specification)
                    settings.append(setting)
            self.store_single_context_settings_by_context(settings, clear_persistent_first=True)

    def store_single_context_time_signature_settings_by_context(self):
        '''For each segment:

        Check segment for an explicit time signature setting.

        If none, check score settings for current time signature setting.

        Halt interpretation if no time signature setting is found.

        Otherwise store time signature setting.
        '''
        for segment_specification in self.score_specification.segment_specifications:
            settings = segment_specification.single_context_settings.get_settings(attribute='time_signatures')
            if settings:
                assert len(settings) == 1, repr(settings)
                setting = settings[0]
            else:
                settings = self.score_specification.single_context_settings_by_context.get_settings(
                    attribute='time_signatures')
                if not settings:
                    return
                assert len(settings) == 1, repr(settings)
                setting = settings[0]
                setting = setting.copy_setting_to_segment(segment_specification.segment_name)
            assert setting.selector.timespan == segment_specification.timespan, [
                repr(setting), '\n', repr(segment_specification.timespan)]
            self.store_single_context_setting_by_context(setting, clear_persistent_first=True)

    def supply_missing_region_division_commands(self, region_division_commands, voice):
        from experimental import interpretertools
        #self._debug_values(region_division_commands, 'rdc')
        if not region_division_commands:
            return region_division_commands
        first_start_offset_in_score = \
            self.score_specification.segment_name_and_segment_offset_to_score_offset(
            region_division_commands[0].start_segment_identifier,
            region_division_commands[0].segment_start_offset)
        if not first_start_offset_in_score == self.score_specification.start_offset:
            region_division_command = self.make_time_signature_division_command(
                voice, self.score_specification.start_offset, first_start_offset_in_score)
            region_division_commands.insert(0, region_division_command)
        last_stop_offset_in_score = \
            self.score_specification.segment_name_and_segment_offset_to_score_offset(
            region_division_commands[-1].start_segment_identifier,
            region_division_commands[-1].segment_stop_offset)
        if not last_stop_offset_in_score == self.score_specification.stop_offset:
            region_division_command = self.make_time_signature_division_command(
                voice, last_stop_offset_in_score, self.score_specification.stop_offset)
            region_division_commands.append(region_division_command)
        if len(region_division_commands) == 1:
            return region_division_commands
        #self._debug_values(region_division_commands, 'midway rdc')
        result = []
        for left_region_division_command, right_region_division_command in \
            sequencetools.iterate_sequence_pairwise_strict(region_division_commands):
            left_stop_offset_in_score = \
                self.score_specification.segment_name_and_segment_offset_to_score_offset(
                left_region_division_command.start_segment_identifier,
                left_region_division_command.segment_stop_offset)
            right_start_offset_in_score = \
                self.score_specification.segment_name_and_segment_offset_to_score_offset(
                right_region_division_command.start_segment_identifier,
                right_region_division_command.segment_start_offset)
            #self._debug((left_stop_offset_in_score, right_start_offset_in_score), 'offsets')
            assert left_stop_offset_in_score <= right_start_offset_in_score
            result.append(left_region_division_command)
            if left_stop_offset_in_score < right_start_offset_in_score:
                region_division_command = self.make_time_signature_division_command(
                    voice, left_stop_offset_in_score, right_start_offset_in_score)
                result.append(region_division_command)
        result.append(right_region_division_command)
        #self._debug_values(result, 'result')
        return result

    def time_signature_material_request_to_time_signatures(self, material_request):
        assert isinstance(material_request, requesttools.MaterialRequest), repr(material_request)
        assert material_request.attribute == 'time_signatures'
        segment_specification = self.get_start_segment_specification(material_request.start_segment_identifier)
        context_proxy = segment_specification.single_context_settings_by_context[material_request.context_name]
        single_context_setting = context_proxy.get_setting(attribute=material_request.attribute)
        absolute_request = single_context_setting.request
        assert isinstance(absolute_request, requesttools.AbsoluteRequest)
        time_signatures = requesttools.apply_request_transforms(material_request, absolute_request.payload)
        return time_signatures

    def uninterpreted_division_commands_to_region_division_commands(self, uninterpreted_division_commands):
        from experimental import interpretertools
        region_division_commands = []
        if not uninterpreted_division_commands:
            return []
        if any([x.request is None for x in uninterpreted_division_commands]):
            return []
        assert uninterpreted_division_commands[0].fresh, repr(uninterpreted_division_commands[0])
        for uninterpreted_division_command in uninterpreted_division_commands:
            #self._debug(uninterpreted_division_command, 'udc')
            if uninterpreted_division_command.fresh or uninterpreted_division_command.truncate:
                region_division_command = copy.deepcopy(uninterpreted_division_command)
                region_division_commands.append(region_division_command)
            else:
                last_region_division_command = region_division_commands[-1]
                if uninterpreted_division_command.request != \
                    last_region_division_command.request:
                    region_division_command = copy.deepcopy(uninterpreted_division_command)
                    region_division_commands.append(region_division_command)
                elif last_region_division_command.truncate:
                    region_division_command = copy.deepcopy(uninterpreted_division_command)
                    region_division_commands.append(region_division_command)
                else:
                    duration = last_region_division_command.duration + uninterpreted_division_command.duration
                    segment_start_offset = last_region_division_command.segment_start_offset
                    segment_stop_offset = last_region_division_command.segment_stop_offset + \
                        uninterpreted_division_command.duration
                    region_division_command = interpretertools.DivisionCommand(
                        last_region_division_command.request,
                        last_region_division_command.start_segment_identifier,
                        uninterpreted_division_command.context_name,
                        segment_start_offset,
                        segment_stop_offset,
                        duration,
                        index=last_region_division_command.index,
                        count=last_region_division_command.count,
                        reverse=last_region_division_command.reverse,
                        rotation=last_region_division_command.rotation,
                        callback=last_region_division_command.callback,
                        fresh=last_region_division_command.fresh,
                        truncate=uninterpreted_division_command.truncate
                        )
                    region_division_commands[-1] = region_division_command
        #self._debug(region_division_commands)
        return region_division_commands

    def voice_name_to_divisions(self, voice_name):
        voice = componenttools.get_first_component_in_expr_with_name(self.score, voice_name)
        assert isinstance(voice, voicetools.Voice), voice
        division_region_division_lists = self.score_specification.contexts[voice.name][
            'division_region_division_lists']
        divisions = []
        for division_region_division_list in division_region_division_lists:
            divisions.extend(division_region_division_list)
        assert isinstance(divisions, list), divisions
        divisions = [mathtools.NonreducedFraction(x) for x in divisions]
        return divisions
