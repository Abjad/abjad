# -*- encoding: utf-8 -*-
import copy
import time
from abjad.tools import *
from abjad.tools.topleveltools import iterate
from experimental.tools.musicexpressiontools.Interpreter import Interpreter


class ConcreteInterpreter(Interpreter):
    r'''Concrete interpreter.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, score_specification):
        r'''Interpret `score_specification`:

            * interpret all time signatures scorewide
            * interpret all divisions scorewide
            * interpret rhythm scorewide
            * interpret additional parameters.

        Returns Abjad score object.
        '''
        from experimental.tools import musicexpressiontools
        start_time = time.time()
        Interpreter.__call__(self, score_specification)
        self.interpret_time_signatures()
        self.interpret_divisions()
        self.interpret_rhythm()
        self.interpret_additional_parameters()
        stop_time = time.time()
        total_time = stop_time - start_time
        if 2 <= total_time:
            message = 'Abjad interpretation time equal to {} seconds ...'
            print(message.format(int(total_time)))
        return self.score

    ### PRIVATE METHODS ###

    @staticmethod
    def _merge_duration_sequences(*sequences):
        r'''Merges duration `sequences`.

        ::

            >>> interpreter = musicexpressiontools.ConcreteInterpreter

        ::

            >>> interpreter._merge_duration_sequences([10, 10, 10], [7])
            [7, 3, 10, 10]

        Merges more duration sequences:

        ::

            >>> interpreter._merge_duration_sequences([10, 10, 10], [10, 10])
            [10, 10, 10]

        The idea is that each sequence element represents a duration.

        Returns list.
        '''
        offset_lists = []
        for sequence in sequences:
            offset_list = mathtools.cumulative_sums(sequence, start=None)
            offset_lists.append(offset_list)
        all_offsets = sequencetools.join_subsequences(offset_lists)
        all_offsets = list(sorted(set(all_offsets)))
        all_offsets.insert(0, 0)
        all_durations = mathtools.difference_series(all_offsets)
        return all_durations

    @staticmethod
    def _pair_duration_sequence_elements_with_input_pair_values(
        duration_sequence,
        input_pairs,
        ):
        r'''Pairs `duration_sequence` elements with the values of
        `input_pairs`.

        ::

            >>> from experimental import *

        ::

            >>> duration_sequence = [10, 10, 10, 10]
            >>> input_pairs = [('red', 1), ('orange', 18), ('yellow', 200)]

        ::

            >>> interpreter = musicexpressiontools.ConcreteInterpreter
            >>> interpreter._pair_duration_sequence_elements_with_input_pair_values(
            ... duration_sequence, input_pairs)
            [(10, 'red'), (10, 'orange'), (10, 'yellow'), (10, 'yellow')]

        Returns a list of ``(element, value)`` output pairs.

        The `input_pairs` argument must be a list of ``(value, duration)`` pairs.

        The basic idea behind the function is model which input pair
        value is in effect at the start of each element in `duration_sequence`.
        '''
        from abjad.tools import sequencetools

        assert mathtools.all_are_numbers(duration_sequence)
        assert mathtools.all_are_pairs(input_pairs)

        output_pairs = []
        current_element_start = 0
        current_input_pair_index = 0
        current_input_pair = input_pairs[current_input_pair_index]
        current_input_pair_value = current_input_pair[0]
        current_input_pair_duration = current_input_pair[-1]
        current_input_pair_start = 0
        current_input_pair_stop = \
            current_input_pair_start + current_input_pair_duration

        for element in duration_sequence:
            while current_input_pair_stop <= current_element_start:
                current_input_pair_index += 1
                current_input_pair = input_pairs[current_input_pair_index]
                current_input_pair_value = current_input_pair[0]
                current_input_pair_duration = current_input_pair[-1]
                current_input_pair_start = current_input_pair_stop
                current_input_pair_stop += current_input_pair_duration
            output_pair = (element, current_input_pair_value)
            output_pairs.append(output_pair)
            current_element_start += element

        return output_pairs

    @staticmethod
    def _partition_sequence_by_backgrounded_weights(sequence, weights):
        r'''Partitions `sequence` by backgrounded `weights`.

        ::

            >>> interpreter = musicexpressiontools.ConcreteInterpreter

        ::

            >>> interpreter._partition_sequence_by_backgrounded_weights(
            ...     [-5, -15, -10], [20, 10])
            [[-5, -15], [-10]]

        Further examples:

        ::

            >>> interpreter._partition_sequence_by_backgrounded_weights(
            ...     [-5, -15, -10], [5, 5, 5, 5, 5, 5])
            [[-5], [-15], [], [], [-10], []]

        ::

            >>> interpreter._partition_sequence_by_backgrounded_weights(
            ...     [-5, -15, -10], [1, 29])
            [[-5], [-15, -10]]

        ::

            >>> interpreter._partition_sequence_by_backgrounded_weights(
            ...     [-5, -15, -10], [2, 28])
            [[-5], [-15, -10]]

        ::

            >>> interpreter._partition_sequence_by_backgrounded_weights(
            ...     [-5, -15, -10], [1, 1, 1, 1, 1, 25])
            [[-5], [], [], [], [], [-15, -10]]

        The term `backgrounded` is a short-hand concocted specifically
        for this function; rely on the formal definition to understand
        the function actually does.

        Input constraint: the weight of `sequence` must equal the weight
        of `weights` exactly.

        The signs of the elements in `sequence` are ignored.

        Formal definition: partition `sequence` into `parts` such that
        (1.) the length of `parts` equals the length of `weights`;
        (2.) the elements in `sequence` appear in order in `parts`; and
        (3.) some final condition that is difficult to formalize.

        Notionally what's going on here is that the elements of `weights`
        are acting as a list of successive time intervals into which the
        elements of `sequence` are being fit in accordance with the start
        offset of each `sequence` element.

        The function models the grouping together of successive timespans
        according to which of an underlying sequence of time intervals
        it is in which each time span begins.

        Note that, for any input to this function, the flattened output
        of this function always equals `sequence` exactly.

        Note too that while `partition` is being used here in the sense of
        the other partitioning functions in the API, the distinguishing feature
        is this funciton is its ability to produce empty lists as output.

        Returns list of `sequence` objects.
        '''
        assert all(0 < x for x in weights)
        assert mathtools.weight(sequence) == mathtools.weight(weights)
        start_offsets = \
            mathtools.cumulative_sums([abs(x) for x in sequence])[:-1]
        token = zip(start_offsets, sequence)
        result = []
        for interval_start, interval_stop in \
            mathtools.cumulative_sums_pairwise(weights):
            part = []
            for pair in token[:]:
                if interval_start <= pair[0] < interval_stop:
                    part.append(pair[1])
                    token.remove(pair)
            result.append(part)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def leaf_offset_lists_by_voice(self):
        return self._leaf_offset_lists_by_voice

    ### PUBLIC METHODS ###

    def add_division_lists_to_score(self):
        from experimental.tools import musicexpressiontools
        for voice in iterate(self.score).by_class(scoretools.Voice):
            voice_division_list = \
                musicexpressiontools.DivisionList([], voice_name=voice.name)
            voice_proxy = \
                self.score_specification.voice_data_structures_by_voice[
                    voice.name]
            expressions = \
                voice_proxy.payload_expressions_by_attribute['divisions']
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
        for voice in iterate(self.score).by_class(scoretools.Voice):
            voice_proxy = \
                self.score_specification.voice_data_structures_by_voice[
                    voice.name]
            for rhythm_payload_expression in \
                voice_proxy.payload_expressions_by_attribute['rhythm']:
                voice.extend(rhythm_payload_expression.payload)

    def add_time_signatures_to_score(self):
        single_context_time_signature_set_expressions = \
            self.score_specification.single_context_time_signature_set_expressions[:]
        while single_context_time_signature_set_expressions:
            for single_context_time_signature_set_expression in \
                single_context_time_signature_set_expressions[:]:
                time_signatures = \
                    single_context_time_signature_set_expression.make_time_signatures()
                if time_signatures:
                    single_context_time_signature_set_expressions.remove(
                        single_context_time_signature_set_expression)
        time_signatures = self.score_specification.time_signatures
        measures = scoretools.make_spacer_skip_measures(
            time_signatures)
        context = self.score['TimeSignatureContext']
        context.extend(measures)

    def build_leaf_offset_lists(self):
        for voice in iterate(self.score).by_class(scoretools.Voice):
            voice_proxy = \
                self.score_specification.voice_data_structures_by_voice[
                    voice.name]
            for leaf in iterate(voice).by_class(scoretools.Leaf):
                voice_proxy.leaf_start_offsets.append(
                    leaf._get_timespan().start_offset)
                voice_proxy.leaf_stop_offsets.append(
                    leaf._get_timespan().stop_offset)
                voice_proxy.leaves.append(leaf)

    def calculate_score_and_segment_timespans(self):
        if hasattr(self.score_specification, '_time_signatures'):
            time_signatures = self.score_specification.time_signatures
            score_duration = sum(
                [durationtools.Duration(x) for x in time_signatures])
            score_start_offset = durationtools.Offset(0)
            score_stop_offset = durationtools.Offset(score_duration)
            self.score_specification._start_offset = \
                durationtools.Offset(0)
            self.score_specification._stop_offset = \
                durationtools.Offset(score_duration)
            score_timespan = \
                timespantools.Timespan(score_start_offset, score_stop_offset)
            self.score_specification._timespan = score_timespan
        else:
            segment_durations = [
                durationtools.Duration(sum(x.time_signatures))
                for x in self.score_specification.segment_specifications]
            assert mathtools.all_are_numbers(segment_durations)
            score_duration = sum(segment_durations)
            score_start_offset = durationtools.Offset(0)
            score_stop_offset = durationtools.Offset(score_duration)
            self.score_specification._start_offset = durationtools.Offset(0)
            self.score_specification._stop_offset = \
                durationtools.Offset(score_duration)
            score_timespan = \
                timespantools.Timespan(score_start_offset, score_stop_offset)
            self.score_specification._timespan = score_timespan
            segment_offset_pairs = \
                mathtools.cumulative_sums_pairwise(segment_durations)
            segment_offset_pairs = [
                (durationtools.Offset(x[0]), durationtools.Offset(x[1]))
                for x in segment_offset_pairs]
            for segment_offset_pair, segment_specification in zip(
                segment_offset_pairs,
                self.score_specification.segment_specifications):
                start_offset, stop_offset = segment_offset_pair
                segment_specification._start_offset = start_offset
                segment_specification._stop_offset = stop_offset
                timespan = timespantools.Timespan(start_offset, stop_offset)
                segment_specification._timespan = timespan

    def interpret_additional_parameters(self):
        for leaf_set_expression in \
            self.score_specification.postrhythm_set_expressions:
            leaf_set_expression.execute_against_score(self.score)

    def interpret_divisions(self):
        self.make_timespan_delimited_single_context_set_expressions('divisions')
        self.make_region_expressions('divisions')
        self.make_payload_expressions('divisions')
        self.add_division_lists_to_score()

    def interpret_rhythm(self):
        self.make_timespan_delimited_single_context_set_expressions('rhythm')
        self.make_region_expressions('rhythm')
        self.make_payload_expressions('rhythm')
        self.add_rhythms_to_score()
        self.build_leaf_offset_lists()

    def interpret_time_signatures(self):
        self.populate_single_context_time_signature_set_expressions()
        self.add_time_signatures_to_score()
        self.calculate_score_and_segment_timespans()

    def make_division_region_expressions_for_voice(self, voice_name):
        voice_proxy = \
            self.score_specification.single_context_set_expressions_by_context[
                voice_name]
        set_expressions = \
            voice_proxy.timespan_delimited_single_context_set_expressions_by_attribute[
                'divisions'][:]
        region_expressions = []
        for set_expression in set_expressions:
            region_expression = set_expression.evaluate(voice_name)
            region_expressions.append(region_expression)
        return region_expressions

    def make_payload_expressions(self, attribute):
        from experimental.tools import musicexpressiontools
        region_expressions = \
            self.score_specification.region_expressions_by_attribute[
                attribute][:]
        while region_expressions:
            made_progress = False
            for region_expression in region_expressions[:]:
                assert isinstance(
                    region_expression, musicexpressiontools.RegionExpression)
                payload_expression = region_expression.evaluate()
                if payload_expression is not None:
                    assert isinstance(
                        payload_expression,
                        musicexpressiontools.StartPositionedPayloadExpression)
                    made_progress = True
                    region_expressions.remove(region_expression)
                    voice_name = region_expression.voice_name
                    voice_proxy = \
                        self.score_specification.voice_data_structures_by_voice[
                            voice_name]
                    voice_payload_expressions = \
                        voice_proxy.payload_expressions_by_attribute[attribute]
                    voice_payload_expressions = \
                        voice_payload_expressions - payload_expression.timespan
                    voice_payload_expressions.append(payload_expression)
                    voice_payload_expressions.sort()
            if not made_progress:
                raise Exception('cyclic specification.')

    def make_region_expressions(self, attribute):
        region_expressions = \
            self.score_specification.region_expressions_by_attribute[
                attribute]
        for voice in iterate(self.score).by_class(scoretools.Voice):
            if attribute == 'divisions':
                voice_region_expressions = \
                    self.make_division_region_expressions_for_voice(voice.name)
            elif attribute == 'rhythm':
                voice_region_expressions = \
                    self.make_rhythm_region_expressions_for_voice(voice.name)
            else:
                raise ValueError(attribute)
            region_expressions.extend(voice_region_expressions)

    def make_rhythm_region_expressions_for_voice(self, voice_name):
        from experimental.tools import musicexpressiontools
        voice_proxy = \
            self.score_specification.voice_data_structures_by_voice[voice_name]
        division_payload_expressions = \
            voice_proxy.payload_expressions_by_attribute['divisions']
        voice_proxy = \
            self.score_specification.single_context_set_expressions_by_context[voice_name]
        expressions = \
            voice_proxy.timespan_delimited_single_context_set_expressions_by_attribute['rhythm']
        timespan_delimited_single_context_rhythm_set_expressions = expressions
        voice_proxy = \
            self.score_specification.voice_data_structures_by_voice[voice_name]
        voice_division_list = voice_proxy.voice_division_list
        if not voice_division_list:
            return []
        division_region_durations = \
            [x.timespan.duration for x in division_payload_expressions]
        timespan_delimited_single_context_rhythm_set_expression_durations = [
            x.target_timespan.duration
            for x in timespan_delimited_single_context_rhythm_set_expressions]
        assert sum(division_region_durations) == \
            sum(timespan_delimited_single_context_rhythm_set_expression_durations)
        timespan_delimited_single_context_rhythm_set_expression_merged_durations = \
            self._merge_duration_sequences(
                division_region_durations,
                timespan_delimited_single_context_rhythm_set_expression_durations)
        # assert that rhythm set expressions cover rhythm regions exactly
        assert sequencetools.partition_sequence_by_weights(
            timespan_delimited_single_context_rhythm_set_expression_merged_durations,
            timespan_delimited_single_context_rhythm_set_expression_durations)
        rhythm_region_start_division_duration_lists = \
                self._partition_sequence_by_backgrounded_weights(
                voice_division_list.divisions,
                timespan_delimited_single_context_rhythm_set_expression_merged_durations)
        #self._debug_values(rhythm_region_start_division_duration_lists, 'rrsddls')
        assert len(rhythm_region_start_division_duration_lists) == \
            len(timespan_delimited_single_context_rhythm_set_expression_merged_durations)
        rhythm_region_start_division_counts = \
            [len(l) for l in rhythm_region_start_division_duration_lists]
        rhythm_region_division_lists = \
            sequencetools.partition_sequence_by_counts(
            voice_division_list.divisions,
            rhythm_region_start_division_counts,
            cyclic=False,
            overhang=False)
        rhythm_region_division_lists = [
            musicexpressiontools.DivisionList(x, voice_name=voice_name)
            for x in rhythm_region_division_lists]
        assert len(rhythm_region_division_lists) == \
            len(timespan_delimited_single_context_rhythm_set_expression_merged_durations)
        #self._debug_values(rhythm_region_division_lists, 'rrdls')
        rhythm_region_durations = \
            [x.duration for x in rhythm_region_division_lists]
        #self._debug(rhythm_region_durations, 'rrds')
        cumulative_sums = \
            mathtools.cumulative_sums(rhythm_region_durations)
        rhythm_region_start_offsets = cumulative_sums[:-1]
        rhythm_region_start_offsets = \
            [durationtools.Offset(x) for x in rhythm_region_start_offsets]
        timespan_delimited_single_context_rhythm_set_expression_duration_pairs = [
            (x, x.target_timespan.duration)
            for x in timespan_delimited_single_context_rhythm_set_expressions]
        #self._debug_values(timespan_delimited_single_context_rhythm_set_expression_duration_pairs,
        #    'rhythm expression / duration pairs')
        merged_duration_timespan_delimited_single_context_rhythm_set_expression_pairs = \
            self._pair_duration_sequence_elements_with_input_pair_values(
            timespan_delimited_single_context_rhythm_set_expression_merged_durations,
            timespan_delimited_single_context_rhythm_set_expression_duration_pairs)
        # the first column in pairs is not used for anything further at all is discarded
        timespan_delimited_single_context_rhythm_set_expressions = [
            x[-1] for x in merged_duration_timespan_delimited_single_context_rhythm_set_expression_pairs]
        assert len(timespan_delimited_single_context_rhythm_set_expressions) == \
            len(rhythm_region_division_lists)
        rhythm_region_expressions = []
        for timespan_delimited_single_context_rhythm_set_expression, \
            rhythm_region_start_offset, rhythm_region_division_list in zip(
            timespan_delimited_single_context_rhythm_set_expressions,
            rhythm_region_start_offsets, rhythm_region_division_lists):
            #self._debug(timespan_delimited_single_context_rhythm_set_expression, 'tsscrsx')
            rhythm_region_expression = \
                timespan_delimited_single_context_rhythm_set_expression.evaluate(
                rhythm_region_division_list,
                rhythm_region_start_offset, voice_name)
            rhythm_region_expressions.append(rhythm_region_expression)
        #self._debug_values(rhythm_region_expressions, 'rrxs')
        rhythm_region_expressions = \
            self.merge_prolonging_rhythm_region_expressions(
            rhythm_region_expressions)
        #self._debug_values(rhythm_region_expressions, 'rrxs')
        return rhythm_region_expressions

    def make_timespan_delimited_single_context_set_expressions(self, attribute):
        for voice in iterate(self.score).by_class(scoretools.Voice):
            timespan_delimited_single_context_set_expressions = \
                self.score_specification.make_timespan_delimited_single_context_set_expressions_for_voice(
                attribute, voice.name)
            timespan_delimited_single_context_set_expressions.sort_and_split_set_expressions()
            timespan_delimited_single_context_set_expressions.compute_logical_or()
            timespan_delimited_single_context_set_expressions.supply_missing_set_expressions(
                attribute, self.score_specification, voice.name)
            voice_proxy = \
                self.score_specification.single_context_set_expressions_by_context[voice.name]
            inventory = \
                voice_proxy.timespan_delimited_single_context_set_expressions_by_attribute[attribute]
            inventory[:] = timespan_delimited_single_context_set_expressions[:]

    def merge_prolonging_rhythm_region_expressions(
        self, rhythm_region_expressions):
        from experimental.tools import musicexpressiontools
        result = []
        for rhythm_region_expression in rhythm_region_expressions:
            if result and isinstance(
                rhythm_region_expression,
                musicexpressiontools.SelectExpressionRhythmRegionExpression) \
                and rhythm_region_expression.prolongs_expr(result[-1]):
                current_stop_offset = rhythm_region_expression.start_offset
                current_stop_offset += rhythm_region_expression.total_duration
                previous_stop_offset = \
                    result[-1].start_offset + result[-1].total_duration
                extra_duration = current_stop_offset - previous_stop_offset
                assert 0 <= extra_duration
                result[-1]._total_duration += extra_duration
            else:
                result.append(rhythm_region_expression)
        return result

    def populate_single_context_time_signature_set_expressions(self):
        score_proxy = \
            self.score_specification.single_context_set_expressions_by_context.score_proxy
        single_context_time_signature_set_expressions = \
            score_proxy.single_context_set_expressions_by_attribute.get(
                'time_signatures', [])
        if single_context_time_signature_set_expressions:
            single_context_time_signature_set_expression = \
                single_context_time_signature_set_expressions[-1]
            self.score_specification.single_context_time_signature_set_expressions.append(
                single_context_time_signature_set_expression)
            return
        for segment_specification in \
            self.score_specification.segment_specifications:
            score_proxy = \
                segment_specification.single_context_set_expressions_by_context.score_proxy
            single_context_time_signature_set_expressions = \
                score_proxy.single_context_set_expressions_by_attribute.get(
                    'time_signatures', [])
            if not single_context_time_signature_set_expressions:
                continue
            single_context_time_signature_set_expression = \
                single_context_time_signature_set_expressions[-1]
            self.score_specification.single_context_time_signature_set_expressions.append(
                single_context_time_signature_set_expression)