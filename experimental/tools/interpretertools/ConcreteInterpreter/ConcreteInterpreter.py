import copy
from abjad.tools import *
from experimental.tools import divisiontools
from experimental.tools import helpertools
from experimental.tools import library
from experimental.tools import requesttools
from experimental.tools import selectortools
from experimental.tools import settingtools
from experimental.tools import specificationtools
from experimental.tools import timeexpressiontools
from experimental.tools.interpretertools.Interpreter import Interpreter


class ConcreteInterpreter(Interpreter):
    r'''

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

    def attribute_to_region_command_class(self, attribute):
        if attribute == 'divisions':
            return settingtools.DivisionRegionCommand
        elif attribute == 'rhythm':
            return settingtools.RhythmRegionCommand
        else:
            raise NotImplementedError(attribute)

    def calculate_score_and_segment_timespans(self):
        segment_durations = [durationtools.Duration(sum(x.time_signatures)) 
            for x in self.score_specification.segment_specifications]
        if sequencetools.all_are_numbers(segment_durations):
            score_duration = sum(segment_durations)
            score_start_offset = durationtools.Offset(0)
            score_stop_offset = durationtools.Offset(score_duration)
            self.score_specification._start_offset = durationtools.Offset(0)
            self.score_specification._stop_offset = durationtools.Offset(score_duration)
            score_timespan = timespantools.Timespan(score_start_offset, score_stop_offset)
            self.score_specification._timespan = score_timespan
            segment_offset_pairs = mathtools.cumulative_sums_zero_pairwise(segment_durations)
            segment_offset_pairs = [
                (durationtools.Offset(x[0]), durationtools.Offset(x[1])) for x in segment_offset_pairs]
            for segment_offset_pair, segment_specification in zip(
                segment_offset_pairs, self.score_specification.segment_specifications):
                start_offset, stop_offset = segment_offset_pair
                segment_specification._start_offset = start_offset
                segment_specification._stop_offset = stop_offset
                timespan = timespantools.Timespan(start_offset, stop_offset)
                segment_specification._timespan = timespan

    def clear_persistent_single_context_settings_by_context(self, context_name, attribute):
        if attribute in self.score_specification.single_context_settings_by_context[context_name]:
            del(self.score_specification.single_context_settings_by_context[context_name][attribute])

    def conditionally_beam_rhythm_containers(self, rhythm_maker, rhythm_containers):
        if getattr(rhythm_maker, 'beam_cells_together', False):
            spannertools.destroy_spanners_attached_to_components_in_expr(rhythm_containers)
            durations = [x.prolated_duration for x in rhythm_containers]
            beamtools.DuratedComplexBeamSpanner(rhythm_containers, durations=durations, span=1)
        elif getattr(rhythm_maker, 'beam_each_cell', False):
            spannertools.destroy_spanners_attached_to_components_in_expr(rhythm_containers)
            for rhythm_container in rhythm_containers:
                beamtools.DuratedComplexBeamSpanner(
                    [rhythm_container], [rhythm_container.prolated_duration], span=1)

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
        #self._debug(division_command_request, 'division command request')
        requested_segment_identifier = division_command_request.offset.start_segment_identifier
        requested_offset = division_command_request.offset._get_offset(self.score_specification, voice_name)
        timespan_inventory = timespantools.TimespanInventory()
        #self._debug_values(self.score_specification.all_division_region_commands, 'all div region commands')
        for division_region_command in self.score_specification.all_division_region_commands:
            if not division_region_command.request == division_command_request:
                timespan_inventory.append(division_region_command)
        #self._debug_values(timespan_inventory, 'timespan inventory')
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=requested_offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        #self._debug_values(candidate_commands, 'candidates')
        segment_specification = self.get_start_segment_specification(requested_segment_identifier)
        source_command = self.get_first_element_in_expr_by_parentage(
            candidate_commands, segment_specification, division_command_request.voice_name, 
            include_improper_parentage=True)
        assert source_command is not None
        #self._debug(source_command, 'source_command')
        absolute_request = source_command.request
        assert isinstance(absolute_request, requesttools.AbsoluteRequest), repr(absolute_request)
        divisions = absolute_request.payload
        return divisions

    def division_region_command_to_division_region_expressions(self, division_region_command, voice_name):
        if isinstance(division_region_command.request, list):
            divisions = division_region_command.request
            divisions = [divisiontools.Division(x) for x in divisions]
            region_duration = division_region_command.timespan.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
        elif isinstance(division_region_command.request, requesttools.AbsoluteRequest):
            request = division_region_command.request
            payload = request.payload
            # TODO: This is a hack; the payload for an absolute request 
            #       should always be some type of (literal) constant.
            #       So the branched call below should be unnecessary.
            divisions = self.timespan_expressions_to_durations(payload)
            divisions = [divisiontools.Division(x) for x in divisions]
            region_duration = division_region_command.timespan.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
        elif isinstance(division_region_command.request, requesttools.CommandRequest):
            assert division_region_command.request.attribute == 'divisions'
            division_command_request = division_region_command.request

            # TODO: migrate to DivisionCommandRequest.get_payload(score_specification, ...)
            divisions = self.division_command_request_to_divisions(division_command_request, voice_name)
            start_offset = division_region_command.timespan.start_offset
            divisions, start_offset = division_command_request._apply_request_modifiers(divisions, start_offset)

            divisions = requesttools.AbsoluteRequest(divisions)
            division_region_command = division_region_command.new(request=divisions)
            division_region_expressions = self.division_region_command_to_division_region_expressions(
                division_region_command, voice_name)
            return division_region_expressions
        elif isinstance(division_region_command.request, selectortools.BeatSelector):
            beat_selector = division_region_command.request
            start_offset, stop_offset = division_region_command.timespan.offsets
            timespan, divisions = beat_selector._get_timespan_and_selected_objects(
                self.score_specification, division_region_command.voice_name, start_offset, stop_offset)
            divisions = requesttools.AbsoluteRequest(divisions)
            division_region_command = division_region_command.new(request=divisions)
            division_region_expressions = self.division_region_command_to_division_region_expressions(
                division_region_command, voice_name)
            return division_region_expressions
        elif isinstance(division_region_command.request, selectortools.DivisionSelector):
            division_selector = division_region_command.request
            division_region_expression = division_selector._get_division_region_expression(
                self.score_specification, division_selector.voice_name)
            #self._debug(division_region_expression, 'drx')
            if division_region_expression is None:
                return
            divisions = division_region_expression.payload.divisions[:]
            region_duration = division_region_command.timespan.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
            divisions = [divisiontools.Division(x) for x in divisions]
            division_list = division_region_expression.division_list.new(divisions=divisions)
            division_region_expression = division_region_expression.new(division_list=division_list)
            #self._debug(division_region_expression, 'drx')
            # remove two lines after testing
            #addendum = division_region_command.timespan.start_offset - \
            #    division_region_expression.timespan.start_offset
            right = division_region_command.timespan.start_offset
            left = division_region_expression.timespan.start_offset
            addendum = right - left
            division_region_expression = division_region_expression.translate_offsets(
                start_offset_translation=addendum, stop_offset_translation=addendum)
            return [division_region_expression]
        elif isinstance(division_region_command.request, selectortools.BackgroundMeasureSelector):
            background_measure_selector = division_region_command.request
            timespan, time_signatures = \
                background_measure_selector._get_timespan_and_selected_objects(
                self.score_specification, None)
            divisions = [divisiontools.Division(x) for x in time_signatures]
        else:
            raise TypeError(division_region_command.request)
        return [
            settingtools.DivisionRegionProduct(
            divisions, 
            voice_name=voice_name, 
            timespan=division_region_command.timespan
            )]

    def dump_rhythm_region_expressions_into_voices(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            for rhythm_region_expression in \
                self.score_specification.contexts[voice.name]['rhythm_region_expressions']:
                voice.extend(rhythm_region_expression.payload)

    def filter_rhythm_quadruples(self, rhythm_quadruples):
        result = []
        for rhythm_quadruple in rhythm_quadruples:
            rhythm_command, division_list, start_offset, stop_offset = rhythm_quadruple
            if isinstance(rhythm_command.request, requesttools.AbsoluteRequest):
                result.append((rhythm_command.request.payload, division_list, start_offset, rhythm_command))
            elif isinstance(rhythm_command.request, requesttools.CommandRequest):
                rhythm_maker = self.rhythm_command_request_to_rhythm_maker(
                    rhythm_command.request, rhythm_command.request.voice_name)
                result.append((rhythm_maker, division_list, start_offset, rhythm_command))
            elif isinstance(rhythm_command.request, selectortools.CounttimeComponentSelector):
                if result and self.rhythm_command_prolongs_expr(rhythm_command, result[-1][0]):
                    last_start_offset = result.pop()[1]
                    new_entry = (rhythm_command,
                        last_start_offset,
                        stop_offset,
                        rhythm_command)
                else:
                    new_entry = (rhythm_command,
                            rhythm_command.timespan.start_offset, 
                            rhythm_command.timespan.stop_offset, 
                            rhythm_command)
                result.append(new_entry)
            else:
                raise TypeError(rhythm_command.request)
        # make one last pass over commands that bear a material request
        postprocessed_result = []
        for quadruple in result:
            if isinstance(quadruple[0], settingtools.RegionCommand):
                postprocessed_result.append((quadruple[0].request, ) + quadruple[1:])
            else:
                postprocessed_result.append(quadruple)
        return postprocessed_result

    def fuse_like_region_commands(self, region_commands):
        if any([x.request is None for x in region_commands]) or not region_commands:
            return []
        assert region_commands[0].fresh, repr(region_commands[0])
        result = [copy.deepcopy(region_commands[0])]
        for region_command in region_commands[1:]:
            if result[-1].can_fuse(region_command):
                result[-1] = result[-1].fuse(region_command)
            else:
                result.append(copy.deepcopy(region_command))
        return result

    def get_first_element_in_expr_by_parentage(self, expr, segment_specification, context_name, 
        include_improper_parentage=False):
        context_names = [context_name]
        if include_improper_parentage:
            context_names = self.context_name_to_parentage_names(
                segment_specification, context_name, proper=False)
        for context_name in context_names:
            for element in expr:
                if element.context_name is None:
                    return element
                if element.context_name == context_name:
                    return element

    def get_raw_commands_for_voice(self, context_name, attribute):
        commands = []
        for segment_specification in self.score_specification.segment_specifications:
            single_context_settings = self.get_single_context_settings_that_start_during_segment(
                segment_specification, context_name, attribute, include_improper_parentage=True)
            for single_context_setting in single_context_settings:
                command = self.single_context_setting_to_command(
                    single_context_setting, segment_specification, context_name)
                commands.append(command)
        return commands

    def get_region_commands_for_voice(self, voice_name, attribute):
        raw_commands = self.get_raw_commands_for_voice(voice_name, attribute)
        region_commands = self.sort_and_split_raw_commands(raw_commands)
        region_commands = self.fuse_like_region_commands(region_commands)
        region_commands = self.supply_missing_region_commands(region_commands, voice_name, attribute)
        return region_commands

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

    def initialize_region_expression_inventories(self, attribute):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            timespan_inventory = timespantools.TimespanInventory()
            region_commands = '{}_region_commands'.format(attribute)
            self.score_specification.contexts[voice.name][region_commands] = timespan_inventory
            timespan_inventory = timespantools.TimespanInventory()
            region_expressions = '{}_region_expressions'.format(attribute)
            self.score_specification.contexts[voice.name][region_expressions] = timespan_inventory

    def interpret_additional_parameters(self):
        pass

    def interpret_divisions(self):
        self.initialize_region_expression_inventories('division')
        self.populate_all_region_commands('divisions')
        self.make_division_region_expressions()
        self.make_voice_division_lists()

    def interpret_pitch_classes(self):
        pass

    def interpret_registration(self):
        pass

    def interpret_rhythm(self):
        self.initialize_region_expression_inventories('rhythm')
        self.populate_all_region_commands('rhythm')
        #self._debug_values(self.score_specification.all_rhythm_region_commands, 'all rhythm region commands')
        self.populate_all_rhythm_quintuples()
        #self._debug_values(self.score_specification.all_rhythm_quintuples, 'all rhythm quintuples')
        self.make_rhythm_region_expressions()
        self.dump_rhythm_region_expressions_into_voices()

    def interpret_time_signatures(self):
        self.populate_all_time_signature_commands()
        self.make_time_signatures()
        self.calculate_score_and_segment_timespans()

    def make_default_region_command(self, voice_name, start_offset, stop_offset, attribute):
        if attribute == 'divisions':
            return self.make_time_signature_division_command(voice_name, start_offset, stop_offset)
        elif attribute == 'rhythm':
            return self.make_skip_token_rhythm_command(voice_name, start_offset, stop_offset)
        else:
            raise ValueError(attribute)

    def make_division_region_expressions(self):
        redo = True
        previous_commands = None
        while redo:
            current_commands = {}
            redo = False
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                voice_division_region_commands = \
                    self.score_specification.contexts[voice.name]['division_region_commands']
                voice_division_region_expressions = \
                    self.score_specification.contexts[voice.name]['division_region_expressions']
                current_commands[voice] = voice_division_region_commands[:]
                voice_division_region_commands_to_reattempt = []
                for division_region_command in voice_division_region_commands:
                    division_region_expressions = self.division_region_command_to_division_region_expressions(
                        division_region_command, voice.name)
                    if division_region_expressions is not None:
                        assert isinstance(division_region_expressions, list)
                        voice_division_region_expressions.extend(division_region_expressions)
                    else:
                        voice_division_region_commands_to_reattempt.append(division_region_command)
                        redo = True
                voice_division_region_commands[:] = voice_division_region_commands_to_reattempt[:]
                # sort may have to happen as each expression adds in, above
                voice_division_region_expressions.sort()
            # check to see if we made absolutely no intepretive progress in this iteration through loop
            if current_commands == previous_commands:
                raise Exception('cyclic specification error.')
            else:
                previous_commands = current_commands

    def make_rhythm_quintuples_for_voice(self, voice, voice_division_list):
        #self._debug(voice, 'voice')
        #self._debug(voice_division_list, 'voice division list')
        rhythm_region_commands = self.score_specification.contexts[voice.name]['rhythm_region_commands']
        #self._debug_values(rhythm_region_commands, 'rhythm region commands')
        rhythm_command_durations = [x.timespan.duration for x in rhythm_region_commands]
        #self._debug(rhythm_command_durations, 'rhythm command durations')
        division_region_expressions = \
            self.score_specification.contexts[voice.name]['division_region_expressions']
        #self._debug_values(division_region_expressions, 'division region expressions')
        division_region_durations = [x.timespan.duration for x in division_region_expressions]
        #self._debug(division_region_durations, 'division region durations')
        assert sum(rhythm_command_durations) == sum(division_region_durations)
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
            voice_division_list.divisions, 
            rhythm_region_start_division_counts, cyclic=False, overhang=False)
        rhythm_region_division_lists = [
            divisiontools.DivisionList(x, voice_name=voice.name) for x in rhythm_region_division_lists]
        assert len(rhythm_region_division_lists) == len(rhythm_command_merged_durations)
        #self._debug_values(rhythm_region_division_lists, 'rrdls')
        rhythm_region_durations = [x.duration for x in rhythm_region_division_lists]
        #self._debug(rhythm_region_durations, 'rrds')
        cumulative_sums = mathtools.cumulative_sums_zero(rhythm_region_durations)
        rhythm_region_start_offsets = cumulative_sums[:-1]
        rhythm_region_start_offsets = [durationtools.Offset(x) for x in rhythm_region_start_offsets]
        rhythm_region_stop_offsets = cumulative_sums[1:]
        rhythm_region_stop_offsets = [durationtools.Offset(x) for x in rhythm_region_stop_offsets]
        rhythm_command_duration_pairs = [(x, x.timespan.duration) for x in rhythm_region_commands]
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
        rhythm_quintuples = [(voice.name,) + x for x in rhythm_quadruples]
        return rhythm_quintuples

    def make_rhythm_region_expression(
        self, rhythm_maker, rhythm_region_division_list, start_offset, rhythm_command):
        if rhythm_region_division_list:
            leaf_lists = rhythm_maker(rhythm_region_division_list.pairs)
            rhythm_containers = [containertools.Container(x) for x in leaf_lists]
            timespan = timespantools.Timespan(start_offset)
            rhythm_region_expression = settingtools.RhythmRegionProduct(
                payload=rhythm_containers, 
                voice_name=rhythm_region_division_list.voice_name, 
                timespan=timespan)
            self.conditionally_beam_rhythm_containers(rhythm_maker, rhythm_containers)
            return rhythm_region_expression

    def make_rhythm_region_expression_from_parseable_string(
        self, parseable_string, rhythm_region_division_list, start_offset, rhythm_command):
        component = iotools.p(parseable_string)
        timespan = timespantools.Timespan(start_offset)
        rhythm_region_expression = settingtools.RhythmRegionProduct(
            payload=[component],
            voice_name=rhythm_region_division_list.voice_name, 
            timespan=timespan)
        duration_needed = sum([durationtools.Duration(x) for x in rhythm_region_division_list])
        stop_offset = start_offset + duration_needed
        if rhythm_region_expression.timespan.stops_before_offset(stop_offset):
            rhythm_region_expression.repeat_to_stop_offset(stop_offset)
        elif rhythm_region_expression.timespan.stops_after(stop_offset):
            rhythm_region_expression.set_offsets(stop_offset=stop_offset)
        return rhythm_region_expression

    def make_rhythm_region_expressions(self):
        while self.score_specification.all_rhythm_quintuples:
            made_progress = False
            for rhythm_quintuple in self.score_specification.all_rhythm_quintuples[:]:
                voice_name = rhythm_quintuple[0]
                voice_proxy = self.score_specification.contexts[voice_name]
                voice_rhythm_region_expressions = voice_proxy['rhythm_region_expressions']
                rhythm_quadruple = rhythm_quintuple[1:]
                if isinstance(rhythm_quadruple[0], str):
                    rhythm_region_expression = \
                        self.make_rhythm_region_expression_from_parseable_string(*rhythm_quadruple)
                elif isinstance(rhythm_quadruple[0], rhythmmakertools.RhythmMaker):
                    rhythm_region_expression = self.make_rhythm_region_expression(*rhythm_quadruple)
                elif isinstance(rhythm_quadruple[0], selectortools.CounttimeComponentSelector):
                    counttime_component_selector, start_offset, stop_offset = rhythm_quadruple[:3]
                    rhythm_region_expression = \
                        counttime_component_selector._get_rhythm_region_expression(
                        self.score_specification, counttime_component_selector.voice_name, 
                        start_offset, stop_offset)
                else:
                    raise TypeError(rhythm_quadruple[0])
                if rhythm_region_expression is not None:
                    self.score_specification.all_rhythm_quintuples.remove(rhythm_quintuple)
                    made_progress = True
                    voice_rhythm_region_expressions.delete_material_that_intersects_timespan(
                            rhythm_region_expression.timespan)
                    voice_rhythm_region_expressions.append(rhythm_region_expression)
                    voice_rhythm_region_expressions.sort()
            if not made_progress:
                raise Exception('cyclic rhythm specification.')

    def make_skip_token_rhythm_command(self, voice_name, start_offset, stop_offset):
        timespan = timespantools.Timespan(start_offset, stop_offset)
        return settingtools.RhythmRegionCommand(
            requesttools.AbsoluteRequest(library.skip_tokens),
            voice_name, 
            timespan,
            fresh=True
            )

    def make_time_signature_division_command(self, voice_name, start_offset, stop_offset):
        timespan = timespantools.Timespan(start_offset, stop_offset)
        divisions = self.score_specification.get_time_signature_slice(timespan)
        return settingtools.DivisionRegionCommand(
            requesttools.AbsoluteRequest(divisions),
            voice_name, 
            timespan,
            fresh=True,
            truncate=True
            )

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
        elif isinstance(time_signature_setting.request, requesttools.CommandRequest):
            time_signatures = self.time_signature_command_request_to_time_signatures(
                time_signature_setting.request)
        elif isinstance(time_signature_setting.request, selectortools.BackgroundMeasureSelector):
            background_measure_selector = time_signature_setting.request
            time_signatures = background_measure_selector._get_time_signatures_without_timespan(
                self.score_specification)
        else:
            raise TypeError(time_signature_setting.request)
        if time_signatures:
            segment_specification = self.get_start_segment_specification(time_signature_setting.anchor)
            segment_specification._time_signatures = time_signatures[:]
            self.score_specification.all_time_signature_commands.remove(time_signature_setting)

    def make_voice_division_lists(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_division_list = divisiontools.DivisionList([], voice.name)
            expressions = self.score_specification.contexts[voice.name]['division_region_expressions']
            #self._debug(expressions, 'expressions')
            divisions = [expression.payload.divisions for expression in expressions]
            divisions = sequencetools.flatten_sequence(divisions, depth=1)
            start_offset = durationtools.Offset(0)
            for division in divisions:
                offset_positioned_division = copy.deepcopy(division)
                offset_positioned_division._start_offset = durationtools.Offset(start_offset)
                start_offset += division.duration
                voice_division_list.divisions.append(offset_positioned_division)
            self.score_specification.contexts[voice.name]['voice_division_list'] = voice_division_list

    def populate_all_region_commands(self, attribute):
        if self.score_specification.segment_specifications:
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                region_commands = self.get_region_commands_for_voice(voice.name, attribute)
                singular_attribute = attribute.rstrip('s')
                key = '{}_region_commands'.format(singular_attribute)
                self.score_specification.contexts[voice.name][key][:] = region_commands[:]
                all_region_commands = getattr(self.score_specification, 'all_' + key)
                for region_command in region_commands:
                    if region_command not in all_region_commands:
                        all_region_commands.append(region_command)

    def populate_all_rhythm_quintuples(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_division_list = self.score_specification.contexts[voice.name]['voice_division_list']
            #self._debug(voice_division_list, 'vdl')
            if voice_division_list:
                rhythm_quintuples = self.make_rhythm_quintuples_for_voice(voice, voice_division_list)
                #self._debug_values(rhythm_quintuples, 'rq')
                self.score_specification.all_rhythm_quintuples.extend(rhythm_quintuples)

    # TODO: eventually merge with self.populate_all_region_commands()
    def populate_all_time_signature_commands(self):
        for segment_specification in self.score_specification.segment_specifications:
            time_signature_settings = \
                segment_specification.single_context_settings_by_context.score_context_proxy.get_settings(
                attribute='time_signatures')
            if not time_signature_settings:
                continue
            time_signature_setting = time_signature_settings[-1]
            self.score_specification.all_time_signature_commands.append(time_signature_setting)

    def rhythm_command_prolongs_expr(self, current_rhythm_command, expr):
        # check that current rhythm command bears a rhythm material request
        assert isinstance(current_rhythm_command, settingtools.RhythmRegionCommand)
        current_material_request = current_rhythm_command.request
        assert isinstance(current_material_request, selectortools.CounttimeComponentSelector)
        # fuse only if expr is also a rhythm command that bears a rhythm material request
        if not isinstance(expr, settingtools.RhythmRegionCommand):
            return False
        else:
            previous_rhythm_command = expr
        previous_material_request = getattr(previous_rhythm_command, 'request', None)
        if not isinstance(previous_material_request, selectortools.CounttimeComponentSelector):
            return False
        # fuse only if current and previous commands request same material
        if not current_material_request == previous_material_request:
            return False
        return True

    # TODO: migrate to RhythmCommandRequest.get_payload(score_specification, ...)
    def rhythm_command_request_to_rhythm_maker(self, rhythm_command_request, voice_name):
        assert isinstance(rhythm_command_request, requesttools.CommandRequest)
        assert rhythm_command_request.attribute == 'rhythm'
        #self._debug(rhythm_command_request, 'rcr')
        requested_segment_identifier = rhythm_command_request.offset.start_segment_identifier
        #self._debug(requested_segment_identifier, 'segment')
        requested_offset = rhythm_command_request.offset._get_offset(self.score_specification, voice_name)
        #self._debug(requested_offset, 'offset')
        timespan_inventory = timespantools.TimespanInventory()
        for rhythm_region_command in self.score_specification.all_rhythm_region_commands:
            if True:
                if not rhythm_region_command.request == rhythm_command_request:
                    timespan_inventory.append(rhythm_region_command)
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=requested_offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        #self._debug_values(candidate_commands, 'candidates')
        segment_specification = self.get_start_segment_specification(requested_segment_identifier)
        source_command = self.get_first_element_in_expr_by_parentage(
            candidate_commands, segment_specification, rhythm_command_request.voice_name, 
            include_improper_parentage=True)
        assert source_command is not None
        #self._debug(source_command, 'source_command')
        absolute_request = source_command.request
        assert isinstance(source_command.request, requesttools.AbsoluteRequest)
        assert isinstance(source_command.request.payload, rhythmmakertools.RhythmMaker)
        rhythm_maker = copy.deepcopy(source_command.request.payload)
        rhythm_maker, start_offset = rhythm_command_request._apply_request_modifiers(
            rhythm_maker, source_command.timespan.start_offset)
        return rhythm_maker

    # do we eventually need to do this with time signature settings, too?
    def single_context_setting_to_command(self, single_context_setting, segment_specification, voice_name):
        anchor_timespan = self.score_specification.get_anchor_timespan(single_context_setting, voice_name)
        region_command_class = self.attribute_to_region_command_class(single_context_setting.attribute)
        command = region_command_class(
            single_context_setting.request, 
            single_context_setting.context_name,
            anchor_timespan,
            fresh=single_context_setting.fresh
            )
        if single_context_setting.attribute == 'divisions':
            command = command.new(truncate=single_context_setting.truncate)
        return command

    def sort_and_split_raw_commands(self, raw_commands):
        #self._debug_values(raw_commands, 'raw')
        cooked_commands = []
        for raw_command in raw_commands:
            command_was_delayed, command_was_split = False, False
            commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split = [], [], [], []
            for cooked_command in cooked_commands:
                if raw_command.timespan.contains_expr_improperly(cooked_command):
                    commands_to_remove.append(cooked_command)
                elif raw_command.timespan.delays_expr(cooked_command):
                    commands_to_delay.append(cooked_command)
                elif raw_command.timespan.curtails_expr(cooked_command):
                    commands_to_curtail.append(cooked_command)
                elif raw_command.timespan.trisects_expr(cooked_command):
                    commands_to_split.append(cooked_command)
            #print commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split
            for command_to_remove in commands_to_remove:
                cooked_commands.remove(command_to_remove)
            for command_to_curtail in commands_to_curtail:
                timespan = timespantools.Timespan(
                    command_to_curtail.timespan.start_offset, raw_command.timespan.start_offset)
                command_to_curtail._timespan = timespan
            for command_to_delay in commands_to_delay:
                timespan = timespantools.Timespan(
                    raw_command.timespan.stop_offset, command_to_delay.timespan.stop_offset)
                command_to_delay._timespan = timespan
                command_was_delayed = True
            # TODO: branch inside and implement a method to split while treating cyclic payload smartly.
            # or, alternatively, special-case for commands that cover the entire duration of score.
            for command_to_split in commands_to_split:
                left_command = command_to_split
                middle_command = raw_command
                right_command = copy.deepcopy(left_command)
                timespan = timespantools.Timespan(
                    left_command.timespan.start_offset, middle_command.timespan.start_offset)
                left_command._timespan = timespan
                timespan = timespantools.Timespan(
                    middle_command.timespan.stop_offset, right_command.timespan.stop_offset)
                right_command._timespan = timespan
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

    def supply_missing_region_commands(self, region_commands, voice_name, attribute):
        #self._debug_values(region_commands, 'region commands')
        if not region_commands and not self.score_specification.time_signatures:
            return []
        elif not region_commands and self.score_specification.time_signatures:
            region_command = self.make_default_region_command(
                voice_name, self.score_specification.timespan.start_offset, 
                self.score_specification.timespan.stop_offset, attribute)
            return [region_command]
        if not region_commands[0].timespan.starts_when_expr_starts(self.score_specification):
            region_command = self.make_default_region_command(
                voice_name, self.score_specification.timespan.start_offset, 
                region_commands[0].timespan.start_offset, attribute)
            region_commands.insert(0, region_command)
        if not region_commands[-1].timespan.stops_when_expr_stops(self.score_specification):
            region_command = self.make_default_region_command(
                voice_name, region_commands[-1].timespan.stop_offset, 
                self.score_specification.timespan.stop_offset, attribute)
            region_commands.append(region_command)
        if len(region_commands) == 1:
            return region_commands
        result = []
        for left_region_command, right_region_command in \
            sequencetools.iterate_sequence_pairwise_strict(region_commands):
            assert not left_region_command.timespan.starts_after_expr_starts(right_region_command.timespan)
            result.append(left_region_command)
            if left_region_command.timespan.stops_before_expr_starts(right_region_command.timespan):
                region_command = self.make_default_region_command(voice_name, 
                    left_region_command.timespan.stop_offset, 
                    right_region_command.timespan.start_offset, attribute)
                result.append(region_command)
        result.append(right_region_command)
        return result

    def timespan_expressions_to_durations(self, expr):
        assert isinstance(expr, (tuple, list))
        result = []
        for element in expr:
            if isinstance(element, timeexpressiontools.TimespanExpression):
                context_name = None
                timespan = element._get_timespan(self.score_specification, context_name)
                result.append(timespan.duration)
            else:
                result.append(element)
        return result

    # TODO: migrate to TimeSignatureCommandRequest.get_payload(score_specification, ...)
    def time_signature_command_request_to_time_signatures(self, command_request):
        assert isinstance(command_request, requesttools.CommandRequest)
        assert command_request.attribute == 'time_signatures'
        segment_specification = self.get_start_segment_specification(command_request.offset)
        time_signatures = segment_specification.time_signatures[:]
        time_signatures, dummy = command_request._apply_request_modifiers(time_signatures, None)
        return time_signatures
