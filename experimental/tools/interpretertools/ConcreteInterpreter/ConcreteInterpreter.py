import copy
from abjad.tools import *
from experimental.tools import library
from experimental.tools import settingtools
from experimental.tools import specificationtools
from experimental.tools.interpretertools.Interpreter import Interpreter


class ConcreteInterpreter(Interpreter):
    r'''Concrete interpreter.

    Currently the only interpreter implemented.

    The name is provisional.
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

    def add_time_signatures_to_score(self):
        while self.score_specification.time_signature_settings[:]:
            for time_signature_setting in self.score_specification.time_signature_settings:
                time_signatures = time_signature_setting.make_time_signatures(self.score_specification)
                if time_signatures:
                    self.score_specification.time_signature_settings.remove(time_signature_setting)
        time_signatures = self.score_specification.time_signatures
        measures = measuretools.make_measures_with_full_measure_spacer_skips(time_signatures)
        context = componenttools.get_first_component_in_expr_with_name(self.score, 'TimeSignatureContext')
        context.extend(measures)

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

    def dump_rhythm_products_into_voices(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_proxy = self.score_specification.contexts[voice.name]
            for rhythm_product in voice_proxy.rhythm_products:
                voice.extend(rhythm_product.payload)

    def get_region_commands_for_voice(self, attribute, voice_name):
        region_commands = self.score_specification.get_region_commands_for_voice(attribute, voice_name)
        region_commands.sort_and_split_commands()
        region_commands.compute_logical_or()
        region_commands.supply_missing_commands(attribute, self.score_specification, voice_name)
        return region_commands

    def interpret_additional_parameters(self):
        pass

    def interpret_divisions(self):
        self.make_region_commands('divisions')
        self.make_division_products()
        self.make_voice_division_lists()

    def interpret_pitch_classes(self):
        pass

    def interpret_registration(self):
        pass

    def interpret_rhythm(self):
        self.make_region_commands('rhythm')
        #self._debug_values(self.score_specification.rhythm_region_commands, 'rhythm region commands')
        self.make_finalized_rhythm_region_commands()
        #self._debug_values(self.score_specification.finalized_rhythm_region_commands, 'finalized rhythm commands')
        self.make_rhythm_products()
        self.dump_rhythm_products_into_voices()

    def interpret_time_signatures(self):
        self.populate_time_signature_settings()
        self.add_time_signatures_to_score()
        self.calculate_score_and_segment_timespans()

    # TODO: structure like self.make_rhythm_products()
    def make_division_products(self):
        redo = True
        while redo:
            redo = False
            made_progress = False
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                voice_proxy = self.score_specification.contexts[voice.name]
                voice_division_region_commands = voice_proxy.division_region_commands
                voice_division_products = voice_proxy.division_products 
                voice_division_region_commands_to_reattempt = []
                for division_region_command in voice_division_region_commands:
                    #self._debug(division_region_command, 'division region command')
                    division_products = division_region_command._evaluate()
                    if division_products is not None:
                        assert isinstance(division_products, list)
                        assert all([isinstance(x, settingtools.VoicedStartPositionedDivisionPayloadExpression) for x in division_products])
                        made_progress = True
                        voice_division_products.extend(division_products)
                    else:
                        voice_division_region_commands_to_reattempt.append(division_region_command)
                        redo = True
                voice_division_region_commands[:] = voice_division_region_commands_to_reattempt[:]
                # sort may have to happen as each adds in, above
                voice_division_products.sort()
            if voice_division_region_commands and not made_progress:
                raise Exception('cyclic division specification.')

    def make_finalized_rhythm_region_commands(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            finalized_rhythm_region_commands = self.make_finalized_rhythm_region_commands_for_voice(voice.name)
            self.score_specification.finalized_rhythm_region_commands.extend(finalized_rhythm_region_commands)

    def make_finalized_rhythm_region_commands_for_voice(self, voice_name):
        voice_proxy = self.score_specification.contexts[voice_name]
        voice_division_list = voice_proxy.voice_division_list
        division_products = voice_proxy.division_products
        rhythm_region_commands = voice_proxy.rhythm_region_commands
        if not voice_division_list:
            return []
        division_region_durations = [x.timespan.duration for x in division_products]
        rhythm_region_command_durations = [x.timespan.duration for x in rhythm_region_commands]
        assert sum(division_region_durations) == sum(rhythm_region_command_durations)
        rhythm_region_command_merged_durations = sequencetools.merge_duration_sequences(
            division_region_durations, rhythm_region_command_durations)
        # assert that rhythm commands cover rhythm regions exactly
        assert sequencetools.partition_sequence_by_weights_exactly(
            rhythm_region_command_merged_durations, rhythm_region_command_durations)
        rhythm_region_start_division_duration_lists = \
                sequencetools.partition_sequence_by_backgrounded_weights(
                voice_division_list.divisions, rhythm_region_command_merged_durations)
        #self._debug_values(rhythm_region_start_division_duration_lists, 'rrsddls')
        assert len(rhythm_region_start_division_duration_lists) == len(rhythm_region_command_merged_durations)
        rhythm_region_start_division_counts = [len(l) for l in rhythm_region_start_division_duration_lists]
        rhythm_region_division_lists = sequencetools.partition_sequence_by_counts(
            voice_division_list.divisions, rhythm_region_start_division_counts, cyclic=False, overhang=False)
        rhythm_region_division_lists = [
            settingtools.DivisionList(x, voice_name=voice_name) for x in rhythm_region_division_lists]
        assert len(rhythm_region_division_lists) == len(rhythm_region_command_merged_durations)
        #self._debug_values(rhythm_region_division_lists, 'rrdls')
        rhythm_region_durations = [x.duration for x in rhythm_region_division_lists]
        #self._debug(rhythm_region_durations, 'rrds')
        cumulative_sums = mathtools.cumulative_sums_zero(rhythm_region_durations)
        rhythm_region_start_offsets = cumulative_sums[:-1]
        rhythm_region_start_offsets = [durationtools.Offset(x) for x in rhythm_region_start_offsets]
        rhythm_region_command_duration_pairs = [(x, x.timespan.duration) for x in rhythm_region_commands]
        #self._debug_values(rhythm_region_command_duration_pairs, 'rhythm command / duration pairs')
        merged_duration_rhythm_region_command_pairs = \
            sequencetools.pair_duration_sequence_elements_with_input_pair_values(
            rhythm_region_command_merged_durations, rhythm_region_command_duration_pairs)
        # the first column in pairs is not used for anything further at all is discarded
        rhythm_region_commands = [x[-1] for x in merged_duration_rhythm_region_command_pairs]
        assert len(rhythm_region_commands) == len(rhythm_region_division_lists)
        finalized_rhythm_region_commands = []
        for rhythm_region_command, rhythm_region_start_offset, rhythm_region_division_list in zip(
            rhythm_region_commands, rhythm_region_start_offsets, rhythm_region_division_lists):
            finalized_rhythm_region_command = rhythm_region_command.finalize(
                self.score_specification, voice_name, rhythm_region_start_offset, rhythm_region_division_list)
            finalized_rhythm_region_commands.append(finalized_rhythm_region_command)
        finalized_rhythm_region_commands = self.merge_prolonging_finalized_rhythm_region_commands(
            finalized_rhythm_region_commands)
        return finalized_rhythm_region_commands

    def make_region_commands(self, attribute):
        if self.score_specification.segment_specifications:
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                voice_proxy = self.score_specification.contexts[voice.name]
                region_commands = self.get_region_commands_for_voice(attribute, voice.name)
                singular_attribute = attribute.rstrip('s')
                key = '{}_region_commands'.format(singular_attribute)
                region_command_inventory = getattr(voice_proxy, key)
                region_command_inventory[:] = region_commands[:]
                score_region_commands = getattr(self.score_specification, key)
                for region_command in region_commands:
                    if region_command not in score_region_commands:
                        score_region_commands.append(region_command)

    def make_rhythm_products(self):
        while self.score_specification.finalized_rhythm_region_commands:
            made_progress = False
            for finalized_rhythm_region_command in self.score_specification.finalized_rhythm_region_commands[:]:
                assert isinstance(finalized_rhythm_region_command, settingtools.FinalizedRhythmRegionExpression)
                rhythm_product = finalized_rhythm_region_command._evaluate()
                if rhythm_product is not None:
                    assert isinstance(rhythm_product, settingtools.VoicedStartPositionedRhythmPayloadExpression)
                    made_progress = True
                    self.score_specification.finalized_rhythm_region_commands.remove(finalized_rhythm_region_command)
                    voice_name = finalized_rhythm_region_command.voice_name
                    voice_proxy = self.score_specification.contexts[voice_name]
                    voice_rhythm_products = voice_proxy.rhythm_products
                    voice_rhythm_products = voice_rhythm_products - rhythm_product.timespan
                    voice_rhythm_products.append(rhythm_product)
                    voice_rhythm_products.sort()
            if not made_progress:
                raise Exception('cyclic rhythm specification.')

    def make_voice_division_lists(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_division_list = settingtools.DivisionList([], voice.name)
            voice_proxy = self.score_specification.contexts[voice.name]
            products = voice_proxy.division_products
            divisions = [x.payload.divisions for x in products]
            divisions = sequencetools.flatten_sequence(divisions, depth=1)
            start_offset = durationtools.Offset(0)
            for division in divisions:
                division = copy.deepcopy(division)
                division._start_offset = durationtools.Offset(start_offset)
                start_offset += division.duration
                voice_division_list.divisions.append(division)
            voice_proxy._voice_division_list = voice_division_list

    def merge_prolonging_finalized_rhythm_region_commands(self, finalized_rhythm_region_commands):
        result = []
        for finalized_rhythm_region_command in finalized_rhythm_region_commands:
            if result and isinstance(finalized_rhythm_region_command, settingtools.SelectorRhythmRegionExpression) and \
                finalized_rhythm_region_command.prolongs_expr(result[-1]):
                current_stop_offset = finalized_rhythm_region_command.start_offset
                current_stop_offset += finalized_rhythm_region_command.total_duration
                previous_stop_offset = result[-1].start_offset + result[-1].total_duration
                extra_duration = current_stop_offset - previous_stop_offset
                assert 0 <= extra_duration
                result[-1]._total_duration += extra_duration
            else:
                result.append(finalized_rhythm_region_command)
        return result

    # TODO: eventually merge with self.make_region_commands()
    def populate_time_signature_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            time_signature_settings = \
                segment_specification.single_context_settings_by_context.score_context_proxy.get_settings(
                attribute='time_signatures')
            if not time_signature_settings:
                continue
            time_signature_setting = time_signature_settings[-1]
            self.score_specification.time_signature_settings.append(time_signature_setting)

    def store_interpreter_specific_single_context_settings_by_context(self):
        self.store_single_context_attribute_settings_by_context('time_signatures')
        self.store_single_context_attribute_settings_by_context('divisions')
        self.store_single_context_attribute_settings_by_context('rhythm')
        self.store_single_context_attribute_settings_by_context('pitch_classes')
        self.store_single_context_attribute_settings_by_context('registration')
