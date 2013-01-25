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

    def get_timespan_scoped_single_context_settings_for_voice(self, attribute, voice_name):
        settings = self.score_specification.get_timespan_scoped_single_context_settings_for_voice(
            attribute, voice_name)
        settings.sort_and_split_settings()
        settings.compute_logical_or()
        settings.supply_missing_settings(attribute, self.score_specification, voice_name)
        return settings

    def interpret_additional_parameters(self):
        pass

    def interpret_divisions(self):
        self.make_timespan_scoped_single_context_settings('divisions')
        self.make_division_products()
        self.make_voice_division_lists()

    def interpret_pitch_classes(self):
        pass

    def interpret_registration(self):
        pass

    def interpret_rhythm(self):
        self.make_timespan_scoped_single_context_settings('rhythm')
        #self._debug_values(self.score_specification.timespan_scoped_single_context_rhythm_settings, 'rhythm region commands')
        self.make_rhythm_region_expressions()
        #self._debug_values(self.score_specification.rhythm_region_expressions, 'finalized rhythm commands')
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
                voice_timespan_scoped_single_context_division_settings = voice_proxy.timespan_scoped_single_context_division_settings
                voice_division_products = voice_proxy.division_products 
                voice_timespan_scoped_single_context_division_settings_to_reattempt = []
                for timespan_scoped_single_context_division_setting in voice_timespan_scoped_single_context_division_settings:
                    division_product = timespan_scoped_single_context_division_setting._evaluate()
                    if division_product is not None:
                        assert isinstance(division_product, settingtools.StartPositionedDivisionPayloadExpression)
                        made_progress = True
                        voice_division_products.append(division_product)
                    else:
                        voice_timespan_scoped_single_context_division_settings_to_reattempt.append(timespan_scoped_single_context_division_setting)
                        redo = True
                voice_timespan_scoped_single_context_division_settings[:] = voice_timespan_scoped_single_context_division_settings_to_reattempt[:]
                # sort may have to happen as each adds in, above
                voice_division_products.sort()
            if voice_timespan_scoped_single_context_division_settings and not made_progress:
                raise Exception('cyclic division specification.')

    def make_rhythm_region_expressions(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            rhythm_region_expressions = self.make_rhythm_region_expressions_for_voice(voice.name)
            self.score_specification.rhythm_region_expressions.extend(rhythm_region_expressions)

    def make_rhythm_region_expressions_for_voice(self, voice_name):
        voice_proxy = self.score_specification.contexts[voice_name]
        voice_division_list = voice_proxy.voice_division_list
        division_products = voice_proxy.division_products
        timespan_scoped_single_context_rhythm_settings = voice_proxy.timespan_scoped_single_context_rhythm_settings
        if not voice_division_list:
            return []
        division_region_durations = [x.timespan.duration for x in division_products]
        timespan_scoped_single_context_rhythm_setting_durations = [x.timespan.duration for x in timespan_scoped_single_context_rhythm_settings]
        assert sum(division_region_durations) == sum(timespan_scoped_single_context_rhythm_setting_durations)
        timespan_scoped_single_context_rhythm_setting_merged_durations = sequencetools.merge_duration_sequences(
            division_region_durations, timespan_scoped_single_context_rhythm_setting_durations)
        # assert that rhythm commands cover rhythm regions exactly
        assert sequencetools.partition_sequence_by_weights_exactly(
            timespan_scoped_single_context_rhythm_setting_merged_durations, timespan_scoped_single_context_rhythm_setting_durations)
        rhythm_region_start_division_duration_lists = \
                sequencetools.partition_sequence_by_backgrounded_weights(
                voice_division_list.divisions, timespan_scoped_single_context_rhythm_setting_merged_durations)
        #self._debug_values(rhythm_region_start_division_duration_lists, 'rrsddls')
        assert len(rhythm_region_start_division_duration_lists) == len(timespan_scoped_single_context_rhythm_setting_merged_durations)
        rhythm_region_start_division_counts = [len(l) for l in rhythm_region_start_division_duration_lists]
        rhythm_region_division_lists = sequencetools.partition_sequence_by_counts(
            voice_division_list.divisions, rhythm_region_start_division_counts, cyclic=False, overhang=False)
        rhythm_region_division_lists = [
            settingtools.DivisionList(x, voice_name=voice_name) for x in rhythm_region_division_lists]
        assert len(rhythm_region_division_lists) == len(timespan_scoped_single_context_rhythm_setting_merged_durations)
        #self._debug_values(rhythm_region_division_lists, 'rrdls')
        rhythm_region_durations = [x.duration for x in rhythm_region_division_lists]
        #self._debug(rhythm_region_durations, 'rrds')
        cumulative_sums = mathtools.cumulative_sums_zero(rhythm_region_durations)
        rhythm_region_start_offsets = cumulative_sums[:-1]
        rhythm_region_start_offsets = [durationtools.Offset(x) for x in rhythm_region_start_offsets]
        timespan_scoped_single_context_rhythm_setting_duration_pairs = [(x, x.timespan.duration) for x in timespan_scoped_single_context_rhythm_settings]
        #self._debug_values(timespan_scoped_single_context_rhythm_setting_duration_pairs, 'rhythm command / duration pairs')
        merged_duration_timespan_scoped_single_context_rhythm_setting_pairs = \
            sequencetools.pair_duration_sequence_elements_with_input_pair_values(
            timespan_scoped_single_context_rhythm_setting_merged_durations, timespan_scoped_single_context_rhythm_setting_duration_pairs)
        # the first column in pairs is not used for anything further at all is discarded
        timespan_scoped_single_context_rhythm_settings = [x[-1] for x in merged_duration_timespan_scoped_single_context_rhythm_setting_pairs]
        assert len(timespan_scoped_single_context_rhythm_settings) == len(rhythm_region_division_lists)
        rhythm_region_expressions = []
        for timespan_scoped_single_context_rhythm_setting, rhythm_region_start_offset, rhythm_region_division_list in zip(
            timespan_scoped_single_context_rhythm_settings, rhythm_region_start_offsets, rhythm_region_division_lists):
            rhythm_region_expression = timespan_scoped_single_context_rhythm_setting.finalize(
                self.score_specification, voice_name, rhythm_region_start_offset, rhythm_region_division_list)
            rhythm_region_expressions.append(rhythm_region_expression)
        rhythm_region_expressions = self.merge_prolonging_rhythm_region_expressions(
            rhythm_region_expressions)
        return rhythm_region_expressions

    def make_timespan_scoped_single_context_settings(self, attribute):
        if self.score_specification.segment_specifications:
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                voice_proxy = self.score_specification.contexts[voice.name]
                region_expressions = self.get_timespan_scoped_single_context_settings_for_voice(attribute, voice.name)
                singular_attribute = attribute.rstrip('s')
                key = 'timespan_scoped_single_context_{}_settings'.format(singular_attribute)
                region_expression_inventory = getattr(voice_proxy, key)
                region_expression_inventory[:] = region_expressions[:]
                score_region_expressions = getattr(self.score_specification, key)
                for region_expression in region_expressions:
                    if region_expression not in score_region_expressions:
                        score_region_expressions.append(region_expression)

    def make_rhythm_products(self):
        while self.score_specification.rhythm_region_expressions:
            made_progress = False
            for rhythm_region_expression in self.score_specification.rhythm_region_expressions[:]:
                assert isinstance(rhythm_region_expression, settingtools.FinalizedRhythmRegionExpression)
                rhythm_product = rhythm_region_expression._evaluate()
                if rhythm_product is not None:
                    assert isinstance(rhythm_product, settingtools.StartPositionedRhythmPayloadExpression)
                    made_progress = True
                    self.score_specification.rhythm_region_expressions.remove(rhythm_region_expression)
                    voice_name = rhythm_region_expression.voice_name
                    voice_proxy = self.score_specification.contexts[voice_name]
                    voice_rhythm_products = voice_proxy.rhythm_products
                    voice_rhythm_products = voice_rhythm_products - rhythm_product.timespan
                    voice_rhythm_products.append(rhythm_product)
                    voice_rhythm_products.sort()
            if not made_progress:
                raise Exception('cyclic rhythm specification.')

    def make_voice_division_lists(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_division_list = settingtools.DivisionList([], voice_name=voice.name)
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

    def merge_prolonging_rhythm_region_expressions(self, rhythm_region_expressions):
        result = []
        for rhythm_region_expression in rhythm_region_expressions:
            if result and isinstance(rhythm_region_expression, settingtools.SelectExpressionRhythmRegionExpression) and \
                rhythm_region_expression.prolongs_expr(result[-1]):
                current_stop_offset = rhythm_region_expression.start_offset
                current_stop_offset += rhythm_region_expression.total_duration
                previous_stop_offset = result[-1].start_offset + result[-1].total_duration
                extra_duration = current_stop_offset - previous_stop_offset
                assert 0 <= extra_duration
                result[-1]._total_duration += extra_duration
            else:
                result.append(rhythm_region_expression)
        return result

    # TODO: eventually merge with self.make_timespan_scoped_single_context_settings()
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
