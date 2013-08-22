# -*- encoding: utf-8 -*-
import fractions
from abjad import *
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.editors.UserInputWrapper \
    import UserInputWrapper
from experimental.tools.scoremanagertools.materialpackagemakers.FunctionInputMaterialPackageMaker \
    import FunctionInputMaterialPackageMaker


class SargassoMeasureMaterialPackageMaker(FunctionInputMaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'sargasso measures'

    output_material_checker = staticmethod(lambda output: all(
        isinstance(x, measuretools.Measure) for x in output))

    output_material_module_import_statements = [
        'from abjad.tools import measuretools']

    user_input_demo_values = [
        ('measure_denominator', 4),
        ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
        ('measure_division_denominator', 16),
        ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
        ('total_duration', durationtools.Duration(44, 8)),
        ('measures_are_scaled', True),
        ('measures_are_split', True),
        ('measures_are_shuffled', True),
        ]

    user_input_module_import_statements = [
        'from abjad.tools import durationtools']

    user_input_tests = [
        ('measure_denominator', 
            mathtools.is_positive_integer_power_of_two),
        ('measure_numerator_talea', 
            sequencetools.all_are_nonnegative_integers),
        ('measure_division_denominator', 
            mathtools.is_nonnegative_integer_power_of_two),
        ('measure_division_talea', 
            sequencetools.all_are_nonnegative_integers),
        ('total_duration', predicates.is_duration_token,
            'evaluated_user_input = Duration({})'),
        ('measures_are_scaled', predicates.is_boolean),
        ('measures_are_split', predicates.is_boolean),
        ('measures_are_shuffled', predicates.is_boolean),
        ]

    ### PUBLIC METHODS ###

    @staticmethod
    def get_possible_meter_multipliers(multiplied_measure_numerator):
        possible_meter_multipliers = []
        for denominator in range(
                multiplied_measure_numerator, 
                2 * multiplied_measure_numerator):
            possible_meter_multiplier = \
                fractions.Fraction(multiplied_measure_numerator, denominator)
            possible_meter_multipliers.append(possible_meter_multiplier)
        return possible_meter_multipliers

    @staticmethod
    def illustration_maker(measures, **kwargs):
        staff = stafftools.RhythmicStaff(measures)
        score = scoretools.Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        illustration.file_initial_system_comments = []
        illustration.file_initial_system_includes = []
        measures = score._get_components(measuretools.Measure)
        for measure in measures:
            beam = spannertools.BeamSpanner()
            beam.attach([measure])
        score.add_double_bar()
        return illustration

    def make_output_material_module_body_lines(self, output_material):
        lines = []
        lines.append('{} = ['.format(self.material_package_name))
        for measure in output_material[:-1]:
            line = measuretools.measure_to_one_line_input_string(measure)
            line = 'measuretools.' + line
            lines.append('\t{},'.format(line))
        line = measuretools.measure_to_one_line_input_string(
            output_material[-1])
        lines.append('\tmeasuretools.{}]'.format(line))
        lines = [line + '\n' for line in lines]
        return lines

    @staticmethod
    def output_material_maker(measure_denominator, measure_numerator_talea,
        measure_division_denominator, measure_division_talea, total_duration,
        measures_are_scaled, measures_are_split, measures_are_shuffled):

        #print measure_denominator
        #print measure_numerator_talea
        #print measure_division_denominator
        #print measure_division_talea
        #print total_duration
        #print measures_are_scaled
        #print measures_are_split
        #print measures_are_shuffled

        assert mathtools.is_nonnegative_integer_power_of_two(
            measure_denominator)
        assert mathtools.is_nonnegative_integer_power_of_two(
            measure_division_denominator)
        assert measure_denominator <= measure_division_denominator

        assert all(mathtools.is_positive_integer(x) 
            for x in measure_numerator_talea)
        assert all(mathtools.is_positive_integer(x) 
            for x in measure_division_talea)
        total_duration = durationtools.Duration(total_duration)

        weight = int(measure_denominator * total_duration)
        measure_numerators = sequencetools.repeat_sequence_to_weight_exactly(
            measure_numerator_talea, weight)
        #print measure_numerators

        weight = int(measure_division_denominator * total_duration)
        measure_divisions = sequencetools.repeat_sequence_to_weight_exactly(
            measure_division_talea, weight)
        #print measure_divisions

        multiplier = measure_division_denominator / measure_denominator
        multiplied_measure_numerators = [
            multiplier * x for x in measure_numerators]
        #print multiplied_measure_numerators

        measure_divisions_by_measure = sequencetools.split_sequence_by_weights(
            measure_divisions, 
            multiplied_measure_numerators, 
            cyclic=True, 
            overhang=True,
            )
        #print measure_divisions_by_measure

        meter_multipliers = [fractions.Fraction(1) 
            for x in measure_divisions_by_measure]

        if measures_are_scaled:

            meter_multipliers = []
            for measure_index, multiplied_measure_numerator in \
                enumerate(multiplied_measure_numerators):
                possible_multipliers = \
                    SargassoMeasureMaterialPackageMaker.get_possible_meter_multipliers(
                    multiplied_measure_numerator)
                meter_multiplier = \
                    SargassoMeasureMaterialPackageMaker.select_meter_multiplier(
                    possible_multipliers, measure_index)
                meter_multipliers.append(meter_multiplier)
            #print meter_multipliers

            prolated_measure_numerators = []
            for meter_multiplier, multiplied_measure_numerator in zip(
                meter_multipliers, multiplied_measure_numerators):
                prolated_measure_numerator = \
                    multiplied_measure_numerator / meter_multiplier
                assert mathtools.is_integer_equivalent_number(
                    prolated_measure_numerator)
                prolated_measure_numerator = int(prolated_measure_numerator)
                prolated_measure_numerators.append(prolated_measure_numerator)
            #print prolated_measure_numerators

            measure_divisions = \
                sequencetools.repeat_sequence_to_weight_exactly(
                measure_division_talea, sum(prolated_measure_numerators))
            #print measure_divisions

            measure_divisions_by_measure = \
                sequencetools.split_sequence_by_weights(
                measure_divisions,
                prolated_measure_numerators,
                cyclic=True,
                overhang=True)
            #print measure_divisions_by_measure

        measure_tokens = zip(meter_multipliers, measure_divisions_by_measure)
        #for x in measure_tokens: print x

        if measures_are_split:
            ratio = [1, 1]
        else:
            ratio = [1]

        divided_measure_tokens = []
        for meter_multiplier, measure_divisions in measure_tokens:
            division_lists = \
                sequencetools.partition_sequence_by_ratio_of_lengths(
                    measure_divisions, ratio)
            for division_list in division_lists:
                if division_list:
                    divided_measure_tokens.append(
                        (meter_multiplier, division_list))
        #for x in divided_measure_tokens: print x

        if measures_are_shuffled:
            divided_measure_tokens = \
                SargassoMeasureMaterialPackageMaker.permute_divided_measure_tokens(
                divided_measure_tokens)

        meter_tokens = []
        for meter_multiplier, measure_divisions in divided_measure_tokens:
            measure_duration = meter_multiplier * fractions.Fraction(
                sum(measure_divisions), measure_division_denominator)
            meter_base_unit = meter_multiplier * fractions.Fraction(
                min(measure_divisions), measure_division_denominator)
            meter_denominator = meter_base_unit.denominator
            meter_token = \
                mathtools.NonreducedFraction(measure_duration).with_multiple_of_denominator(
                meter_denominator)
            meter_tokens.append(meter_token)
        #print meter_tokens

        division_tokens = []
        for measure_duration, division_token in divided_measure_tokens:
            division_tokens.append(division_token)
        #print division_tokens

        measures = []
        for meter_token, division_token in zip(meter_tokens, division_tokens):
            leaves = leaftools.make_leaves_from_talea(
                division_token, measure_division_denominator)
            measure = measuretools.Measure(meter_token, leaves)
            measures.append(measure)
        #print measures

        return measures

    @staticmethod
    def permute_divided_measure_tokens(divided_measure_tokens):
        modulus_of_permutation = 5
        len_divided_measure_tokens = len(divided_measure_tokens)
        assert mathtools.are_relatively_prime(
            [modulus_of_permutation, len_divided_measure_tokens])
        permutation = [(5 * x) % len_divided_measure_tokens 
            for x in range(len_divided_measure_tokens)]
        divided_measure_tokens = \
            sequencetools.permute_sequence(
                divided_measure_tokens, permutation)
        return divided_measure_tokens

    @staticmethod
    def select_meter_multiplier(possible_meter_multipliers, measure_index):
        possible_meter_multipliers = \
            sequencetools.CyclicTuple(possible_meter_multipliers)
        meter_multiplier = possible_meter_multipliers[5 * measure_index]
        return meter_multiplier
