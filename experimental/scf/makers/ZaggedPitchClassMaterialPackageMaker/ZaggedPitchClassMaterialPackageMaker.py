from abjad.tools import sequencetools
from baca.music.make_zagged_pitch_classes import make_illustration_from_output_material
from experimental.tools import specificationtools
from scf.makers.FunctionInputMaterialPackageMaker import FunctionInputMaterialPackageMaker
import baca


class ZaggedPitchClassMaterialPackageMaker(FunctionInputMaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'zagged pitch-classes'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, specificationtools.StatalServer))
    output_material_maker = staticmethod(baca.music.make_zagged_pitch_classes)
    output_material_module_import_statements = [
        'from abjad.tools import sequencetools',
        'from experimental.tools import specificationtools',
        ]

    user_input_demo_values = [
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),
        ]

    user_input_tests = [
        ('pc_cells', list),
        ('division_cells', list),
        ('grouping_counts', sequencetools.all_are_nonnegative_integers),
        ]
