import copy
from abjad.tools import *
from experimental import divisiontools
from experimental import helpertools
from experimental import library
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timetools
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

            * interpret all time signatures scorewide
            * interpret all divisions scorewide
            * interpret all rhythms scorewide
            * interpret all pitch-classes scorewide
            * interpret all registration scorewide
            * interpret all additional parameters scorewide

        Return Abjad score object.
        '''
        Interpreter.__call__(self, score_specification)
        self.interpret_time_signatures()
        self.interpret_divisions()
        self.interpret_rhythm()
        self.interpret_pitch_classes()
        self.interpret_registration()
        self.interpret_additional_parameters()
        return self.score

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def attribute_to_command_klass(self, attribute):
        if attribute == 'divisions':
            return settingtools.DivisionCommand
        elif attribute == 'rhythm':
            return settingtools.RhythmCommand
        else:
            raise NotImplementedError(attribute)

    def attribute_to_default_request(self, segment_specification, attribute):
        from experimental import requesttools
        if attribute == 'divisions':
            return requesttools.AbsoluteRequest(segment_specification.time_signatures)
        elif attribute == 'rhythm':
            return requesttools.AbsoluteRequest(library.skip_filled_tokens) 
        else:
            raise NotImplementedError(attribute)

    def calculate_score_and_segment_durations(self):
        '''Set ``'segment_durations'`` property on score specification.

        Set ``'score_duration'`` property on score specification.

        Set ``'start_offset'`` to ``Offset(0)`` on score specification.

        Set ``'stop_offset'`` on score specification.

        Set ``'segment_offset_pairs'`` property on score specification.
        '''
        segment_durations = [x.duration for x in self.score_specification.segment_specifications]
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
            durations = [x.prolated_duration for x in rhythm_containers]
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

    def division_command_request_to_divisions(self, division_command_request, voice_name):
        assert isinstance(division_command_request, requesttools.CommandRequest)
        assert division_command_request.attribute == 'divisions'
        #self._debug(division_command_request, 'dcr')
        requested_segment_identifier = division_command_request.timepoint.start_segment_identifier
        requested_offset = division_command_request.timepoint.get_score_offset(
            self.score_specification, voice_name)
        timespan_inventory = timetools.TimespanInventory()
        #self._debug_values(self.score_specification.all_division_region_commands, 'all div region commands')
        for division_region_command in self.score_specification.all_division_region_commands:
            if not division_region_command.request == division_command_request:
                timespan_inventory.append(division_region_command)
        #self._debug_values(timespan_inventory, 'timespan inventory')
        timespan_inequality = timetools.timepoint_happens_during_timespan(
            timepoint=requested_offset)
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
        selector = division_material_request.selector
        voice_name = division_material_request.voice_name
        start_offset = selector.get_score_start_offset(self.score_specification, voice_name)
        stop_offset = selector.get_score_stop_offset(self.score_specification, voice_name)
        #self._debug((voice_name, start_offset, stop_offset), 'request parameters')
        division_region_expressions = \
            self.score_specification.contexts[voice_name]['division_region_expressions']
        #self._debug(division_region_expressions, 'drx')
        source_timespan = durationtools.TimespanConstant(start_offset, stop_offset)
        timespan_inequality = timetools.timespan_2_intersects_timespan_1(
            timespan_1=source_timespan)
        division_region_expressions = division_region_expressions.get_timespans_that_satisfy_inequality(
            timespan_inequality)
        division_region_expressions = timetools.TimespanInventory(division_region_expressions)
        #self._debug(division_region_expressions, 'drx')
        if not division_region_expressions:
            return
        if not division_region_expressions.all_are_contiguous:
            return
        trimmed_division_region_expressions = copy.deepcopy(division_region_expressions)
        trimmed_division_region_expressions = timetools.TimespanInventory(trimmed_division_region_expressions)
        keep_timespan = durationtools.TimespanConstant(start_offset, stop_offset)
        trimmed_division_region_expressions.keep_material_that_intersects_timespan(keep_timespan)
        divisions = []
        for division_region_expression in trimmed_division_region_expressions:
            divisions.extend(division_region_expression.divisions)
        #self._debug(divisions, 'divisions')
        divisions = requesttools.apply_request_transforms(division_material_request, divisions)
        return divisions

    def division_region_command_to_division_region_expression(self, division_region_command, voice_name):
        if isinstance(division_region_command.request, list):
            divisions = division_region_command.request
            divisions = [divisiontools.Division(x) for x in divisions]
            region_duration = division_region_command.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
        elif isinstance(division_region_command.request, requesttools.AbsoluteRequest):
            request = division_region_command.request
            divisions = requesttools.apply_request_transforms(request, request.payload)
            divisions = requesttools.apply_request_transforms(division_region_command, divisions) 
            divisions = [divisiontools.Division(x) for x in divisions]
            region_duration = division_region_command.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
        elif isinstance(division_region_command.request, requesttools.CommandRequest):
            assert division_region_command.request.attribute == 'divisions'
            division_command_request = division_region_command.request
            divisions = self.division_command_request_to_divisions(
                division_command_request, voice_name)
            divisions = requesttools.apply_request_transforms(division_command_request, divisions)
            divisions = requesttools.apply_request_transforms(division_region_command, divisions) 
            division_region_command._request = divisions
            division_region_expression = self.division_region_command_to_division_region_expression(
                division_region_command, voice_name)
            return division_region_expression
        elif isinstance(division_region_command.request, requesttools.MaterialRequest):
            assert division_region_command.request.attribute == 'divisions'
            division_material_request = division_region_command.request
            divisions = self.division_material_request_to_divisions(division_material_request)
            if divisions is None:
                return
            divisions = requesttools.apply_request_transforms(division_region_command, divisions)
            division_region_command._request = divisions
            division_region_expression = self.division_region_command_to_division_region_expression(
                division_region_command, voice_name)
            return division_region_expression
        else:
            raise TypeError(division_region_command.request)
        return settingtools.OffsetPositionedDivisionList(
            divisions, 
            voice_name=voice_name, 
            start_offset=division_region_command.start_offset,
            stop_offset=division_region_command.stop_offset
            )

    def dump_rhythm_region_expressions_into_voices(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            for rhythm_region_expression in \
                self.score_specification.contexts[voice.name]['rhythm_region_expressions']:
                voice.extend(rhythm_region_expression.music)

    def filter_rhythm_quadruples(self, rhythm_quadruples):
        result = []
        for rhythm_quadruple in rhythm_quadruples:
            rhythm_command, division_list, start_offset, stop_offset = rhythm_quadruple
            start_offset = durationtools.Offset(start_offset)
            stop_offset = durationtools.Offset(stop_offset)
            if isinstance(rhythm_command.request, requesttools.AbsoluteRequest):
                result.append((rhythm_command.request.payload, division_list, start_offset, rhythm_command))
            elif isinstance(rhythm_command.request, requesttools.CommandRequest):
                rhythm_maker = self.rhythm_command_request_to_rhythm_maker(
                    rhythm_command.request, rhythm_command.request.context_name)
                result.append((rhythm_maker, division_list, start_offset, rhythm_command))
            elif isinstance(rhythm_command.request, requesttools.RhythmRequest):
                # maybe smarter to do all of these comparisons on command rather than request
                if not result:
                    result.append((rhythm_command.request, start_offset, stop_offset, rhythm_command))
                elif not isinstance(result[-1][0], requesttools.RhythmRequest):
                    result.append((rhythm_command.request, start_offset, stop_offset, rhythm_command))
                elif rhythm_command.request != result[-1][0]:
                    result.append((rhythm_command.request, start_offset, stop_offset, rhythm_command))
                else:
                    last_start_offset = result.pop()[1]
                    result.append((rhythm_command.request, last_start_offset, stop_offset, rhythm_command))
            else:
                raise TypeError(rhythm_command.request)
        return result

    def fuse_like_commands(self, commands):
        if any([x.request is None for x in commands]) or not commands:
            return []
        assert commands[0].fresh, repr(commands[0])
        result = [copy.deepcopy(commands[0])]
        for command in commands[1:]:
            if result[-1].can_fuse(command):
                result[-1] = result[-1].fuse(command)
            else:
                result.append(copy.deepcopy(command))
        return result

    def get_commands_that_start_during_segment(self, segment_specification, context_name, attribute):
        single_context_settings = self.get_single_context_settings_that_start_during_segment(
            segment_specification, context_name, attribute, include_improper_parentage=True)
        #self._debug_values(single_context_settings, 'scs')
        commands = []
        for single_context_setting in single_context_settings:
            command = self.single_context_setting_to_command(
                single_context_setting, segment_specification, context_name)
            commands.append(command)
        return commands

    # TODO: eventually merge with self.get_rhythm_commands_for_voice()
    def get_division_commands_for_voice(self, voice):
        division_commands = []
        for segment_specification in self.score_specification.segment_specifications:
            raw_commands = self.get_commands_that_start_during_segment(
                segment_specification, voice.name, 'divisions')
            cooked_commands = self.sort_and_split_raw_commands(raw_commands)
            if cooked_commands:
                division_commands.extend(cooked_commands)
            elif segment_specification.time_signatures:
                command = self.make_default_command_for_segment_specification(
                    segment_specification, 'divisions')
                division_commands.append(command)
        return division_commands

    def get_rhythm_commands_for_score(self):
        score_rhythm_commands = []
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_rhythm_commands = self.get_rhythm_commands_for_voice(voice)
            score_rhythm_commands.extend(voice_rhythm_commands)
        return score_rhythm_commands

    # TODO: eventually merge with self.get_division_commands_for_voice()
    def get_rhythm_commands_for_voice(self, voice):
        rhythm_commands = []
        for segment_specification in self.score_specification.segment_specifications:
            raw_commands = self.get_commands_that_start_during_segment(
                segment_specification, voice.name, 'rhythm')
            default_command = self.make_default_command_for_segment_specification(
                segment_specification, 'rhythm')
            raw_commands.insert(0, default_command)
            cooked_commands = self.sort_and_split_raw_commands(raw_commands)
            rhythm_commands.extend(cooked_commands)
        return rhythm_commands

    def get_single_context_settings_that_start_during_segment(
        self, segment_specification, context_name, attribute, 
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

    def get_start_segment_specification(self, expr):
        return self.score_specification.get_start_segment_specification(expr)

    def get_time_signature_slice(self, start_offset, stop_offset):
        time_signatures = self.score_specification.time_signatures
        assert time_signatures
        slice_duration = stop_offset - start_offset
        weights = [start_offset, slice_duration]
        shards = sequencetools.split_sequence_by_weights(
            time_signatures, weights, cyclic=False, overhang=False)
        result = shards[1]
        result = [x.pair for x in result]
        return result

    def initialize_region_expression_inventories_for_attribute(self, attribute):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            timespan_inventory = timetools.TimespanInventory()
            region_commands = '{}_region_commands'.format(attribute)
            self.score_specification.contexts[voice.name][region_commands] = timespan_inventory
            timespan_inventory = timetools.TimespanInventory()
            region_expressions = '{}_region_expressions'.format(attribute)
            self.score_specification.contexts[voice.name][region_expressions] = timespan_inventory

    def interpret_additional_parameters(self):
        pass

    def interpret_divisions(self):
        self.initialize_region_expression_inventories_for_attribute('division')
        self.populate_all_region_commands_for_attribute('divisions')
        self.make_division_region_expressions()
        self.make_voice_division_lists()

    def interpret_pitch_classes(self):
        pass

    def interpret_registration(self):
        pass

    def interpret_rhythm(self):
        self.initialize_region_expression_inventories_for_attribute('rhythm')
        self.populate_all_region_commands_for_attribute('rhythm')
        #self._debug_values(self.score_specification.all_rhythm_region_commands, 'region commands')
        self.populate_all_rhythm_quintuples()
        #self._debug_values(self.score_specification.all_rhythm_quintuples, 'quintuples')
        self.make_rhythm_region_expressions()
        self.dump_rhythm_region_expressions_into_voices()

    def interpret_time_signatures(self):
        self.populate_all_time_signature_commands()
        self.make_time_signatures()
        self.calculate_score_and_segment_durations()

    def make_default_command_for_segment_specification(self, segment_specification, attribute):
        request = self.attribute_to_default_request(segment_specification, attribute)
        start_offset, stop_offset = self.score_specification.segment_identifier_expression_to_offsets(
            segment_specification.segment_name)
        command_klass = self.attribute_to_command_klass(attribute)
        command = command_klass(
            request, 
            self.score_specification.score_name,
            start_offset,
            stop_offset,
            fresh=True
            )
        if attribute == 'divisions':
            command._truncate = False
        return command

    def make_division_region_expressions(self):
        redo = True
        while redo:
            redo = False
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                division_region_commands = \
                    self.score_specification.contexts[voice.name]['division_region_commands']
                division_region_commands_to_reattempt = []
                for division_region_command in division_region_commands:
                    #self._debug(division_region_command, 'drc')
                    division_region_expression = self.division_region_command_to_division_region_expression(
                        division_region_command, voice.name)
                    if division_region_expression is not None:
                        self.score_specification.contexts[voice.name]['division_region_expressions'].append(
                            division_region_expression)
                    else:
                        division_region_commands_to_reattempt.append(division_region_command)
                        redo = True
                self.score_specification.contexts[voice.name]['division_region_commands'] = \
                    division_region_commands_to_reattempt[:]
                # sort may have to happen as each expression adds in, above
                self.score_specification.contexts[voice.name]['division_region_expressions'].sort()

    def make_rhythm_quintuples_for_voice(self, voice, voice_division_list):
        rhythm_commands = self.score_specification.contexts[voice.name]['rhythm_region_commands']
        rhythm_command_durations = [x.duration for x in rhythm_commands]
        #self._debug(rhythm_command_durations, 'rcd')
        division_region_expressions = \
            self.score_specification.contexts[voice.name]['division_region_expressions']
        #self._debug_values(division_region_expressions, 'drx')
        division_region_durations = [x.duration for x in division_region_expressions]
        #self._debug(division_region_durations, 'drd')
        rhythm_command_merged_durations = sequencetools.merge_duration_sequences(
            division_region_durations, rhythm_command_durations)
        #self._debug(rhythm_command_merged_durations, 'rcmds')
        # assert that rhythm commands cover rhythm regions exactly
        assert sequencetools.partition_sequence_by_weights_exactly(
            rhythm_command_merged_durations, rhythm_command_durations)
        rhythm_region_start_division_duration_lists = \
                sequencetools.partition_sequence_by_backgrounded_weights(
                voice_division_list.divisions, rhythm_command_merged_durations)
        #self._debug_values(rhythm_region_start_division_duration_lists, 'rrsddls')
        assert len(rhythm_region_start_division_duration_lists) == len(rhythm_command_merged_durations)
        rhythm_region_start_division_counts = [len(l) for l in rhythm_region_start_division_duration_lists]
        rhythm_region_division_lists = sequencetools.partition_sequence_by_counts(
            voice_division_list.divisions, rhythm_region_start_division_counts, cyclic=False, overhang=False)
        rhythm_region_division_lists = [
            divisiontools.DivisionList(x, voice_name=voice.name) for x in rhythm_region_division_lists]
        assert len(rhythm_region_division_lists) == len(rhythm_command_merged_durations)
        #self._debug_values(rhythm_region_division_lists, 'rrdls')
        rhythm_region_durations = [x.duration for x in rhythm_region_division_lists]
        #self._debug(rhythm_region_durations, 'rrds')
        cumulative_sums = mathtools.cumulative_sums_zero(rhythm_region_durations)
        rhythm_region_start_offsets = cumulative_sums[:-1]
        rhythm_region_stop_offsets = cumulative_sums[1:]
        rhythm_command_duration_pairs = [(x, x.duration) for x in rhythm_commands]
        #self._debug_values(rhythm_command_duration_pairs, 'rhythm command / duration pairs')
        merged_duration_rhythm_command_pairs = \
            sequencetools.pair_duration_sequence_elements_with_input_pair_values(
            rhythm_command_merged_durations, rhythm_command_duration_pairs)
        # the first column in pairs is not used for anything further at all is discarded
        rhythm_commands = [x[-1] for x in merged_duration_rhythm_command_pairs]
        #self._debug_values(rhythm_commands, 'rhythm commands')
        assert len(rhythm_commands) == len(rhythm_region_division_lists)
        rhythm_quadruples = zip(rhythm_commands, rhythm_region_division_lists, 
            rhythm_region_start_offsets, rhythm_region_stop_offsets)
        #self._debug_values(rhythm_quadruples, 'rhythm quadruples')
        rhythm_quadruples = self.filter_rhythm_quadruples(rhythm_quadruples)
        #self._debug_values(rhythm_quadruples, 'rhythm quadruples')
        rhythm_quadruples = self.reestablish_rhythm_material_request_offsets(rhythm_quadruples)
        #self._debug_values(rhythm_quadruples, 'rhythm quadruples')
        rhythm_quintuples = [(voice.name,) + x for x in rhythm_quadruples]
        return rhythm_quintuples

    def make_rhythm_region_expression(
        self, rhythm_maker, rhythm_region_division_list, start_offset, rhythm_command):
        if rhythm_region_division_list:
            rhythm_maker = requesttools.apply_request_transforms(rhythm_command, rhythm_maker)
            leaf_lists = rhythm_maker(rhythm_region_division_list.pairs)
            rhythm_containers = [containertools.Container(x) for x in leaf_lists]
            rhythm_region_expression = settingtools.OffsetPositionedRhythmExpression(
                rhythm_containers, 
                voice_name=rhythm_region_division_list.voice_name, start_offset=start_offset)
            self.conditionally_beam_rhythm_containers(rhythm_maker, rhythm_containers)
            return rhythm_region_expression

    def make_rhythm_region_expressions(self):
        while self.score_specification.all_rhythm_quintuples:
            #self._debug(len(self.score_specification.all_rhythm_quintuples), 'len')
            for rhythm_quintuple in self.score_specification.all_rhythm_quintuples[:]:
                voice_name = rhythm_quintuple[0]
                rhythm_quadruple = rhythm_quintuple[1:]
                if isinstance(rhythm_quadruple[0], timetokentools.TimeTokenMaker):
                    rhythm_region_expression = self.make_rhythm_region_expression(*rhythm_quadruple)
                elif isinstance(rhythm_quadruple[0], requesttools.RhythmRequest):
                    rhythm_region_expression = self.rhythm_request_to_rhythm_region_expression(
                        *rhythm_quadruple)
                else:
                    raise TypeError(rhythm_quadruple[0])
                if rhythm_region_expression is not None:
                    self.score_specification.all_rhythm_quintuples.remove(rhythm_quintuple)
                    start_offset, stop_offset = rhythm_region_expression.offsets
                    self.score_specification.contexts[voice_name][
                        'rhythm_region_expressions'].delete_material_that_intersects_timespan(
                            rhythm_region_expression)
                    self.score_specification.contexts[voice_name]['rhythm_region_expressions'].append(
                        rhythm_region_expression)
                    self.score_specification.contexts[voice_name]['rhythm_region_expressions'].sort()

    def make_time_signature_division_command(self, voice, start_offset, stop_offset):
        divisions = self.get_time_signature_slice(start_offset, stop_offset)
        segment_identifier = self.score_specification.score_offset_to_segment_identifier(start_offset)
        division_command = settingtools.DivisionCommand(
            requesttools.AbsoluteRequest(divisions),
            voice.name, 
            start_offset,
            stop_offset,
            fresh=True,
            truncate=True
            )
        return division_command

    def make_time_signatures(self):
        while self.score_specification.all_time_signature_commands:
            for time_signature_setting in self.score_specification.all_time_signature_commands:
                self.make_time_signatures_for_time_signature_setting(time_signature_setting)
        time_signatures = self.score_specification.time_signatures
        measures = measuretools.make_measures_with_full_measure_spacer_skips(time_signatures)
        context = componenttools.get_first_component_in_expr_with_name(self.score, 'TimeSignatureContext')
        context.extend(measures)

    def make_time_signatures_for_time_signature_setting(self, time_signature_setting):
        if isinstance(time_signature_setting.request, requesttools.AbsoluteRequest):
            time_signatures = time_signature_setting.request.payload
            time_signatures = requesttools.apply_request_transforms(
                time_signature_setting.request, time_signatures)
        elif isinstance(time_signature_setting.request, requesttools.CommandRequest):
            time_signatures = self.time_signature_command_request_to_time_signatures(
                time_signature_setting.request)
        elif isinstance(time_signature_setting.request, requesttools.MaterialRequest):
            time_signatures = self.time_signature_material_request_to_time_signatures(
                time_signature_setting.request)
        else:
            raise TypeError(time_signature_setting.request)
        if time_signatures:
            time_signatures = requesttools.apply_request_transforms(time_signature_setting, time_signatures)
            segment_specification = self.get_start_segment_specification(time_signature_setting.selector)
            segment_specification._time_signatures = time_signatures[:]
            self.score_specification.all_time_signature_commands.remove(time_signature_setting)

    def make_voice_division_lists(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_division_list = divisiontools.DivisionList([], voice.name)
            expressions = self.score_specification.contexts[voice.name]['division_region_expressions']
            divisions = [expression.divisions for expression in expressions]
            divisions = sequencetools.flatten_sequence(divisions, depth=1)
            start_offset = durationtools.Offset(0)
            for division in divisions:
                offset_positioned_division = copy.deepcopy(division)
                offset_positioned_division._start_offset = durationtools.Offset(start_offset)
                start_offset += division.duration
                voice_division_list.divisions.append(offset_positioned_division)
            self.score_specification.contexts[voice.name]['voice_division_list'] = voice_division_list

    def populate_all_rhythm_quintuples(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_division_list = self.score_specification.contexts[voice.name]['voice_division_list']
            if voice_division_list:
                rhythm_quintuples = self.make_rhythm_quintuples_for_voice(voice, voice_division_list)
                self.score_specification.all_rhythm_quintuples.extend(rhythm_quintuples)

    def populate_all_region_commands_for_attribute(self, attribute):
        if self.score_specification.segment_specifications:
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                if attribute == 'divisions':
                    region_commands = self.get_division_commands_for_voice(voice)
                elif attribute == 'rhythm':
                    region_commands = self.get_rhythm_commands_for_voice(voice)
#                elif attribute == 'time_signatures':
#                    region_commands = \
#                        segment_specification.single_context_settings_by_context.score_context_proxy.get_settings(
#                        attribute='time_signatures')
#                    region_commands = region_commands[-1:]
                else:
                    raise ValueError(attribute)
                region_commands = self.fuse_like_commands(region_commands)
                region_commands = self.supply_missing_region_commands_for_attribute(
                    region_commands, voice, attribute)
                singular_attribute = attribute.rstrip('s')
                key = '{}_region_commands'.format(singular_attribute)
                self.score_specification.contexts[voice.name][key][:] = region_commands[:]
                all_region_commands = getattr(self.score_specification, 'all_' + key)
                for region_command in region_commands:
                    if region_command not in all_region_commands:
                        all_region_commands.append(region_command)

    # TODO: eventually merge with self.populate_all_region_commands_for_attribute()
    def populate_all_time_signature_commands(self):
        for segment_specification in self.score_specification.segment_specifications:
            time_signature_settings = \
                segment_specification.single_context_settings_by_context.score_context_proxy.get_settings(
                attribute='time_signatures')
            if not time_signature_settings:
                continue
            time_signature_setting = time_signature_settings[-1]
            self.score_specification.all_time_signature_commands.append(time_signature_setting)

    def reestablish_rhythm_material_request_offsets(self, rhythm_quadruples):
        result = []
        for rhythm_quadruple in rhythm_quadruples:
            if isinstance(rhythm_quadruple[0], requesttools.RhythmRequest):
                rhythm_command = rhythm_quadruple[-1]
                assert isinstance(rhythm_command, settingtools.RhythmCommand)
                start_offset = rhythm_command.start_offset
                stop_offset = rhythm_command.stop_offset
                result.append((rhythm_quadruple[0], start_offset, stop_offset, rhythm_command))
            else:
                result.append(rhythm_quadruple)
        return result

    def rhythm_command_request_to_rhythm_maker(self, rhythm_command_request, voice_name):
        assert isinstance(rhythm_command_request, requesttools.CommandRequest)
        assert rhythm_command_request.attribute == 'rhythm'
        #self._debug(rhythm_command_request, 'rcr')
        requested_segment_identifier = rhythm_command_request.timepoint.start_segment_identifier
        #self._debug(requested_segment_identifier, 'segment')
        requested_offset = rhythm_command_request.timepoint.get_score_offset(
            self.score_specification, voice_name)
        #self._debug(requested_offset, 'offset')
        timespan_inventory = timetools.TimespanInventory()
        for rhythm_region_command in self.score_specification.all_rhythm_region_commands:
            #if rhythm_region_command.start_segment_identifier == requested_segment_identifier:
            if True:
                if not rhythm_region_command.request == rhythm_command_request:
                    timespan_inventory.append(rhythm_region_command)
        timespan_inequality = timetools.timepoint_happens_during_timespan(
            timepoint=requested_offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_inequality(timespan_inequality)
        #self._debug_values(candidate_commands, 'candidates')
        segment_specification = self.get_start_segment_specification(requested_segment_identifier)
        source_command = self.select_first_element_in_expr_by_parentage(
            candidate_commands, segment_specification, rhythm_command_request.context_name, 
            include_improper_parentage=True)
        assert source_command is not None
        #self._debug(source_command, 'source_command')
        absolute_request = source_command.request
        assert isinstance(source_command.request, requesttools.AbsoluteRequest)
        assert isinstance(source_command.request.payload, timetokentools.TimeTokenMaker)
        rhythm_maker = copy.deepcopy(source_command.request.payload)
        rhythm_maker = requesttools.apply_request_transforms(rhythm_command_request, rhythm_maker)
        return rhythm_maker

    def rhythm_request_to_rhythm_region_expression(
        self, rhythm_request, start_offset, stop_offset, rhythm_command):
        assert isinstance(rhythm_request, requesttools.RhythmRequest)
        #self._debug(rhythm_request, 'rhythm request')
        #self._debug((start_offset, stop_offset), 'offsets')
        voice_name = rhythm_request.context_name
        source_score_offsets = rhythm_request.selector.get_score_offsets(
            self.score_specification, rhythm_request.context_name)
        source_timespan = durationtools.TimespanConstant(*source_score_offsets)
        #self._debug(source_timespan, 'source timespan')
        rhythm_region_expressions = \
            self.score_specification.contexts[voice_name]['rhythm_region_expressions']
        #self._debug_values(rhythm_region_expressions, 'rhythm region expressions')
        timespan_inequality = timetools.timespan_2_intersects_timespan_1(
            timespan_1=source_timespan)
        rhythm_region_expressions = rhythm_region_expressions.get_timespans_that_satisfy_inequality(
            timespan_inequality)
        if not rhythm_region_expressions:
            return
        rhythm_region_expressions = copy.deepcopy(rhythm_region_expressions)
        rhythm_region_expressions = timetools.TimespanInventory(rhythm_region_expressions)
        rhythm_region_expressions.sort()
        rhythm_region_expressions.keep_material_that_intersects_timespan(source_timespan)
        result = settingtools.OffsetPositionedRhythmExpression(
            voice_name=voice_name, start_offset=start_offset)
        #self._debug(result, 'result')
        for rhythm_region_expression in rhythm_region_expressions:
            result.music.extend(rhythm_region_expression.music)
        #self._debug(result, 'result')
        assert componenttools.is_well_formed_component(result.music)
        result.adjust_to_offsets(start_offset=start_offset, stop_offset=stop_offset)
        # TODO: encapsulate all of the following in a single call
        if rhythm_request.reverse:
            result.reverse()
        if rhythm_request.rotation:
            result.rotate(rhythm_request.rotation)    
        if rhythm_command.reverse:
            result.reverse()
        if rhythm_command.rotation:
            result.rotate(rhythm_command.rotation)
        result.repeat_to_stop_offset(stop_offset)
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

    # do we eventually need to do this with time signature settings, too?
    def single_context_setting_to_command(self, single_context_setting, segment_specification, voice_name):
        assert single_context_setting.selector.start_segment_identifier == segment_specification.segment_name
        start_offset, stop_offset = single_context_setting.selector.get_score_offsets(
            self.score_specification, voice_name)
        command_klass = self.attribute_to_command_klass(single_context_setting.attribute)
        command = command_klass(
            single_context_setting.request, 
            single_context_setting.context_name,
            start_offset,
            stop_offset,
            index=single_context_setting.index,
            count=single_context_setting.count,
            reverse=single_context_setting.reverse,
            rotation=single_context_setting.rotation,
            callback=single_context_setting.callback,
            fresh=single_context_setting.fresh
            )
        if single_context_setting.attribute == 'divisions':
            command._truncate = single_context_setting.truncate
        return command

    def sort_and_split_raw_commands(self, raw_commands):
        #self._debug_values(raw_commands, 'raw')
        cooked_commands = []
        for raw_command in raw_commands:
            command_was_delayed, command_was_split = False, False
            commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split = [], [], [], []
            for cooked_command in cooked_commands:
                if timetools.timespan_2_contains_timespan_1_improperly(
                    cooked_command, raw_command):
                    commands_to_remove.append(cooked_command)
                elif timetools.timespan_2_delays_timespan_1(cooked_command, raw_command):
                    commands_to_delay.append(cooked_command)
                elif timetools.timespan_2_curtails_timespan_1(cooked_command, raw_command):
                    commands_to_curtail.append(cooked_command)
                elif timetools.timespan_2_trisects_timespan_1(cooked_command, raw_command):
                    commands_to_split.append(cooked_command)
            #print commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split
            for command_to_remove in commands_to_remove:
                cooked_commands.remove(command_to_remove)
            for command_to_curtail in commands_to_curtail:
                command_to_curtail._stop_offset = raw_command.start_offset
            for command_to_delay in commands_to_delay:
                command_to_delay._start_offset = raw_command.stop_offset
                command_was_delayed = True
            for command_to_split in commands_to_split:
                left_command = command_to_split
                middle_command = raw_command
                right_command = copy.deepcopy(left_command)
                left_command._stop_offset = middle_command.start_offset
                right_command._start_offset = middle_command.stop_offset
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

    def store_interpreter_specific_single_context_settings_by_context(self):
        self.store_single_context_attribute_settings_by_context('time_signatures')
        self.store_single_context_attribute_settings_by_context('divisions')
        self.store_single_context_attribute_settings_by_context('rhythm')
        self.store_single_context_attribute_settings_by_context('pitch_classes')
        self.store_single_context_attribute_settings_by_context('registration')

    def store_single_context_attribute_settings_by_context(self, attribute):
        for segment_specification in self.score_specification.segment_specifications:
            new_settings = segment_specification.single_context_settings.get_settings(attribute=attribute)
            existing_settings = \
                self.score_specification.single_context_settings_by_context.get_settings(
                attribute=attribute)
            new_context_names = [x.context_name for x in new_settings]
            forwarded_existing_settings = []
            for existing_setting in existing_settings[:]:
                if existing_setting.context_name in new_context_names:
                    existing_settings.remove(existing_setting)
                else:
                    forwarded_existing_setting = existing_setting.copy_setting_to_segment(
                        segment_specification)
                    forwarded_existing_settings.append(forwarded_existing_setting)
            settings_to_store = new_settings + forwarded_existing_settings
            self.store_single_context_settings_by_context(settings_to_store, clear_persistent_first=True)

    def supply_missing_region_commands_for_attribute(self, region_commands, voice, attribute):
        if attribute == 'divisions':
            return self.supply_missing_division_commands(region_commands, voice)
        # does a rhythm version of this method need to be implemented eventually?
        else:
            return region_commands
        
    def supply_missing_division_commands(self, division_region_commands, voice):
        #self._debug_values(division_region_commands, 'rdcs')
        if not division_region_commands:
            return division_region_commands
        if not division_region_commands[0].start_offset == self.score_specification.start_offset:
            division_region_command = self.make_time_signature_division_command(
                voice, self.score_specification.start_offset, division_region_commands[0].start_offset)
            division_region_commands.insert(0, division_region_command)
        if not division_region_commands[-1].stop_offset == self.score_specification.stop_offset:
            division_region_command = self.make_time_signature_division_command(
                voice, division_region_commands[-1].stop_offset, self.score_specification.stop_offset)
            division_region_commands.append(division_region_command)
        if len(division_region_commands) == 1:
            return division_region_commands
        #self._debug_values(division_region_commands, 'rdcs')
        result = []
        for left_division_region_command, right_division_region_command in \
            sequencetools.iterate_sequence_pairwise_strict(division_region_commands):
            assert left_division_region_command.stop_offset <= right_division_region_command.start_offset
            result.append(left_division_region_command)
            if left_division_region_command.stop_offset < right_division_region_command.start_offset:
                division_region_command = self.make_time_signature_division_command(
                    voice, 
                    left_division_region_command.stop_offset, right_division_region_command.start_offset)
                result.append(division_region_command)
        result.append(right_division_region_command)
        #self._debug_values(result, 'result')
        return result

    def time_signature_command_request_to_time_signatures(self, command_request):
        assert isinstance(command_request, requesttools.CommandRequest)
        assert command_request.attribute == 'time_signatures'
        segment_specification = self.get_start_segment_specification(command_request.timepoint)
        time_signatures = segment_specification.time_signatures[:]
        time_signatures = requesttools.apply_request_transforms(command_request, time_signatures)
        return time_signatures

    def time_signature_material_request_to_time_signatures(self, material_request):
        assert isinstance(material_request, requesttools.MaterialRequest), repr(material_request)
        assert material_request.attribute == 'time_signatures'
        segment_specification = self.get_start_segment_specification(
            material_request.start_segment_identifier)
        context_proxy = segment_specification.single_context_settings_by_context[
            material_request.context_name]
        single_context_setting = context_proxy.get_setting(attribute=material_request.attribute)
        absolute_request = single_context_setting.request
        assert isinstance(absolute_request, requesttools.AbsoluteRequest)
        time_signatures = requesttools.apply_request_transforms(material_request, absolute_request.payload)
        return time_signatures
