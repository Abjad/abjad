import copy
from abjad.tools import *
from experimental import divisiontools
from experimental import exceptions
from experimental import helpertools
from experimental import library
from experimental import requesttools
from experimental import settingtools
from experimental import specificationtools
from experimental import symbolictimetools
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

    def apply_source_transforms_to_target(self, source, target):
        if getattr(source, 'index', None):
            raise NotImplementedError
        if getattr(source, 'count', None):
            raise NotImplementedError
        if getattr(source, 'reverse', False):
            target.reverse()
        if getattr(source, 'rotation', None):
            target.rotate(source.rotation)

    def attribute_to_command_klass(self, attribute):
        if attribute == 'divisions':
            return settingtools.DivisionCommand
        elif attribute == 'rhythm':
            return settingtools.RhythmCommand
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
            self.score_specification._segment_durations = segment_durations
            self.score_specification._score_duration = sum(self.score_specification.segment_durations)
            self.score_specification._start_offset = durationtools.Offset(0)
            self.score_specification._stop_offset = durationtools.Offset(
                self.score_specification.score_duration)
            segment_offset_pairs = mathtools.cumulative_sums_zero_pairwise(
                self.score_specification.segment_durations)
            segment_offset_pairs = [
                (durationtools.Offset(x[0]), durationtools.Offset(x[1])) for x in segment_offset_pairs]
            self.score_specification._segment_offset_pairs = segment_offset_pairs

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
        requested_segment_identifier = division_command_request.symbolic_offset.start_segment_identifier
        requested_offset = division_command_request.symbolic_offset.get_score_offset(
            self.score_specification, voice_name)
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
        divisions = requesttools.apply_request_transforms(absolute_request, absolute_request.payload)
        return divisions

    def division_material_request_to_division_region_expressions(self, division_material_request):
        assert isinstance(division_material_request, requesttools.MaterialRequest)
        assert division_material_request.attribute == 'divisions'
        #self._debug(division_material_request, 'division material request')
        anchor = division_material_request.anchor
        voice_name = division_material_request.voice_name
        if isinstance(anchor, str):
            start_offset, stop_offset = self.score_specification.segment_identifier_expression_to_offsets(anchor)
        else:
            start_offset, stop_offset = anchor._get_offsets(self.score_specification, voice_name)
        #self._debug((voice_name, start_offset, stop_offset), 'request parameters')
        division_region_expressions = \
            self.score_specification.contexts[voice_name]['division_region_expressions']
        #self._debug(division_region_expressions, 'division region expressions')
        source_timespan = timespantools.LiteralTimespan(start_offset, stop_offset)
        timespan_time_relation = timerelationtools.timespan_2_intersects_timespan_1(
            timespan_1=source_timespan)
        division_region_expressions = division_region_expressions.get_timespans_that_satisfy_time_relation(
            timespan_time_relation)
        division_region_expressions = timespantools.TimespanInventory(division_region_expressions)
        #self._debug(division_region_expressions, 'drx')
        if not division_region_expressions:
            return
        if not division_region_expressions.all_are_contiguous:
            return
        trimmed_division_region_expressions = copy.deepcopy(division_region_expressions)
        trimmed_division_region_expressions = timespantools.TimespanInventory(
            trimmed_division_region_expressions)
        keep_timespan = timespantools.LiteralTimespan(start_offset, stop_offset)
        trimmed_division_region_expressions.keep_material_that_intersects_timespan(keep_timespan)
        #self._debug(trimmed_division_region_expressions, 'trimmed')
        self.apply_source_transforms_to_target(division_material_request, trimmed_division_region_expressions)
        return trimmed_division_region_expressions

    def division_region_command_to_division_region_expression(self, division_region_command, voice_name):
        #self._debug(division_region_command, 'command')
        if isinstance(division_region_command.request, list):
            divisions = division_region_command.request
            divisions = [divisiontools.Division(x) for x in divisions]
            region_duration = division_region_command.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
        elif isinstance(division_region_command.request, requesttools.AbsoluteRequest):
            request = division_region_command.request
            payload = request.payload
            #self._debug(payload, 'payload')
            divisions = self.symbolic_timespans_to_durations(payload)
            divisions = requesttools.apply_request_transforms(request, divisions)
            divisions = requesttools.apply_request_transforms(division_region_command, divisions) 
            #self._debug(divisions, 'divisions')
            divisions = [divisiontools.Division(x) for x in divisions]
            region_duration = division_region_command.duration
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
        elif isinstance(division_region_command.request, requesttools.CommandRequest):
            assert division_region_command.request.attribute == 'divisions'
            division_command_request = division_region_command.request
            divisions = self.division_command_request_to_divisions(division_command_request, voice_name)
            divisions = requesttools.apply_request_transforms(division_command_request, divisions)
            divisions = requesttools.apply_request_transforms(division_region_command, divisions) 
            division_region_command._request = divisions
            division_region_expression = self.division_region_command_to_division_region_expression(
                division_region_command, voice_name)
            return division_region_expression
        elif isinstance(division_region_command.request, requesttools.MaterialRequest) and \
            division_region_command.request.attribute == 'naive_beats':
            start_offset, stop_offset = division_region_command.offsets
            divisions = self.get_naive_time_signature_beat_slice(start_offset, stop_offset)
            divisions = requesttools.apply_request_transforms(division_region_command.request, divisions)
            divisions = requesttools.apply_request_transforms(division_region_command, divisions) 
            division_region_command._request = divisions
            division_region_expression = self.division_region_command_to_division_region_expression(
                division_region_command, voice_name)
            return division_region_expression
        elif isinstance(division_region_command.request, requesttools.MaterialRequest) and \
            division_region_command.request.attribute == 'divisions':
            division_region_expressions = self.division_material_request_to_division_region_expressions(
                division_region_command.request)
            if division_region_expressions is None:
                return
            for division_region_expression in division_region_expressions:
                division_region_expression._voice_name = voice_name
            addendum = division_region_command.start_offset - division_region_expressions[0].start_offset
            division_region_expressions.translate_timespans(addendum)
            self.apply_source_transforms_to_target(division_region_command, division_region_expressions)
            division_region_expressions.adjust_to_stop_offset(division_region_command.stop_offset)
            return division_region_expressions
        elif isinstance(division_region_command.request, requesttools.MaterialRequest) and \
            division_region_command.request.attribute == 'time_signatures':    
            time_signatures = self.time_signature_material_request_to_time_signatures(
                division_region_command.request)
            divisions = [divisiontools.Division(x) for x in time_signatures]
            divisions = requesttools.apply_request_transforms(division_region_command, divisions)
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
            if isinstance(rhythm_command.request, requesttools.AbsoluteRequest):
                result.append((rhythm_command.request.payload, division_list, start_offset, rhythm_command))
            elif isinstance(rhythm_command.request, requesttools.CommandRequest):
                rhythm_maker = self.rhythm_command_request_to_rhythm_maker(
                    rhythm_command.request, rhythm_command.request.voice_name)
                result.append((rhythm_maker, division_list, start_offset, rhythm_command))
            elif isinstance(rhythm_command.request, requesttools.MaterialRequest):
                assert rhythm_command.request.attribute == 'rhythm'
                if result and self.rhythm_command_prolongs_expr(rhythm_command, result[-1][0]):
                    last_start_offset = result.pop()[1]
                    new_entry = (rhythm_command,
                        last_start_offset,
                        stop_offset,
                        rhythm_command)
                else:
                    new_entry = (rhythm_command,
                            rhythm_command.start_offset, 
                            rhythm_command.stop_offset, 
                            rhythm_command)
                result.append(new_entry)
            else:
                raise TypeError(rhythm_command.request)
        # make one last pass over commands that bear a material request
        postprocessed_result = []
        for quadruple in result:
            if isinstance(quadruple[0], settingtools.Command):
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
                if element.context_name == context_name:
                    return element

    # TODO: combine with self.get_time_signature_slice()
    def get_naive_time_signature_beat_slice(self, start_offset, stop_offset):
        time_signatures = self.score_specification.time_signatures
        assert time_signatures
        naive_beats = []
        for time_signature in time_signatures:
            numerator, denominator = time_signature.pair
            naive_beats.extend(numerator * [mathtools.NonreducedFraction(1, denominator)])
        #self._debug(naive_beats, 'naive beats')
        slice_duration = stop_offset - start_offset
        weights = [start_offset, slice_duration]
        shards = sequencetools.split_sequence_by_weights(
            naive_beats, weights, cyclic=False, overhang=False)
        result = shards[1]
        result = [x.pair for x in result]
        return result

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
        self.calculate_score_and_segment_durations()

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
                #self._debug(voice, 'voice')
                division_region_commands = \
                    self.score_specification.contexts[voice.name]['division_region_commands']
                current_commands[voice] = division_region_commands[:]
                division_region_commands_to_reattempt = []
                for division_region_command in division_region_commands:
                    #self._debug(voice.name, 'voice')
                    #self._debug(division_region_command, 'command')
                    division_region_expression = self.division_region_command_to_division_region_expression(
                        division_region_command, voice.name)
                    #self._debug(division_region_expression, 'division region expression')
                    #print ''
                    if division_region_expression is not None:
                        # TODO: collapse branches by changing 
                        # self.division_region_command_to_division_region_expression (singular) to
                        # self.division_region_command_to_division_region_expressions (plural) 
                        # which will then always return a list of zero or more expressions
                        if isinstance(division_region_expression, settingtools.OffsetPositionedDivisionList):
                            self.score_specification.contexts[voice.name]['division_region_expressions'].append(
                                division_region_expression)
                        elif isinstance(division_region_expression, list):
                            self.score_specification.contexts[voice.name]['division_region_expressions'].extend(
                                division_region_expression)
                    else:
                        division_region_commands_to_reattempt.append(division_region_command)
                        redo = True
                self.score_specification.contexts[voice.name]['division_region_commands'] = \
                    division_region_commands_to_reattempt[:]
                # sort may have to happen as each expression adds in, above
                self.score_specification.contexts[voice.name]['division_region_expressions'].sort()
            # check to see if we made absolutely no intepretive progress in this iteration through loop
            if current_commands == previous_commands:
                raise exceptions.CyclicSpecificationError
            else:
                previous_commands = current_commands

    def make_naive_time_signature_beat_division_command(self, voice, start_offset, stop_offset):
        divisions = self.get_naive_time_signature_beat_slice(start_offset, stop_offset)
        return settingtools.DivisionCommand(
            requesttools.AbsoluteRequest(divisions),
            voice.name, 
            start_offset,
            stop_offset,
            fresh=True,
            truncate=True
            )

    def make_rhythm_quintuples_for_voice(self, voice, voice_division_list):
        #self._debug(voice, 'voice')
        #self._debug(voice_division_list, 'voice division list')
        rhythm_region_commands = self.score_specification.contexts[voice.name]['rhythm_region_commands']
        #self._debug_values(rhythm_region_commands, 'rhythm region commands')
        rhythm_command_durations = [x.duration for x in rhythm_region_commands]
        #self._debug(rhythm_command_durations, 'rhythm command durations')
        division_region_expressions = \
            self.score_specification.contexts[voice.name]['division_region_expressions']
        #self._debug_values(division_region_expressions, 'division region expressions')
        division_region_durations = [x.duration for x in division_region_expressions]
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
            voice_division_list.divisions, rhythm_region_start_division_counts, cyclic=False, overhang=False)
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
        rhythm_command_duration_pairs = [(x, x.duration) for x in rhythm_region_commands]
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
            rhythm_maker = requesttools.apply_request_transforms(rhythm_command, rhythm_maker)
            leaf_lists = rhythm_maker(rhythm_region_division_list.pairs)
            rhythm_containers = [containertools.Container(x) for x in leaf_lists]
            rhythm_region_expression = settingtools.OffsetPositionedRhythmExpression(
                rhythm_containers, 
                voice_name=rhythm_region_division_list.voice_name, start_offset=start_offset)
            self.conditionally_beam_rhythm_containers(rhythm_maker, rhythm_containers)
            return rhythm_region_expression

    def make_rhythm_region_expression_from_parseable_string(
        self, parseable_string, rhythm_region_division_list, start_offset, rhythm_command):
        component = iotools.p(parseable_string)
        rhythm_region_expression = settingtools.OffsetPositionedRhythmExpression(
            music=[component],
            voice_name=rhythm_region_division_list.voice_name, 
            start_offset=start_offset)
        self.apply_source_transforms_to_target(rhythm_command, rhythm_region_expression)
        duration_needed = sum([durationtools.Duration(x) for x in rhythm_region_division_list])
        stop_offset = start_offset + duration_needed
        if rhythm_region_expression.stop_offset < stop_offset:
            rhythm_region_expression.repeat_to_stop_offset(stop_offset)
        elif stop_offset < rhythm_region_expression.stop_offset:
            rhythm_region_expression.trim_to_stop_offset(stop_offset)
        return rhythm_region_expression

    def make_rhythm_region_expressions(self):
        #self._debug(len(self.score_specification.all_rhythm_quintuples), 'quintuple count')
        while self.score_specification.all_rhythm_quintuples:
            #self._debug(len(self.score_specification.all_rhythm_quintuples), 'len')
            previous_all_rhythm_quintuples = self.score_specification.all_rhythm_quintuples[:]
            for rhythm_quintuple in self.score_specification.all_rhythm_quintuples[:]:
                voice_name = rhythm_quintuple[0]
                rhythm_quadruple = rhythm_quintuple[1:]
                #self._debug(rhythm_quadruple, 'rhythm quadruple')
                #self._debug(rhythm_quadruple[0], 'rhythm quadruple 0')
                if isinstance(rhythm_quadruple[0], str):
                    rhythm_region_expression = self.make_rhythm_region_expression_from_parseable_string(
                        *rhythm_quadruple)
                elif isinstance(rhythm_quadruple[0], rhythmmakertools.RhythmMaker):
                    rhythm_region_expression = self.make_rhythm_region_expression(*rhythm_quadruple)
                elif isinstance(rhythm_quadruple[0], requesttools.MaterialRequest):
                    rhythm_region_expression = self.rhythm_material_request_to_rhythm_region_expression(
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
            if self.score_specification.all_rhythm_quintuples == previous_all_rhythm_quintuples:
                raise exceptions.CyclicSpecificationError('cyclic rhythm specification')

    def make_skip_token_rhythm_command(self, voice_name, start_offset, stop_offset):
        return settingtools.RhythmCommand(
            requesttools.AbsoluteRequest(library.skip_tokens),
            voice_name, 
            start_offset,
            stop_offset,
            fresh=True
            )

    def make_time_signature_division_command(self, voice_name, start_offset, stop_offset):
        divisions = self.get_time_signature_slice(start_offset, stop_offset)
        return settingtools.DivisionCommand(
            requesttools.AbsoluteRequest(divisions),
            voice_name, 
            start_offset,
            stop_offset,
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
            segment_specification = self.get_start_segment_specification(time_signature_setting.anchor)
            segment_specification._time_signatures = time_signatures[:]
            self.score_specification.all_time_signature_commands.remove(time_signature_setting)

    def make_voice_division_lists(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_division_list = divisiontools.DivisionList([], voice.name)
            expressions = self.score_specification.contexts[voice.name]['division_region_expressions']
            #self._debug(expressions, 'expressions')
            divisions = [expression.divisions for expression in expressions]
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
        assert isinstance(current_rhythm_command, settingtools.RhythmCommand)
        current_material_request = current_rhythm_command.request
        assert isinstance(current_material_request, requesttools.MaterialRequest)
        assert current_material_request.attribute == 'rhythm'
        # fuse only if expr is also a rhythm command that bears a rhythm material request
        if not isinstance(expr, settingtools.RhythmCommand):
            return False
        else:
            previous_rhythm_command = expr
        previous_material_request = getattr(previous_rhythm_command, 'request', None)
        if not isinstance(previous_material_request, requesttools.MaterialRequest):
            return False        
        if not previous_material_request.attribute == 'rhythm':
            return False
        # fuse only if current and previous commands request same material
        if not current_material_request == previous_material_request:
            return False
        # TODO: implement one-line statement for command treatment comparison
        # fuse only if current and previous commands treat material equally
        for attribute in ('index', 'count', 'reverse', 'rotation'):
            if getattr(current_rhythm_command, attribute, None) != \
                getattr(previous_rhythm_command, attribute, None):
                return False
        return True

    def rhythm_command_request_to_rhythm_maker(self, rhythm_command_request, voice_name):
        assert isinstance(rhythm_command_request, requesttools.CommandRequest)
        assert rhythm_command_request.attribute == 'rhythm'
        #self._debug(rhythm_command_request, 'rcr')
        requested_segment_identifier = rhythm_command_request.symbolic_offset.start_segment_identifier
        #self._debug(requested_segment_identifier, 'segment')
        requested_offset = rhythm_command_request.symbolic_offset.get_score_offset(
            self.score_specification, voice_name)
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
        rhythm_maker = requesttools.apply_request_transforms(rhythm_command_request, rhythm_maker)
        return rhythm_maker

    def rhythm_material_request_to_rhythm_region_expression(
        self, rhythm_material_request, start_offset, stop_offset, rhythm_command):
        assert isinstance(rhythm_material_request, requesttools.MaterialRequest)
        assert rhythm_material_request.attribute == 'rhythm'
        #self._debug(rhythm_material_request, 'rhythm request')
        #self._debug((start_offset, stop_offset), 'offsets')
        voice_name = rhythm_material_request.voice_name
        if isinstance(rhythm_material_request.anchor, str):
            source_score_offsets = self.score_specification.segment_identifier_expression_to_offsets(
                rhythm_material_request.anchor)
        else:
            source_score_offsets = rhythm_material_request.anchor._get_offsets(
                self.score_specification, rhythm_material_request.voice_name)
        source_timespan = timespantools.LiteralTimespan(*source_score_offsets)
        #self._debug(source_timespan, 'source timespan')
        rhythm_region_expressions = \
            self.score_specification.contexts[voice_name]['rhythm_region_expressions']
        #self._debug_values(rhythm_region_expressions, 'rhythm region expressions')
        timespan_time_relation = timerelationtools.timespan_2_intersects_timespan_1(
            timespan_1=source_timespan)
        rhythm_region_expressions = rhythm_region_expressions.get_timespans_that_satisfy_time_relation(
            timespan_time_relation)
        #self._debug(rhythm_region_expressions, 'rhythm region expressions')
        if not rhythm_region_expressions:
            return
        rhythm_region_expressions = copy.deepcopy(rhythm_region_expressions)
        rhythm_region_expressions = timespantools.TimespanInventory(rhythm_region_expressions)
        rhythm_region_expressions.sort()
        #self._debug_values(rhythm_region_expressions, 'rhythm region expressions')
        #self._debug(source_timespan, 'source timespan', blank=True)
        assert source_timespan.is_well_formed, repr(source_timespan)
        rhythm_region_expressions.keep_material_that_intersects_timespan(source_timespan)
        result = settingtools.OffsetPositionedRhythmExpression(voice_name=voice_name, start_offset=start_offset)
        for rhythm_region_expression in rhythm_region_expressions:
            result.music.extend(rhythm_region_expression.music)
        #self._debug(result, 'result')
        assert wellformednesstools.is_well_formed_component(result.music)
        self.apply_source_transforms_to_target(rhythm_material_request, result)
        self.apply_source_transforms_to_target(rhythm_command, result)
        result.adjust_to_offsets(start_offset=start_offset, stop_offset=stop_offset)
        result.repeat_to_stop_offset(stop_offset)
        return result

    # do we eventually need to do this with time signature settings, too?
    def single_context_setting_to_command(self, single_context_setting, segment_specification, voice_name):
        assert single_context_setting.start_segment_name == segment_specification.segment_name
        #self._debug(single_context_setting.anchor, 'anchor')
        if isinstance(single_context_setting.anchor, str):
            start_offset, stop_offset = self.score_specification.segment_identifier_expression_to_offsets(
                single_context_setting.anchor)
        else:
            start_offset, stop_offset = single_context_setting.anchor._get_offsets(
                self.score_specification, voice_name)
        #self._debug((start_offset, stop_offset), 'anchor offsets')
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
                if timerelationtools.timespan_2_contains_timespan_1_improperly(
                    cooked_command, raw_command):
                    commands_to_remove.append(cooked_command)
                elif timerelationtools.timespan_2_delays_timespan_1(cooked_command, raw_command):
                    commands_to_delay.append(cooked_command)
                elif timerelationtools.timespan_2_curtails_timespan_1(cooked_command, raw_command):
                    commands_to_curtail.append(cooked_command)
                elif timerelationtools.timespan_2_trisects_timespan_1(cooked_command, raw_command):
                    commands_to_split.append(cooked_command)
            #print commands_to_remove, commands_to_curtail, commands_to_delay, commands_to_split
            for command_to_remove in commands_to_remove:
                cooked_commands.remove(command_to_remove)
            for command_to_curtail in commands_to_curtail:
                command_to_curtail._stop_offset = raw_command.start_offset
            for command_to_delay in commands_to_delay:
                command_to_delay._start_offset = raw_command.stop_offset
                command_was_delayed = True
            # NEXT TODO: branch inside and implement a method to split while treating cyclic payload smartly.
            # or, alternatively, special-case for commands that cover the entire duration of score.
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

    def supply_missing_region_commands(self, region_commands, voice_name, attribute):
        #self._debug_values(region_commands, 'region commands')
        if not region_commands and not self.score_specification.time_signatures:
            return []
        elif not region_commands and self.score_specification.time_signatures:
            region_command = self.make_default_region_command(
                voice_name, self.score_specification.start_offset, self.score_specification.stop_offset, attribute)
            return [region_command]
        if not region_commands[0].start_offset == self.score_specification.start_offset:
            region_command = self.make_default_region_command(
                voice_name, self.score_specification.start_offset, region_commands[0].start_offset, attribute)
            region_commands.insert(0, region_command)
        if not region_commands[-1].stop_offset == self.score_specification.stop_offset:
            region_command = self.make_default_region_command(
                voice_name, region_commands[-1].stop_offset, self.score_specification.stop_offset, attribute)
            region_commands.append(region_command)
        if len(region_commands) == 1:
            return region_commands
        result = []
        for left_region_command, right_region_command in \
            sequencetools.iterate_sequence_pairwise_strict(region_commands):
            assert left_region_command.stop_offset <= right_region_command.start_offset
            result.append(left_region_command)
            if left_region_command.stop_offset < right_region_command.start_offset:
                region_command = self.make_default_region_command(voice_name, 
                    left_region_command.stop_offset, right_region_command.start_offset, attribute)
                result.append(region_command)
        result.append(right_region_command)
        return result

    def symbolic_timespans_to_durations(self, expr):
        assert isinstance(expr, (tuple, list))
        result = []
        for element in expr:
            if isinstance(element, symbolictimetools.SymbolicTimespan):
                context_name = None
                start_offset, stop_offset = element._get_offsets(self.score_specification, context_name)
                duration = stop_offset - start_offset
                result.append(duration)
            else:
                result.append(element)
        return result


    def time_signature_command_request_to_time_signatures(self, command_request):
        assert isinstance(command_request, requesttools.CommandRequest)
        assert command_request.attribute == 'time_signatures'
        segment_specification = self.get_start_segment_specification(command_request.symbolic_offset)
        time_signatures = segment_specification.time_signatures[:]
        time_signatures = requesttools.apply_request_transforms(command_request, time_signatures)
        return time_signatures

    def time_signature_material_request_to_time_signatures(self, material_request):
        assert isinstance(material_request, requesttools.MaterialRequest), repr(material_request)
        assert material_request.attribute == 'time_signatures'
        segment_specification = self.get_start_segment_specification(
            material_request.start_segment_identifier)
        single_context_settings = self.get_single_context_settings_that_start_during_segment(
            segment_specification, material_request.voice_name, material_request.attribute, 
            include_improper_parentage=True)
        assert len(single_context_settings) == 1
        single_context_setting = single_context_settings[0]
        absolute_request = single_context_setting.request
        if not isinstance(absolute_request, requesttools.AbsoluteRequest):
            raise exceptions.CyclicSpecificationError(absolute_request)
        time_signatures = requesttools.apply_request_transforms(material_request, absolute_request.payload)
        return time_signatures
