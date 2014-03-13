# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.managers.MaterialManager import MaterialManager


class SargassoMeasureMaterialManager(MaterialManager):
    r'''Sargasso measure material manager.
    '''

    ### CLASS VARIABLES ###


    ### INITIALIZER ###

    def __init__(self, path, session=None):
        superclass = super(SargassoMeasureMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'sargasso measures'
        self._output_material_module_import_statements = [
            'from abjad import *',
            ]
        self._should_have_user_input_module = True
        wrapper = self._initialize_user_input_wrapper_in_memory()

    ### SPECIAL METHODS ###

    @staticmethod
    def __illustrate__(measures, **kwargs):
        r'''Illustrates sargasso measures.

        Returns LilyPond file.
        '''
        staff = scoretools.Staff(measures)
        staff.context_name = 'RhythmicStaff'
        score = scoretools.Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        illustration.file_initial_system_comments = []
        illustration.file_initial_system_includes = []
        measures = score._get_components(scoretools.Measure)
        for measure in measures:
            beam = spannertools.Beam()
            attach(beam, [measure])
        score.add_final_bar_line()
        return illustration

    ### PRIVATE METHODS ###

    @staticmethod
    def _check_output_material(material):
        return all(
            isinstance(_, scoretools.Measure) and _.implicit_scaling
            for _ in material
            )

    @staticmethod
    def _get_possible_meter_multipliers(multiplied_measure_numerator):
        possible_meter_multipliers = []
        for denominator in range(
                multiplied_measure_numerator, 
                2 * multiplied_measure_numerator):
            possible_meter_multiplier = \
                Multiplier(multiplied_measure_numerator, denominator)
            possible_meter_multipliers.append(possible_meter_multiplier)
        return possible_meter_multipliers

    @staticmethod
    def _make_output_material(
        measure_denominator, 
        measure_numerator_talea,
        measure_division_denominator, 
        measure_division_talea, 
        total_duration,
        measures_are_scaled, 
        measures_are_split, 
        measures_are_shuffled,
        ):

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
        measure_numerators = sequencetools.repeat_sequence_to_weight(
            measure_numerator_talea, weight)
        #print measure_numerators

        weight = int(measure_division_denominator * total_duration)
        measure_divisions = sequencetools.repeat_sequence_to_weight(
            measure_division_talea, weight)
        #print measure_divisions

        multiplier = measure_division_denominator / measure_denominator
        multiplied_measure_numerators = [
            multiplier * x for x in measure_numerators]
        #print multiplied_measure_numerators

        measure_divisions_by_measure = sequencetools.split_sequence(
            measure_divisions, 
            multiplied_measure_numerators, 
            cyclic=True, 
            overhang=True,
            )
        #print measure_divisions_by_measure

        meter_multipliers = [
            Multiplier(1) for x in measure_divisions_by_measure
            ]

        if measures_are_scaled:

            meter_multipliers = []
            for measure_index, multiplied_measure_numerator in \
                enumerate(multiplied_measure_numerators):
                possible_multipliers = \
                    SargassoMeasureMaterialManager._get_possible_meter_multipliers(
                    multiplied_measure_numerator)
                meter_multiplier = \
                    SargassoMeasureMaterialManager._select_meter_multiplier(
                    possible_multipliers, measure_index)
                meter_multipliers.append(meter_multiplier)
            #print meter_multipliers

            prolated_measure_numerators = []
            for meter_multiplier, multiplied_measure_numerator in \
                zip(meter_multipliers, multiplied_measure_numerators):
                prolated_measure_numerator = \
                    multiplied_measure_numerator / meter_multiplier
                assert mathtools.is_integer_equivalent_number(
                    prolated_measure_numerator)
                prolated_measure_numerator = int(prolated_measure_numerator)
                prolated_measure_numerators.append(prolated_measure_numerator)
            #print prolated_measure_numerators

            measure_divisions = \
                sequencetools.repeat_sequence_to_weight(
                measure_division_talea, sum(prolated_measure_numerators))
            #print measure_divisions

            measure_divisions_by_measure = \
                sequencetools.split_sequence(
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
                    token = (meter_multiplier, division_list)
                    divided_measure_tokens.append(token)
        #for x in divided_measure_tokens: print x

        if measures_are_shuffled:
            divided_measure_tokens = \
                SargassoMeasureMaterialManager._permute_divided_measure_tokens(
                divided_measure_tokens)

        meter_tokens = []
        for meter_multiplier, measure_divisions in divided_measure_tokens:
            measure_duration = meter_multiplier * Multiplier(
                sum(measure_divisions), measure_division_denominator)
            meter_base_unit = meter_multiplier * Multiplier(
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
            leaves = scoretools.make_leaves_from_talea(
                division_token, measure_division_denominator)
            measure = scoretools.Measure(
                meter_token, 
                leaves,
                implicit_scaling=True,
                )
            measures.append(measure)
        #print measures

        return measures

    def _make_output_material_module_body_lines(self, output_material):
        lines = []
        lines.append('{} = ['.format(self._material_package_name))
        for measure in output_material[:-1]:
            line = measure._one_line_input_string
            line = 'scoretools.' + line
            lines.append('\t{},'.format(line))
        line = output_material[-1]._one_line_input_string
        lines.append('\tscoretools.{}]'.format(line))
        lines = [line + '\n' for line in lines]
        return lines

    @staticmethod
    def _permute_divided_measure_tokens(divided_measure_tokens):
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
    def _select_meter_multiplier(possible_meter_multipliers, measure_index):
        possible_meter_multipliers = \
            datastructuretools.CyclicTuple(possible_meter_multipliers)
        meter_multiplier = possible_meter_multipliers[5 * measure_index]
        return meter_multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def user_input_demo_values(self):
        r'''Gest user input demo values.

        Returns list.
        '''
        return [
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', 
                [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
            ('total_duration', durationtools.Duration(44, 8)),
            ('measures_are_scaled', True),
            ('measures_are_split', True),
            ('measures_are_shuffled', True),
        ]

    @property
    def user_input_module_import_statements(self):
        r'''Gets user input module import statements.

        Returns list of strings.
        '''
        return ['from abjad import *']

    @property
    def user_input_tests(self):
        r'''Gets user input tests.

        Returns list of pairs.
        '''
        from scoremanager import predicates
        return [
            ('measure_denominator', 
                mathtools.is_positive_integer_power_of_two),
            ('measure_numerator_talea', 
                mathtools.all_are_nonnegative_integers),
            ('measure_division_denominator', 
                mathtools.is_nonnegative_integer_power_of_two),
            ('measure_division_talea', 
                mathtools.all_are_nonnegative_integers),
            ('total_duration', predicates.is_duration_token,
                'evaluated_user_input = Duration({})'),
            ('measures_are_scaled', predicates.is_boolean),
            ('measures_are_split', predicates.is_boolean),
            ('measures_are_shuffled', predicates.is_boolean),
        ]
