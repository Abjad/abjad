import copy
from abjad.tools import *
from experimental.tools import library
from experimental.tools import expressiontools
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

    def add_division_lists_to_score(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_division_list = expressiontools.DivisionList([], voice_name=voice.name)
            voice_proxy = self.score_specification.contexts[voice.name]
            expressions = voice_proxy.division_payload_expressions
            divisions = [x.payload.divisions for x in expressions]
            divisions = sequencetools.flatten_sequence(divisions, depth=1)
            start_offset = durationtools.Offset(0)
            for division in divisions:
                division = copy.deepcopy(division)
                division._start_offset = durationtools.Offset(start_offset)
                start_offset += division.duration
                voice_division_list.divisions.append(division)
            voice_proxy._voice_division_list = voice_division_list

    def add_rhythms_to_score(self):
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            voice_proxy = self.score_specification.contexts[voice.name]
            for rhythm_payload_expression in voice_proxy.rhythm_payload_expressions:
                voice.extend(rhythm_payload_expression.payload)

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

    def get_timespan_scoped_single_context_set_expressions_for_voice(self, attribute, voice_name):
        set_expressions = self.score_specification.get_timespan_scoped_single_context_set_expressions_for_voice(
            attribute, voice_name)
        set_expressions.sort_and_split_set_expressions()
        set_expressions.compute_logical_or()
        set_expressions.supply_missing_set_expressions(attribute, self.score_specification, voice_name)
        return set_expressions

    def interpret_additional_parameters(self):
        pass

    def interpret_divisions(self):
        self.make_timespan_scoped_single_context_set_expressions('divisions')
        self.make_region_expressions('divisions')
        self.make_payload_expressions('divisions')
        self.add_division_lists_to_score()

    def interpret_pitch_classes(self):
        pass

    def interpret_registration(self):
        pass

    def interpret_rhythm(self):
        self.make_timespan_scoped_single_context_set_expressions('rhythm')
        self.make_region_expressions('rhythm')
        self.make_payload_expressions('rhythm')
        self.add_rhythms_to_score()

    def interpret_time_signatures(self):
        self.populate_time_signature_settings()
        self.add_time_signatures_to_score()
        self.calculate_score_and_segment_timespans()

    def make_division_region_expressions_for_voice(self, voice_name):
        voice_proxy = self.score_specification.contexts[voice_name]
        set_expressions = voice_proxy.timespan_scoped_single_context_division_set_expressions[:]
        region_expressions = []
        for set_expression in set_expressions:
            region_expression = set_expression.evaluate(voice_name)
            region_expressions.append(region_expression)
        return region_expressions

    def make_payload_expressions(self, attribute):
        attribute = attribute.rstrip('s')
        region_expression_key = '{}_region_expressions'.format(attribute)
        payload_expression_key = '{}_payload_expressions'.format(attribute)
        score_region_expressions = getattr(self.score_specification, region_expression_key)
        while score_region_expressions:
            made_progress = False
            for region_expression in getattr(self.score_specification, region_expression_key)[:]:
                assert isinstance(region_expression, expressiontools.RegionExpression)
                payload_expression = region_expression.evaluate()
                if payload_expression is not None:
                    assert isinstance(payload_expression, expressiontools.StartPositionedPayloadExpression)
                    made_progress = True
                    score_region_expressions.remove(region_expression)
                    voice_name = region_expression.voice_name
                    voice_proxy = self.score_specification.contexts[voice_name]
                    voice_payload_expressions = getattr(voice_proxy, payload_expression_key)
                    voice_payload_expressions = voice_payload_expressions - payload_expression.timespan
                    voice_payload_expressions.append(payload_expression)
                    voice_payload_expressions.sort()
            if not made_progress:
                raise Exception('cyclic specification.')

    def make_region_expressions(self, attribute):
        attribute = attribute.rstrip('s')
        method_key = 'make_{}_region_expressions_for_voice'.format(attribute)
        score_region_expressions_key = '{}_region_expressions'.format(attribute)
        score_region_expressions = getattr(self.score_specification, score_region_expressions_key)
        for voice in iterationtools.iterate_voices_in_expr(self.score):
            region_expressions = getattr(self, method_key)(voice.name)
            score_region_expressions.extend(region_expressions)

    def make_rhythm_region_expressions_for_voice(self, voice_name):
        voice_proxy = self.score_specification.contexts[voice_name]
        voice_division_list = voice_proxy.voice_division_list
        division_payload_expressions = voice_proxy.division_payload_expressions
        timespan_scoped_single_context_rhythm_set_expressions = \
            voice_proxy.timespan_scoped_single_context_rhythm_set_expressions
        if not voice_division_list:
            return []
        division_region_durations = [x.timespan.duration for x in division_payload_expressions]
        timespan_scoped_single_context_rhythm_set_expression_durations = [
            x.target_timespan.duration for x in timespan_scoped_single_context_rhythm_set_expressions]
        assert sum(division_region_durations) == sum(timespan_scoped_single_context_rhythm_set_expression_durations)
        timespan_scoped_single_context_rhythm_set_expression_merged_durations = sequencetools.merge_duration_sequences(
            division_region_durations, timespan_scoped_single_context_rhythm_set_expression_durations)
        # assert that rhythm commands cover rhythm regions exactly
        assert sequencetools.partition_sequence_by_weights_exactly(
            timespan_scoped_single_context_rhythm_set_expression_merged_durations, 
            timespan_scoped_single_context_rhythm_set_expression_durations)
        rhythm_region_start_division_duration_lists = \
                sequencetools.partition_sequence_by_backgrounded_weights(
                voice_division_list.divisions, timespan_scoped_single_context_rhythm_set_expression_merged_durations)
        #self._debug_values(rhythm_region_start_division_duration_lists, 'rrsddls')
        assert len(rhythm_region_start_division_duration_lists) == \
            len(timespan_scoped_single_context_rhythm_set_expression_merged_durations)
        rhythm_region_start_division_counts = [len(l) for l in rhythm_region_start_division_duration_lists]
        rhythm_region_division_lists = sequencetools.partition_sequence_by_counts(
            voice_division_list.divisions, rhythm_region_start_division_counts, cyclic=False, overhang=False)
        rhythm_region_division_lists = [
            expressiontools.DivisionList(x, voice_name=voice_name) for x in rhythm_region_division_lists]
        assert len(rhythm_region_division_lists) == \
            len(timespan_scoped_single_context_rhythm_set_expression_merged_durations)
        #self._debug_values(rhythm_region_division_lists, 'rrdls')
        rhythm_region_durations = [x.duration for x in rhythm_region_division_lists]
        #self._debug(rhythm_region_durations, 'rrds')
        cumulative_sums = mathtools.cumulative_sums_zero(rhythm_region_durations)
        rhythm_region_start_offsets = cumulative_sums[:-1]
        rhythm_region_start_offsets = [durationtools.Offset(x) for x in rhythm_region_start_offsets]
        timespan_scoped_single_context_rhythm_set_expression_duration_pairs = [
            (x, x.target_timespan.duration) for x in timespan_scoped_single_context_rhythm_set_expressions]
        #self._debug_values(timespan_scoped_single_context_rhythm_set_expression_duration_pairs, 
        #    'rhythm command / duration pairs')
        merged_duration_timespan_scoped_single_context_rhythm_set_expression_pairs = \
            sequencetools.pair_duration_sequence_elements_with_input_pair_values(
            timespan_scoped_single_context_rhythm_set_expression_merged_durations, 
            timespan_scoped_single_context_rhythm_set_expression_duration_pairs)
        # the first column in pairs is not used for anything further at all is discarded
        timespan_scoped_single_context_rhythm_set_expressions = [
            x[-1] for x in merged_duration_timespan_scoped_single_context_rhythm_set_expression_pairs]
        assert len(timespan_scoped_single_context_rhythm_set_expressions) == len(rhythm_region_division_lists)
        rhythm_region_expressions = []
        for timespan_scoped_single_context_rhythm_set_expression, rhythm_region_start_offset, rhythm_region_division_list in zip(
            timespan_scoped_single_context_rhythm_set_expressions, rhythm_region_start_offsets, rhythm_region_division_lists):
            rhythm_region_expression = timespan_scoped_single_context_rhythm_set_expression.evaluate(
                rhythm_region_division_list, rhythm_region_start_offset, voice_name)
            rhythm_region_expressions.append(rhythm_region_expression)
        rhythm_region_expressions = self.merge_prolonging_rhythm_region_expressions(
            rhythm_region_expressions)
        return rhythm_region_expressions

    def make_timespan_scoped_single_context_set_expressions(self, attribute):
        if self.score_specification.segment_specifications:
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                voice_proxy = self.score_specification.contexts[voice.name]
                set_expressions = self.get_timespan_scoped_single_context_set_expressions_for_voice(
                    attribute, voice.name)
                singular_attribute = attribute.rstrip('s')
                key = 'timespan_scoped_single_context_{}_set_expressions'.format(singular_attribute)
                inventory = getattr(voice_proxy, key)
                inventory[:] = set_expressions[:]
                score_set_expressions = getattr(self.score_specification, key)
                for set_expression in set_expressions:
                    if set_expression not in score_set_expressions:
                        score_set_expressions.append(set_expression)

    def merge_prolonging_rhythm_region_expressions(self, rhythm_region_expressions):
        result = []
        for rhythm_region_expression in rhythm_region_expressions:
            if result and isinstance(
                rhythm_region_expression, expressiontools.SelectExpressionRhythmRegionExpression) and \
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

    # TODO: eventually merge with self.make_timespan_scoped_single_context_set_expressions()
    def populate_time_signature_settings(self):
        for segment_specification in self.score_specification.segment_specifications:
            score_proxy = segment_specification.single_context_set_expressions_by_context.score_context_proxy
            time_signature_settings = score_proxy.get_set_expressions(attribute='time_signatures')
            if not time_signature_settings:
                continue
            time_signature_setting = time_signature_settings[-1]
            self.score_specification.time_signature_settings.append(time_signature_setting)

    def store_interpreter_specific_single_context_set_expressions_by_context(self):
        self.store_single_context_attribute_set_expressions_by_context('time_signatures')
        self.store_single_context_attribute_set_expressions_by_context('divisions')
        self.store_single_context_attribute_set_expressions_by_context('rhythm')
        self.store_single_context_attribute_set_expressions_by_context('pitch_classes')
        self.store_single_context_attribute_set_expressions_by_context('registration')
